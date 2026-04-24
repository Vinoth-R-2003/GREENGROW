from google import genai
from django.conf import settings
from datetime import date, timedelta
import json
import re
import time

def get_fallback_tasks(plant_name):
    """Returns a generic, reliable care schedule if the AI API fails."""
    from datetime import date, timedelta
    today = date.today()
    return [
        {
            'task_type': 'Watering',
            'notes': f'Check soil moisture for {plant_name}. Water deeply if the top inch is dry.',
            'due_date': today,
            'recurrence_days': 3,
        },
        {
            'task_type': 'Fertilizing',
            'notes': f'Apply a balanced liquid fertilizer to {plant_name}.',
            'due_date': today + timedelta(days=14),
            'recurrence_days': 30,
        },
        {
            'task_type': 'Pruning',
            'notes': f'Inspect {plant_name} and remove any dead or yellowing leaves.',
            'due_date': today + timedelta(days=7),
            'recurrence_days': 14,
        },
        {
            'task_type': 'Pest Control',
            'notes': 'Check under leaves and along stems for early signs of pests.',
            'due_date': today + timedelta(days=5),
            'recurrence_days': 7,
        },
        {
            'task_type': 'Other',
            'notes': 'Check overall plant health and ensure it receives adequate sunlight.',
            'due_date': today + timedelta(days=2),
            'recurrence_days': 14,
        }
    ]


def generate_ai_tasks(plant_name, plant_description, how_to_grow):
    """
    Use Google Gemini AI to generate care tasks for a plant.
    Returns a list of task dictionaries.
    Uses the new google-genai SDK with built-in retry logic.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in settings.")

    client = genai.Client(api_key=api_key)

    today = date.today().isoformat()

    prompt = f"""You are an expert gardener assistant. Based on the following plant information, generate a list of care tasks and reminders.

Plant Name: {plant_name}
Plant Description: {plant_description}
How to Grow: {how_to_grow}
Today's Date: {today}

Generate exactly 5 care tasks. For each task, provide:
- task_type: One of "Watering", "Fertilizing", "Pruning", "Pest Control", or "Other"
- notes: A brief, helpful description of what to do (1-2 sentences)
- due_days_from_now: Number of days from today when this task should first be done (integer, 0-30)
- recurrence_days: How often to repeat this task in days (integer, or null if one-time)

Respond ONLY with a valid JSON array. No markdown, no explanation. Example format:
[
  {{"task_type": "Watering", "notes": "Water deeply at the base.", "due_days_from_now": 0, "recurrence_days": 2}},
  {{"task_type": "Fertilizing", "notes": "Apply balanced fertilizer.", "due_days_from_now": 7, "recurrence_days": 14}}
]"""

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
            )
            text = response.text.strip()

            # Remove markdown code fences if present
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            text = text.strip()

            tasks_data = json.loads(text)

            # Validate and convert
            valid_types = ['Watering', 'Fertilizing', 'Pruning', 'Pest Control', 'Other']
            result = []

            for task in tasks_data:
                task_type = task.get('task_type', 'Other')
                if task_type not in valid_types:
                    task_type = 'Other'

                due_days = int(task.get('due_days_from_now', 0))
                recurrence = task.get('recurrence_days')
                if recurrence is not None:
                    recurrence = int(recurrence)

                result.append({
                    'task_type': task_type,
                    'notes': str(task.get('notes', '')),
                    'due_date': date.today() + timedelta(days=due_days),
                    'recurrence_days': recurrence,
                })

            return result

        except json.JSONDecodeError as e:
            last_error = e
            # Don't retry JSON errors from the same response
            raise ValueError(f"AI returned invalid response. Please try again. Error: {e}")
        except Exception as e:
            last_error = e
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "resource" in error_str.lower():
                if attempt < max_retries - 1:
                    # Wait before retrying (exponential backoff)
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    time.sleep(wait_time)
                    continue
                # API is completely exhausted -> Trigger Fallback
                return get_fallback_tasks(plant_name)
            
            # For any other fatal error, also trigger the fallback instead of crashing
            if attempt == max_retries - 1:
                return get_fallback_tasks(plant_name)

    # Absolute ultimate fallback
    return get_fallback_tasks(plant_name)
