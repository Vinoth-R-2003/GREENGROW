from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from .models import PlantCheck
from .forms import PlantCheckForm, CropRecommendationForm, EncyclopediaSearchForm


CHECK_TYPE_META = {
    'health': {
        'title': 'Plant Health Checkup',
        'description': 'Upload a photo of your plant to get a comprehensive health analysis.',
        'icon': '💚',
        'color': 'emerald',
    },
    'disease': {
        'title': 'Plant Disease Detection',
        'description': 'Upload a photo to detect diseases, infections, or pest damage.',
        'icon': '🔬',
        'color': 'blue',
    },
    'yield': {
        'title': 'Crop Recommendation',
        'description': 'Enter temperature, soil type, and rainfall to get the best crop recommendations.',
        'icon': '📊',
        'color': 'amber',
    },
    'encyclopedia': {
        'title': 'Plants Encyclopedia',
        'description': 'Upload a photo of a plant to identify it and learn about its characteristics.',
        'icon': '🌿',
        'color': 'purple',
    },
}


@login_required
def checks_dashboard(request):
    recent_checks = PlantCheck.objects.filter(user=request.user)[:6]
    
    # Get weather data if user has location
    weather = None
    if request.user.latitude and request.user.longitude:
        from .weather import get_weather_data
        weather = get_weather_data(request.user.latitude, request.user.longitude)
        
    return render(request, 'checks/dashboard.html', {
        'check_types': CHECK_TYPE_META,
        'recent_checks': recent_checks,
        'weather': weather,
    })


@login_required
def upload_check(request, check_type):
    if check_type not in CHECK_TYPE_META:
        messages.error(request, 'Invalid check type.')
        return redirect('checks_dashboard')

    meta = CHECK_TYPE_META[check_type]

    if request.method == 'POST':
        if check_type == 'yield':
            form = CropRecommendationForm(request.POST)
        elif check_type == 'encyclopedia' and request.POST.get('plant_name', '').strip():
            form = EncyclopediaSearchForm(request.POST)
        else:
            form = PlantCheckForm(request.POST, request.FILES)
        
        if form.is_valid():
            if check_type == 'encyclopedia' and request.POST.get('plant_name', '').strip():
                # Handle Text Search for Encyclopedia
                plant_name = form.cleaned_data['plant_name']
                
                check = PlantCheck(user=request.user, check_type=check_type)
                # Don't save it yet until we get results
                
                try:
                    from .ai_checks import search_plant_encyclopedia
                    result = search_plant_encyclopedia(plant_name)
                    
                    check.result_title = result['title']
                    check.result_summary = result['summary']
                    check.severity = result['severity']
                    check.confidence_score = result['confidence']
                    check.result_details = result['details']
                    check.recommendations = result['recommendations']
                    check.save()
                    
                    messages.success(request, f'✅ Encyclopedia entry for {plant_name} found!')
                    return redirect('check_result', pk=check.pk)
                    
                except Exception as e:
                    import traceback
                    print("--- AI SEARCH ERROR ---")
                    traceback.print_exc()
                    messages.error(request, f'❌ Search error: {str(e)}')
                    return redirect('upload_check', check_type=check_type)

            else:
                # Handle Standard Image Uploads or Yield
                check = form.save(commit=False)
                check.user = request.user
                check.check_type = check_type
                check.save()

                # Run analysis — try ML model first, fall back to Gemini AI
                try:
                    from django.conf import settings as app_settings
                    result = None

                    if check_type == 'yield':
                        from .ml_engine import predict_crop as ml_predict_crop
                        result = ml_predict_crop(check.temperature, check.soil_type, check.rainfall, check.proposed_crop)
                    else:
                        # Attempt ML-based analysis first
                        if getattr(app_settings, 'USE_ML_MODEL', False):
                            try:
                                from .ml_engine import analyze_plant_image as ml_analyze
                                from .ml_engine import is_model_available
                                if is_model_available():
                                    result = ml_analyze(check.image.path, check_type)
                            except Exception as ml_err:
                                # ML failed — will fall back to Gemini
                                result = None

                        # Fall back to Gemini AI if ML didn't produce a result
                        if result is None:
                            from .ai_checks import analyze_plant_image as ai_analyze
                            result = ai_analyze(check.image.path, check_type)

                    check.result_title = result['title']
                    check.result_summary = result['summary']
                    check.severity = result['severity']
                    check.confidence_score = result['confidence']
                    check.result_details = result['details']
                    check.recommendations = result['recommendations']
                    check.save()

                    messages.success(request, f'✅ {meta["title"]} complete!')
                    return redirect('check_result', pk=check.pk)

                except ValueError as e:
                    messages.warning(request, str(e))
                    return redirect('check_result', pk=check.pk)
                except Exception as e:
                    messages.error(request, f'❌ Analysis error: {str(e)[:100]}')
                    return redirect('check_result', pk=check.pk)
        else:
            messages.error(request, 'Please provide valid input.')
    else:
        if check_type == 'yield':
            form = CropRecommendationForm()
        elif check_type == 'encyclopedia':
            form = PlantCheckForm() # Used for the upload part
            search_form = EncyclopediaSearchForm()
            return render(request, 'checks/upload.html', {
                'form': form,
                'search_form': search_form,
                'check_type': check_type,
                'meta': meta,
            })
        else:
            form = PlantCheckForm()

    return render(request, 'checks/upload.html', {
        'form': form,
        'check_type': check_type,
        'meta': meta,
    })


@login_required
def check_result(request, pk):
    check = get_object_or_404(PlantCheck, pk=pk, user=request.user)
    meta = CHECK_TYPE_META.get(check.check_type, {})
    
    details_list = []
    if check.result_details:
        for key, value in check.result_details.items():
            details_list.append({
                'key': key,
                'value': value,
                'is_list': isinstance(value, list)
            })

    return render(request, 'checks/result.html', {
        'check': check,
        'meta': meta,
        'details_list': details_list,
    })


@login_required
def check_history(request):
    checks = PlantCheck.objects.filter(user=request.user)
    return render(request, 'checks/history.html', {
        'checks': checks,
        'check_types': CHECK_TYPE_META,
    })


@login_required
def delete_check(request, pk):
    check = get_object_or_404(PlantCheck, pk=pk, user=request.user)
    if request.method == 'POST':
        check.delete()
        messages.success(request, 'Check history record deleted successfully.')
        return redirect('check_history')
    return redirect('check_history')

@login_required
def agro_chat(request):
    """Render the Agro-Assistant chat interface."""
    return render(request, 'checks/chat.html')

@login_required
@require_POST
def agro_chat_api(request):
    """API endpoint for Agro-Assistant chat responses."""
    import json
    try:
        data = json.loads(request.body)
        prompt = data.get('message', '')
        history = data.get('history', [])
        
        if not prompt:
            return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
            
        from .ai_checks import get_agro_advice
        response_text = get_agro_advice(prompt, history)
        
        return JsonResponse({
            'status': 'success',
            'response': response_text
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
