import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from market.models import Item

# Define the items and their image paths (relative to media/)
items = {
    # Vegetables
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
    "Broccoli": "item_types/broccoli.png",
    "Bell Pepper": "item_types/bell_pepper.png",
    "Garlic": "item_types/garlic.png",
    "Ginger": "item_types/ginger.png",
    "Cucumber": "item_types/cucumber.png",
    "Radish": "item_types/radish.png",
    "Sweet Potato": "item_types/sweet_potato.png",
    "Corn": "item_types/corn.png",
    "Green Peas": "item_types/green_peas.png",
    "Mushroom": "item_types/mushroom.png",
    "Beetroot": "item_types/beetroot.png",
    "Capsicum": "item_types/capsicum.png",
    "Chilli": "item_types/chilli.png",
    
    # Fruits
    "Apple": "item_types/apple.png",
    "Mango": "item_types/mango.png",
    "Banana": "item_types/banana.png",
    "Strawberry": "item_types/strawberry.png",
    "Watermelon": "item_types/watermelon.png",
    "Grape": "item_types/grape.png",
    "Pineapple": "item_types/pineapple.png",
    "Lemon": "item_types/lemon.png",
    "Blueberry": "item_types/blueberry.png",
    "Papaya": "item_types/papaya.png",
    "Pomegranate": "item_types/pomegranate.png",
    "Orange": "item_types/orange.png",
    "Kiwi": "item_types/kiwi.png",
    "Guava": "item_types/guava.png",
    
    # Herbs
    "Basil": "item_types/Basil.jpg",
    "Mint": "item_types/Mint.jpg",
    "Coriander": "item_types/Coriander.jpg",
    "Curry Leaves": "item_types/Curry Leaves.jpg",
}

def seed_marketplace_items():
    print("Starting Marketplace item seeding...")
    count = 0
    for name, image_path in items.items():
        item, created = Item.objects.get_or_create(name=name)
        if image_path:
            # Check if file exists to avoid broken links
            full_path = os.path.join('media', image_path)
            if os.path.exists(full_path):
                item.image = image_path
            else:
                print(f"[WARNING] Image not found: {full_path}")
        item.save()
        if created:
            count += 1
            print(f"Added: {name}")
        else:
            print(f"Updated: {name}")
    
    print(f"Successfully processed {len(items)} items for the Marketplace.")

if __name__ == "__main__":
    seed_marketplace_items()
