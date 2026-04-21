import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from market.models import Item

items = {
    "Tomato": "item_types/tomato.png",
    "Potato": "item_types/potato.png",
    "Onion": "item_types/onion.png",
    "Carrot": "item_types/carrot.png",
    "Cabbage": "item_types/cabbage.png",
    "Spinach": "item_types/spinach.png",
    "Cauliflower": "item_types/cauliflower.png",
    "Brinjal": "item_types/brinjal.png",
    "Lady Finger": "item_types/lady_finger.png",
    "Pumpkin": "item_types/pumpkin.png",
}

for name, image_path in items.items():
    item, created = Item.objects.get_or_create(name=name)
    item.image = image_path
    item.save()

print(f"Seeded {len(items)} items with images.")
