import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from market.models import Item

# Define the items and their image filenames (files located in static/img/item_types/)
items = {
    # Vegetables
    "Tomato": "tomato.png",
    "Potato": "potato.png",
    "Onion": "onion.png",
    "Carrot": "carrot.png",
    "Cabbage": "cabbage.png",
    "Spinach": "spinach.png",
    "Cauliflower": "cauliflower.png",
    "Brinjal": "brinjal.png",
    "Lady Finger": "lady_finger.png",
    "Pumpkin": "pumpkin.png",
    "Broccoli": "broccoli.png",
    "Bell Pepper": "bell_pepper.png",
    "Garlic": "garlic.png",
    "Ginger": "ginger.png",
    "Cucumber": "cucumber.png",
    "Radish": "radish.png",
    "Sweet Potato": "sweet_potato.png",
    "Corn": "corn.png",
    "Green Peas": "green_peas.png",
    "Mushroom": "mushroom.png",
    "Beetroot": "beetroot.png",
    "Capsicum": "capsicum.png",
    "Chilli": "chilli.png",
    
    # Fruits
    "Apple": "apple.png",
    "Mango": "mango.png",
    "Banana": "banana.png",
    "Strawberry": "strawberry.png",
    "Watermelon": "watermelon.png",
    "Grape": "grape.png",
    "Pineapple": "pineapple.png",
    "Lemon": "lemon.png",
    "Blueberry": "blueberry.png",
    "Papaya": "papaya.png",
    "Pomegranate": "pomegranate.png",
    "Orange": "orange.png",
    "Kiwi": "kiwi.png",
    "Guava": "guava.png",
    
    # Herbs
    "Basil": "Basil.jpg",
    "Mint": "Mint.jpg",
    "Coriander": "Coriander.jpg",
    "Curry Leaves": "Curry Leaves.jpg",
}

def seed_marketplace_items():
    print("Starting Marketplace item seeding...")
    count = 0
    for name, filename in items.items():
        item, created = Item.objects.get_or_create(name=name)
        if filename:
            # Check if file exists in static directory
            full_path = os.path.join('static', 'img', 'item_types', filename)
            if os.path.exists(full_path):
                item.image = filename
            else:
                print(f"[WARNING] Image not found in static: {full_path}")
        item.save()
        if created:
            count += 1
            print(f"Added: {name}")
        else:
            print(f"Updated: {name}")
    
    print(f"Successfully processed {len(items)} items for the Marketplace.")

if __name__ == "__main__":
    seed_marketplace_items()
