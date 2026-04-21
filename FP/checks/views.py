from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlantCheck
from .forms import PlantCheckForm, CropRecommendationForm


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
    return render(request, 'checks/dashboard.html', {
        'check_types': CHECK_TYPE_META,
        'recent_checks': recent_checks,
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
        else:
            form = PlantCheckForm(request.POST, request.FILES)
        
        if form.is_valid():
            check = form.save(commit=False)
            check.user = request.user
            check.check_type = check_type
            check.save()

                # Run analysis — try ML model first, fall back to Gemini AI
            try:
                from django.conf import settings as app_settings
                result = None

                if check_type == 'yield':
                    from .ai_checks import analyze_crop_recommendation as ai_analyze
                    result = ai_analyze(check.temperature, check.soil_type, check.rainfall, check.proposed_crop)
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
                import traceback
                print("--- AI ANALYSIS ERROR ---")
                traceback.print_exc()
                print("-------------------------")
                messages.warning(request, str(e))
                # Still redirect to result page even if analysis failed
                return redirect('check_result', pk=check.pk)
            except Exception as e:
                import traceback
                print("--- AI ANALYSIS ERROR ---")
                traceback.print_exc()
                print("-------------------------")
                messages.error(request, f'❌ Analysis error: {str(e)[:100]}')
                return redirect('check_result', pk=check.pk)
        else:
            messages.error(request, 'Please upload a valid image.')
    else:
        if check_type == 'yield':
            form = CropRecommendationForm()
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
