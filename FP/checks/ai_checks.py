import base64
import requests
import json
import re
import time
from django.conf import settings


# ---------------------------------------------------------------------------
# Plant.id API — Image Analysis (health, disease, encyclopedia)
# ---------------------------------------------------------------------------

PLANT_ID_ENDPOINT = "https://api.plant.id/v3/identification"


def _encode_image(image_file):
    """Encode image file to Base64 string for Plant.id API."""
    image_file.open('rb')
    image_file.seek(0)
    return base64.b64encode(image_file.read()).decode("ascii")


def _severity_from_probability(probability):
    """Map a 0-1 confidence probability to our internal severity scale."""
    if probability >= 0.8:
        return "critical"
    elif probability >= 0.6:
        return "high"
    elif probability >= 0.4:
        return "medium"
    elif probability >= 0.2:
        return "low"
    return "healthy"


def analyze_plant_image(image_file, check_type):
    """
    Use the Plant.id v3 API to analyze a plant image.
    Supports check_type: 'health', 'disease', 'encyclopedia'
    Returns a dict compatible with our app's result template.
    """
    api_key = getattr(settings, "PLANT_ID_API_KEY", "")
    if not api_key:
        raise ValueError("PLANT_ID_API_KEY is not configured in settings.")

    encoded_image = _encode_image(image_file)

    # Build request payload — always request identification + health
    payload = {
        "images": [encoded_image],
        "health": "all",
        "classification_level": "species",
    }

    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = requests.post(
                PLANT_ID_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 429:
                if attempt < max_retries - 1:
                    time.sleep((2 ** attempt) * 2)
                    continue
                raise ValueError(
                    "🔄 Plant.id API rate limit reached. Please try again in a few minutes."
                )

            if response.status_code == 401:
                raise ValueError(
                    "❌ Invalid Plant.id API key. Please check the PLANT_ID_API_KEY setting."
                )

            if not response.ok:
                raise ValueError(
                    f"Plant.id API returned an error: {response.status_code} — {response.text[:200]}"
                )

            data = response.json()
            return _parse_plant_id_response(data, check_type)

        except requests.exceptions.Timeout:
            last_error = "Request timed out."
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except ValueError:
            raise
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(2)
                continue

    raise ValueError(f"Plant.id analysis failed after {max_retries} attempts: {last_error}")


def _parse_plant_id_response(data, check_type):
    """
    Convert Plant.id v3 API response into the standard dict
    our Django templates expect.
    """
    result = data.get("result", {})

    # ── Species identification ──────────────────────────────────────────────
    classification = result.get("classification", {})
    suggestions = classification.get("suggestions", [])
    top_species = suggestions[0] if suggestions else {}
    plant_name = top_species.get("name", "Unknown Plant")
    plant_probability = top_species.get("probability", 0.0)
    species_details = top_species.get("details", {})

    common_names = species_details.get("common_names") or []
    common_name = common_names[0] if common_names else plant_name
    description = species_details.get("description", {})
    description_text = (
        description.get("value", "") if isinstance(description, dict) else str(description)
    )

    # ── Health / Disease ────────────────────────────────────────────────────
    health_data = result.get("health_assessment", result.get("disease", {}))
    is_healthy = health_data.get("is_healthy", {})
    is_healthy_prob = (
        is_healthy.get("probability", 1.0) if isinstance(is_healthy, dict) else float(is_healthy)
    )
    diseases = health_data.get("diseases", health_data.get("suggestions", []))

    # Pick the top disease if any
    top_disease = None
    top_disease_prob = 0.0
    for d in diseases:
        prob = d.get("probability", 0.0)
        if prob > top_disease_prob:
            top_disease = d
            top_disease_prob = prob

    disease_name = top_disease.get("name", "None detected") if top_disease else "None detected"
    disease_details_raw = top_disease.get("details", {}) if top_disease else {}
    treatment = disease_details_raw.get("treatment", {}) if isinstance(disease_details_raw, dict) else {}

    # ── Build the standard response based on check_type ────────────────────
    if check_type == "health":
        if is_healthy_prob >= 0.7:
            title = f"Healthy {common_name}"
            severity = "healthy"
            summary = (
                f"Your {common_name} ({plant_name}) appears to be in good health "
                f"with a confidence of {plant_probability * 100:.0f}%. "
                "No significant health issues were detected."
            )
        else:
            title = f"Health Issues Detected — {common_name}"
            severity = _severity_from_probability(1 - is_healthy_prob)
            summary = (
                f"Your plant ({common_name}) shows signs of health issues. "
                f"The most likely problem is {disease_name}. "
                "See recommendations below for treatment advice."
            )

        details = {
            "plant_identified": f"{common_name} ({plant_name})",
            "overall_health": "Good" if is_healthy_prob >= 0.7 else "Poor",
            "disease_detected": disease_name if disease_name != "None detected" else "None",
            "identification_confidence": f"{plant_probability * 100:.0f}%",
        }
        if description_text:
            details["about"] = description_text[:300]

        recs = []
        if treatment:
            if isinstance(treatment, dict):
                for method, advice in treatment.items():
                    if isinstance(advice, str):
                        recs.append(f"{method.title()}: {advice[:150]}")
            elif isinstance(treatment, str):
                recs.append(treatment)
        if not recs:
            recs = ["Monitor your plant regularly.", "Ensure proper watering and sunlight."]
        recommendations = "\n".join(recs[:5])

    elif check_type == "disease":
        if not diseases or top_disease_prob < 0.2:
            title = f"No Disease Found — {common_name}"
            severity = "healthy"
            summary = (
                f"No significant diseases or infections were detected on your {common_name}. "
                "The plant appears to be in healthy condition."
            )
        else:
            title = f"{disease_name} Detected"
            severity = _severity_from_probability(top_disease_prob)
            summary = (
                f"A potential case of **{disease_name}** was detected on your {common_name} "
                f"with {top_disease_prob * 100:.0f}% confidence. "
                "See the treatment recommendations below."
            )

        details = {
            "plant_identified": f"{common_name} ({plant_name})",
            "disease_detected": disease_name,
            "confidence": f"{top_disease_prob * 100:.0f}%",
        }

        recs = []
        if treatment:
            if isinstance(treatment, dict):
                for method, advice in treatment.items():
                    if isinstance(advice, str):
                        recs.append(f"{method.title()}: {advice[:150]}")
            elif isinstance(treatment, str):
                recs.append(treatment)
        if not recs:
            recs = ["Consult a local agronomist for advice.", "Remove affected parts to limit spread."]
        recommendations = "\n".join(recs[:5])

    else:  # encyclopedia
        title = f"{common_name} Identified"
        severity = "healthy"
        summary = (
            description_text[:300]
            if description_text
            else f"This is a {common_name} ({plant_name})."
        )

        taxonomy = species_details.get("taxonomy", {}) or {}
        details = {
            "plant_identified": f"{common_name} ({plant_name})",
            "family": taxonomy.get("family", "Unknown"),
            "identification_confidence": f"{plant_probability * 100:.0f}%",
        }
        sunlight = species_details.get("best_light_condition") or species_details.get("sunlight")
        watering = species_details.get("best_watering") or species_details.get("watering")
        soil = species_details.get("best_soil_type")
        common_uses = species_details.get("common_uses")

        if sunlight:
            details["light_requirements"] = sunlight if isinstance(sunlight, str) else str(sunlight)
        if watering:
            details["water_requirements"] = watering if isinstance(watering, str) else str(watering)
        if soil:
            details["soil_type"] = soil if isinstance(soil, str) else str(soil)
        if common_uses:
            details["common_uses"] = common_uses if isinstance(common_uses, list) else [str(common_uses)]

        recommendations = "Water regularly. Ensure adequate sunlight. Check for pests periodically."

    return {
        "title": title,
        "summary": summary,
        "severity": severity,
        "confidence": round(plant_probability * 100, 1),
        "details": details,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# Google Gemini — Text-based Crop Recommendation (unchanged)
# ---------------------------------------------------------------------------

def analyze_crop_recommendation(temperature, soil_type, rainfall, proposed_crop=None):
    """
    Use Google Gemini AI to analyze environmental parameters and recommend the best crop.
    Returns a dict with analysis results.
    """
    from google import genai

    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in settings.")

    client = genai.Client(api_key=api_key)

    proposed_crop_text = (
        f"The user is thinking of planting: {proposed_crop}."
        if proposed_crop
        else "The user has not specified a default crop."
    )

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
                model="gemini-1.5-flash",
                contents=[prompt],
            )
            text = response.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            text = text.strip()

            result = json.loads(text)

            valid_severities = ["healthy", "low", "medium", "high", "critical"]
            severity = result.get("severity", "medium")
            if severity not in valid_severities:
                severity = "medium"

            confidence = result.get("confidence", 70)
            try:
                confidence = float(confidence)
                confidence = max(0, min(100, confidence))
            except (ValueError, TypeError):
                confidence = 70.0

            return {
                "title": str(result.get("title", "Recommendation Complete")),
                "summary": str(result.get("summary", "")),
                "severity": severity,
                "confidence": confidence,
                "details": result.get("details", {}),
                "recommendations": str(result.get("recommendations", "")),
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


# ---------------------------------------------------------------------------
# Google Gemini — Plant Encyclopedia Search
# ---------------------------------------------------------------------------

def search_plant_encyclopedia(plant_name):
    """
    Use Google Gemini AI to generate an encyclopedia entry for a given plant name.
    """
    from google import genai
    from django.conf import settings

    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in settings.")

    client = genai.Client(api_key=api_key)

    prompt = f"""You are an expert botanist and horticulturist. Provide a comprehensive encyclopedia entry for the plant: "{plant_name}".
Ensure the plant exists. If it's a completely invalid or fake plant name, return an empty JSON object {{}} or indicate it's unknown.

Return strictly in the following JSON format ONLY:
{{
    "title": "Common Name (Scientific Name)",
    "summary": "A 3-4 sentence comprehensive description of the plant.",
    "severity": "healthy",
    "confidence": 99,
    "details": {{
        "plant_identified": "Common Name",
        "family": "Botanical Family",
        "light_requirements": "Sunlight needs",
        "water_requirements": "Watering needs",
        "soil_type": "Best soil type",
        "common_uses": ["Use 1", "Use 2", "Use 3"]
    }},
    "recommendations": "1. Step to grow\\n2. Step to care\\n3. Step to harvest/maintain"
}}"""

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[prompt],
            )
            text = response.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            text = text.strip()

            result = json.loads(text)
            
            if not result or "title" not in result:
                raise ValueError(f"Could not find information for '{plant_name}'.")

            return {
                "title": str(result.get("title", f"{plant_name} Identified")),
                "summary": str(result.get("summary", "")),
                "severity": "healthy",
                "confidence": 99.0,
                "details": result.get("details", {}),
                "recommendations": str(result.get("recommendations", "")),
            }

        except json.JSONDecodeError as e:
            raise ValueError(f"AI returned an invalid response. Please try again.")
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep((2 ** attempt) * 2)
                continue
            raise ValueError(f"AI search failed: {e}")

    raise ValueError(f"AI search failed after retries: {last_error}")

# ---------------------------------------------------------------------------
# Google Gemini — Agro-Assistant Chat
# ---------------------------------------------------------------------------

def get_agro_advice(prompt, history=None):
    """
    Use Hugging Face API with an Open-Source LLM (Llama-3) and Personal Knowledge Base (RAG).
    """
    import os
    import requests
    from django.conf import settings

    api_key = getattr(settings, "HUGGINGFACE_API_KEY", "")
    if not api_key:
        return "⚠️ HUGGINGFACE_API_KEY is not configured. Please add your free Hugging Face API key to the .env file!"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_path = os.path.join(base_dir, 'agrobot_data', 'my_garden_knowledge.txt')

    # Read personal knowledge base
    personal_knowledge = ""
    if os.path.exists(knowledge_path):
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            personal_knowledge = f.read()

    system_instruction = f"""You are 'AgroBot', the expert AI assistant for the GREENGROW platform. 
    Your goal is to help the user with practical, sustainable, and scientific farming advice.
    Keep your answers concise, helpful, and supportive. Use bullet points for steps.
    
    IMPORTANT: You have been personally trained on the user's specific garden. Here is their garden profile:
    ---
    {personal_knowledge}
    ---
    Always prioritize this personal profile when giving advice!"""

    # Build messages list
    messages = [{"role": "system", "content": system_instruction}]
    
    if history:
        for msg in history:
            # history comes from the frontend as [{'text': '...', 'is_user': True/False}]
            role = "user" if msg.get('is_user') else "assistant"
            messages.append({"role": role, "content": msg.get('text', '')})
            
    messages.append({"role": "user", "content": prompt})

    # Hugging Face Chat Completions API
    # Using Llama-3-8B-Instruct as a powerful open-source conversational model
    api_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        elif response.status_code == 429:
            return "⚠️ Hugging Face API rate limit reached. Please wait a minute and try again."
        elif response.status_code == 401:
            return "⚠️ Invalid Hugging Face API Key. Please check your .env file."
        elif response.status_code == 503:
            # Model is loading (cold start)
            return "⏳ The AI model is currently loading on Hugging Face servers. Please wait about 30 seconds and ask again!"
        else:
            return f"⚠️ API Error ({response.status_code}): {response.text[:200]}"
            
    except requests.exceptions.Timeout:
        return "⚠️ Request to Hugging Face timed out. Please try again."
    except Exception as e:
        print(f"HuggingFace API Error: {e}")
        return f"I'm sorry, I encountered an error connecting to my AI brain: {e}"
