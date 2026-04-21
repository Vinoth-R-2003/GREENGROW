from google import genai
from django.conf import settings
import json
import re
import time
import base64


PROMPTS = {
    'health': """You are an expert plant pathologist and botanist. Analyze this plant image for overall health status.

Provide your analysis in the following JSON format ONLY (no markdown, no explanation):
{{
    "title": "Brief health status title (e.g., 'Healthy Tomato Plant' or 'Nutrient-Deficient Rose')",
    "summary": "2-3 sentence summary of the plant's overall health condition",
    "severity": "One of: healthy, low, medium, high, critical",
    "confidence": 85,
    "details": {{
        "plant_identified": "Name of the plant if identifiable",
        "overall_health": "Good/Fair/Poor/Critical",
        "leaf_condition": "Description of leaf health",
        "stem_condition": "Description of stem health",
        "color_analysis": "Analysis of colors observed",
        "growth_stage": "Estimated growth stage",
        "stress_indicators": ["list", "of", "stress", "signs"]
    }},
    "recommendations": "3-5 actionable recommendations separated by newlines"
}}""",

    'disease': """You are an expert plant pathologist specializing in plant disease detection. Analyze this plant image to identify any diseases, infections, or pest damage.

Provide your analysis in the following JSON format ONLY (no markdown, no explanation):
{{
    "title": "Disease identification title (e.g., 'Powdery Mildew Detected' or 'No Disease Found')",
    "summary": "2-3 sentence summary of the disease analysis findings",
    "severity": "One of: healthy, low, medium, high, critical",
    "confidence": 85,
    "details": {{
        "plant_identified": "Name of the plant if identifiable",
        "disease_detected": true,
        "disease_name": "Name of disease if detected, or 'None'",
        "disease_type": "Fungal/Bacterial/Viral/Pest/Nutrient/None",
        "affected_parts": ["list", "of", "affected", "parts"],
        "symptoms_observed": ["list", "of", "symptoms"],
        "spread_risk": "Low/Medium/High",
        "stage": "Early/Moderate/Advanced/Severe"
    }},
    "recommendations": "3-5 treatment and prevention recommendations separated by newlines"
}}""",

    'yield': """You are an expert agronomist specializing in crop yield assessment. Analyze this plant/crop image to predict the potential yield.

Provide your analysis in the following JSON format ONLY (no markdown, no explanation):
{{
    "title": "Yield prediction title (e.g., 'Good Yield Expected for Tomato Crop')",
    "summary": "2-3 sentence summary of the yield prediction",
    "severity": "One of: healthy, low, medium, high (healthy=excellent yield, low=good, medium=average, high=below average)",
    "confidence": 75,
    "details": {{
        "plant_identified": "Name of the crop if identifiable",
        "growth_stage": "Seedling/Vegetative/Flowering/Fruiting/Mature/Harvest-ready",
        "yield_potential": "Excellent/Good/Average/Below Average/Poor",
        "estimated_harvest_time": "Estimated days or weeks to harvest",
        "fruit_count_visible": "Number of fruits/vegetables visible if applicable",
        "plant_vigor": "Strong/Moderate/Weak",
        "environmental_factors": ["list", "of", "observed", "environmental", "factors"],
        "limiting_factors": ["list", "of", "factors", "limiting", "yield"]
    }},
    "recommendations": "3-5 recommendations to maximize yield separated by newlines"
}}""",

    'encyclopedia': """You are an expert botanist and horticulturist. Analyze this image to identify the plant and provide encyclopedic information.

Provide your analysis in the following JSON format ONLY (no markdown, no explanation):
{{
    "title": "Plant identification title (e.g., 'Tomato Plant Identified' or 'Unknown Plant')",
    "summary": "2-3 sentence overview of the plant, its origin, and common uses.",
    "severity": "healthy",
    "confidence": 85,
    "details": {{
        "plant_identified": "Scientific and common name of the plant",
        "family": "Botanical family",
        "origin": "Native region or origin",
        "growth_habit": "e.g., Shrub, Tree, Vine, Herbaceous",
        "light_requirements": "e.g., Full sun, Partial shade",
        "water_requirements": "e.g., Moderate, High, Drought-tolerant",
        "ideal_climate": ["list", "of", "ideal", "climates", "or", "zones"],
        "common_uses": ["list", "of", "uses"]
    }},
    "recommendations": "3-5 general care tips for this plant separated by newlines"
}}"""
}


