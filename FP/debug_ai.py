import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()
from checks.ai_checks import analyze_plant_image
import traceback

try:
    print(analyze_plant_image(r"x:\FP\media\post_images\tomato_farm.png", "disease"))
except Exception as e:
    traceback.print_exc()
