import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from market.models import Item

# Define items with category and filename
items_data = [
    # Vegetables
    {"name": "Tomato", "filename": "tomato.png", "category": "Vegetables"},
    {"name": "Potato", "filename": "potato.png", "category": "Vegetables"},
    {"name": "Onion", "filename": "onion.png", "category": "Vegetables"},
    {"name": "Carrot", "filename": "carrot.png", "category": "Vegetables"},
    {"name": "Cabbage", "filename": "cabbage.png", "category": "Vegetables"},
    {"name": "Spinach", "filename": "spinach.png", "category": "Vegetables"},
    {"name": "Cauliflower", "filename": "cauliflower.png", "category": "Vegetables"},
    {"name": "Brinjal", "filename": "brinjal.png", "category": "Vegetables"},
    {"name": "Lady Finger", "filename": "lady_finger.png", "category": "Vegetables"},
    {"name": "Pumpkin", "filename": "pumpkin.png", "category": "Vegetables"},
    {"name": "Broccoli", "filename": "broccoli.png", "category": "Vegetables"},
    {"name": "Bell Pepper", "filename": "bell_pepper.png", "category": "Vegetables"},
    {"name": "Garlic", "filename": "garlic.png", "category": "Vegetables"},
    {"name": "Ginger", "filename": "ginger.png", "category": "Vegetables"},
    {"name": "Cucumber", "filename": "cucumber.png", "category": "Vegetables"},
    {"name": "Radish", "filename": "radish.png", "category": "Vegetables"},
    {"name": "Sweet Potato", "filename": "sweet_potato.png", "category": "Vegetables"},
    {"name": "Corn", "filename": "corn.png", "category": "Vegetables"},
    {"name": "Green Peas", "filename": "green_peas.png", "category": "Vegetables"},
    {"name": "Mushroom", "filename": "mushroom.png", "category": "Vegetables"},
    {"name": "Beetroot", "filename": "beetroot.png", "category": "Vegetables"},
    {"name": "Capsicum", "filename": "capsicum.png", "category": "Vegetables"},
    {"name": "Chilli", "filename": "chilli.png", "category": "Vegetables"},

    # Fruits
    {"name": "Apple", "filename": "apple.png", "category": "Fruits"},
    {"name": "Mango", "filename": "mango.png", "category": "Fruits"},
    {"name": "Banana", "filename": "banana.png", "category": "Fruits"},
    {"name": "Strawberry", "filename": "strawberry.png", "category": "Fruits"},
    {"name": "Watermelon", "filename": "watermelon.png", "category": "Fruits"},
    {"name": "Grape", "filename": "grape.png", "category": "Fruits"},
    {"name": "Pineapple", "filename": "pineapple.png", "category": "Fruits"},
    {"name": "Lemon", "filename": "lemon.png", "category": "Fruits"},
    {"name": "Blueberry", "filename": "blueberry.png", "category": "Fruits"},
    {"name": "Papaya", "filename": "papaya.png", "category": "Fruits"},
    {"name": "Pomegranate", "filename": "pomegranate.png", "category": "Fruits"},
    {"name": "Orange", "filename": "orange.png", "category": "Fruits"},
    {"name": "Kiwi", "filename": "kiwi.png", "category": "Fruits"},
    {"name": "Guava", "filename": "guava.png", "category": "Fruits"},

    # Herbs
    {"name": "Basil", "filename": "Basil.jpg", "category": "Herbs"},
    {"name": "Mint", "filename": "Mint.jpg", "category": "Herbs"},
    {"name": "Coriander", "filename": "Coriander.jpg", "category": "Herbs"},
    {"name": "Curry Leaves", "filename": "Curry Leaves.jpg", "category": "Herbs"},
]

def seed_marketplace_items():
    print("Starting Marketplace item seeding...")
    count = 0
    for entry in items_data:
        name = entry["name"]
        filename = entry["filename"]
        cat = entry["category"]
        
        item, created = Item.objects.get_or_create(name=name)
        item.category = cat
        if filename:
            full_path = os.path.join('static', 'img', 'item_types', filename)
            if os.path.exists(full_path):
                item.image = filename
            else:
                print(f"[WARNING] Image not found in static: {full_path}")
        item.save()
        if created:
            count += 1
            print(f"Added [{cat}]: {name}")
        else:
            print(f"Updated [{cat}]: {name}")
    
    print(f"Successfully processed {len(items_data)} items for the Marketplace.")

if __name__ == "__main__":
    seed_marketplace_items()
