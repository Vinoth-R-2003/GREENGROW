import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from market.models import Item

# Define the items and their image paths (if available)
items = {
    # Existing ones
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
    
    # New Fruits (using generated images from garden if available, or just names)
    "Apple": "garden/plants/apple.png",
    "Mango": "garden/plants/mango.png",
    "Banana": "garden/plants/banana.png",
    "Strawberry": "garden/plants/strawberry.png",
    "Watermelon": "",
    "Grape": "",
    "Pineapple": "",
    "Lemon": "",
    "Blueberry": "",
    "Papaya": "",
    "Pomegranate": "",
    "Orange": "",
    "Kiwi": "",
    "Guava": "",
    
    # New Vegetables
    "Broccoli": "",
    "Bell Pepper": "",
    "Garlic": "",
    "Ginger": "",
    "Cucumber": "",
    "Radish": "",
    "Sweet Potato": "",
    "Corn": "",
    "Green Peas": "",
    "Mushroom": "",
    "Beetroot": "",
    "Capsicum": "",
    "Chilli": "",
    
    # Herbs
    "Basil": "",
    "Mint": "",
    "Coriander": "",
    "Curry Leaves": "",
}

def seed_marketplace_items():
    print("Starting Marketplace item seeding...")
    count = 0
    for name, image_path in items.items():
        item, created = Item.objects.get_or_create(name=name)
        if image_path:
            item.image = image_path
        item.save()
        if created:
            count += 1
            print(f"Added: {name}")
        else:
            print(f"Updated: {name}")
    
    print(f"Successfully processed {len(items)} items for the Marketplace.")

if __name__ == "__main__":
    seed_marketplace_items()
