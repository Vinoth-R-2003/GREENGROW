from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Plant, UserPlant, PlantJournal, GardenTask, GardenExpense

# ... (existing code, not replaced) ...

def plant_list(request):
    plants = Plant.objects.all()
    user_plants = []
    if request.user.is_authenticated:
        user_plants = UserPlant.objects.filter(user=request.user).values_list('plant_id', flat=True)
    return render(request, 'garden/plant_list.html', {'plants': plants, 'user_plant_ids': user_plants})

def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    user_plant = None
    if request.user.is_authenticated:
        user_plant = UserPlant.objects.filter(user=request.user, plant=plant).first()
    return render(request, 'garden/plant_detail.html', {'plant': plant, 'user_plant': user_plant})

@login_required
def my_garden(request):
    user_plants = UserPlant.objects.filter(user=request.user).select_related('plant')
    return render(request, 'garden/user_garden_final.html', {'user_plants': user_plants})

@login_required
def add_to_garden(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    UserPlant.objects.get_or_create(user=request.user, plant=plant)
    return redirect('my_garden')

@login_required
def update_plant_status(request, user_plant_id):
    if request.method == "POST":
        user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(UserPlant.STATUS_CHOICES):
            user_plant.status = new_status
            user_plant.save()
    return redirect('my_garden')

@login_required
def plant_journal(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    entries = user_plant.journal_entries.all()
    return render(request, 'garden/journal_list.html', {'user_plant': user_plant, 'entries': entries})

@login_required
def add_journal_entry(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        PlantJournal.objects.create(
            user_plant=user_plant,
            title=title,
            content=content,
            image=image
        )
        return redirect('plant_journal', user_plant_id=user_plant.id)
    return render(request, 'garden/journal_form.html', {'user_plant': user_plant})

# --- New Views for Garden Features ---

from .forms import HarvestForm, GardenTaskForm, HealthLogForm, GardenExpenseForm, PlantUpdateForm
import qrcode
from io import BytesIO
from django.core.files import File

@login_required
def generate_qr_code(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    # URL to the plant detail page (you might want to make this a public URL if sharing)
    # For now, it points to the internal detail view
    url = request.build_absolute_uri(f'/garden/user-plant/{user_plant.id}/')
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    blob = BytesIO()
    img.save(blob, 'PNG')
    user_plant.qr_code.save(f'qr_{user_plant.id}.png', File(blob), save=False)
    user_plant.save()
    return redirect('my_garden')

@login_required
def harvest_list(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    harvests = user_plant.harvests.all()
    if request.method == 'POST':
        form = HarvestForm(request.POST)
        if form.is_valid():
            harvest = form.save(commit=False)
            harvest.user_plant = user_plant
            harvest.save()
            return redirect('harvest_list', user_plant_id=user_plant_id)
    else:
        form = HarvestForm()
    return render(request, 'garden/harvest_list.html', {'user_plant': user_plant, 'harvests': harvests, 'form': form})

@login_required
def task_list(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    tasks = user_plant.tasks.all()
    if request.method == 'POST':
        form = GardenTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_plant = user_plant
            task.save()
            return redirect('task_list', user_plant_id=user_plant_id)
    else:
        form = GardenTaskForm()
    return render(request, 'garden/task_list.html', {'user_plant': user_plant, 'tasks': tasks, 'form': form})

@login_required
def generate_ai_tasks_view(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    try:
        from .ai_tasks import generate_ai_tasks
        tasks_data = generate_ai_tasks(
            plant_name=user_plant.plant.name,
            plant_description=user_plant.plant.description,
            how_to_grow=user_plant.plant.how_to_grow,
        )
        created = 0
        for task_info in tasks_data:
            GardenTask.objects.create(
                user_plant=user_plant,
                task_type=task_info['task_type'],
                due_date=task_info['due_date'],
                recurrence_days=task_info.get('recurrence_days'),
                notes=task_info.get('notes', ''),
            )
            created += 1
        from django.contrib import messages
        messages.success(request, f'✅ AI generated {created} tasks for {user_plant.plant.name}!')
    except ValueError as e:
        from django.contrib import messages
        # ValueError is raised for API quota or validation errors - show user-friendly message
        if "quota" in str(e).lower():
            messages.warning(request, str(e))
        else:
            messages.error(request, str(e))
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f'❌ Unexpected error: {str(e)[:100]}')
    return redirect('task_list', user_plant_id=user_plant_id)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(GardenTask, pk=task_id, user_plant__user=request.user)
    task.is_completed = True
    task.save()
    # Logic for recurrence could go here (create existing task copy with new date)
    return redirect('task_list', user_plant_id=task.user_plant.id)

@login_required
def health_log_list(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    logs = user_plant.health_logs.all()
    if request.method == 'POST':
        form = HealthLogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.user_plant = user_plant
            log.save()
            return redirect('health_log_list', user_plant_id=user_plant_id)
    else:
        form = HealthLogForm()
    return render(request, 'garden/health_log_list.html', {'user_plant': user_plant, 'logs': logs, 'form': form})

@login_required
def expense_list(request):
    expenses = request.user.garden_expenses.all()
    if request.method == 'POST':
        form = GardenExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = GardenExpenseForm()
    return render(request, 'garden/expense_list.html', {'expenses': expenses, 'form': form})

@login_required
def user_plant_detail(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, pk=user_plant_id, user=request.user)
    if request.method == 'POST':
        form = PlantUpdateForm(request.POST, instance=user_plant)
        if form.is_valid():
            form.save()
            return redirect('user_plant_detail', user_plant_id=user_plant.id)
    else:
        form = PlantUpdateForm(instance=user_plant)
    return render(request, 'garden/user_plant_detail.html', {'user_plant': user_plant, 'form': form})