def analyze_plant_image(image_path, check_type):
    """
    Use Google Gemini AI with vision to analyze a plant image.
    Returns a dict with analysis results.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in settings.")

    if check_type not in PROMPTS:
        raise ValueError(f"Invalid check type: {check_type}")

    client = genai.Client(api_key=api_key)
    prompt = PROMPTS[check_type]

    # Read and encode the image
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Determine MIME type
    ext = str(image_path).lower().rsplit('.', 1)[-1]
    mime_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
        'gif': 'image/gif',
    }
    mime_type = mime_map.get(ext, 'image/jpeg')

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    {
                        'inline_data': {
                            'mime_type': mime_type,
                            'data': base64.b64encode(image_data).decode('utf-8'),
                        }
                    },
                    prompt,
                ],
            )
            text = response.text.strip()

            # Remove markdown code fences if present
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            text = text.strip()

            result = json.loads(text)

            # Validate required fields
            valid_severities = ['healthy', 'low', 'medium', 'high', 'critical']
            severity = result.get('severity', 'medium')
            if severity not in valid_severities:
                severity = 'medium'

            confidence = result.get('confidence', 70)
            try:
                confidence = float(confidence)
                confidence = max(0, min(100, confidence))
            except (ValueError, TypeError):
                confidence = 70.0

            return {
                'title': str(result.get('title', 'Analysis Complete')),
                'summary': str(result.get('summary', '')),
                'severity': severity,
                'confidence': confidence,
                'details': result.get('details', {}),
                'recommendations': str(result.get('recommendations', '')),
            }

        except json.JSONDecodeError as e:
            raise ValueError(f"AI returned an invalid response. Please try again. Error: {e}")
        except Exception as e:
            last_error = e
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "resource" in error_str.lower():
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    time.sleep(wait_time)
                    continue
                raise ValueError(
                    "🔄 API quota exceeded. Please try again in a few moments. "
                    "The AI check feature has reached its usage limit and will be available again soon."
                )
            raise ValueError(f"AI analysis failed: {e}")

    raise ValueError(f"AI analysis failed after {max_retries} retries: {last_error}")

def analyze_crop_recommendation(temperature, soil_type, rainfall, proposed_crop=None):
    """
    Use Google Gemini AI to analyze environmental parameters and recommend the best crop to grow.
    Returns a dict with analysis results.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in settings.")

    client = genai.Client(api_key=api_key)
    
    proposed_crop_text = f"The user is thinking of planting: {proposed_crop}." if proposed_crop else "The user has not specified a default crop."
    
    prompt = f"""You are an expert agronomist and crop consultant. A farmer wants your advice.
Environmental conditions:
- Temperature: {temperature} °C
- Soil Type: {soil_type}
- Annual Rainfall: {rainfall} mm
{proposed_crop_text}

Analyze these conditions to recommend the BEST crop(s) for these exact conditions and predict potential yield success. If they proposed a crop, evaluate its viability first, then provide alternatives if there's a better option. 

Provide your analysis in the following JSON format ONLY (no markdown, no explanation):
{{
    "title": "Short title (e.g., 'Ideal for Rice Cultivation')",
    "summary": "2-3 sentence overview of why the recommended crop is suitable or if the proposed crop is viable.",
    "severity": "One of: healthy, low, medium, high (healthy=excellent match, low=good match, medium=fair, high=poor match for proposed)",
    "confidence": 85,
    "details": {{
        "best_recommended_crop": "Name of best crop to grow",
        "proposed_crop_viability": "Viable/Not Viable/Unknown",
        "alternative_crops": ["list", "of", "other", "good", "options"],
        "expected_growth_challenges": ["list", "of", "challenges"],
        "soil_suitability": "Excellent/Good/Average/Poor",
        "water_needs_meet": "Yes/No/Requires Irrigation"
    }},
    "recommendations": "3-5 recommendations on preparation, sowing season, and fertilizer separated by newlines"
}}"""

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[prompt],
            )
            text = response.text.strip()

            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            text = text.strip()

            result = json.loads(text)

            valid_severities = ['healthy', 'low', 'medium', 'high', 'critical']
            severity = result.get('severity', 'medium')
            if severity not in valid_severities:
                severity = 'medium'

            confidence = result.get('confidence', 70)
            try:
                confidence = float(confidence)
                confidence = max(0, min(100, confidence))
            except (ValueError, TypeError):
                confidence = 70.0

            return {
                'title': str(result.get('title', 'Recommendation Complete')),
                'summary': str(result.get('summary', '')),
                'severity': severity,
                'confidence': confidence,
                'details': result.get('details', {}),
                'recommendations': str(result.get('recommendations', '')),
            }

        except json.JSONDecodeError as e:
            raise ValueError(f"AI returned an invalid response. Please try again. Error: {e}")
        except Exception as e:
            last_error = e
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "resource" in error_str.lower():
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    time.sleep(wait_time)
                    continue
                raise ValueError("API quota exceeded. Please try again later.")
            raise ValueError(f"AI recommendation failed: {e}")

    raise ValueError(f"AI recommendation failed after {max_retries} retries: {last_error}")

