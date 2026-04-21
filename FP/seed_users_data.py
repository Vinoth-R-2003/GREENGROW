import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from feed.models import Post
from market.models import Product, Item

User = get_user_model()

# Data Definitions
users_data = [
    {
        "username": "VINOTH",
        "is_farmer": True,
        "location": "Salem, Tamil Nadu",
        "bio": "Passionate farmer specializing in organic vegetables.",
        "latitude": 11.6643,
        "longitude": 78.1460
    },
    {
        "username": "AJITH",
        "is_farmer": True,
        "location": "Erode, Tamil Nadu",
        "bio": "Bringing fresh produce directly from farm to table.",
        "latitude": 11.3410,
        "longitude": 77.7172
    },
    {
        "username": "MUNI",
        "is_farmer": True,
        "location": "Coimbatore, Tamil Nadu",
        "bio": "Expert in seasonal crops and sustainable farming.",
        "latitude": 11.0168,
        "longitude": 76.9558
    },
    {
        "username": "PRUDHVI",
        "is_farmer": True,
        "location": "Madurai, Tamil Nadu",
        "bio": "Dedicated to high-quality yield and customer satisfaction.",
        "latitude": 9.9252,
        "longitude": 78.1198
    }
]

sample_posts = [
    {"content": "Just harvested a fresh batch of tomatoes! 🍅 #fresh #organic", "image": "post_images/tomato_farm.png"},
    {"content": "Rainy days are good for the crops. 🌱", "image": "post_images/sunrise.png"},
    {"content": "Check out my new listing for potatoes. Best price in the market!", "image": "post_images/harvest.png"},
    {"content": "Farming is not just a job, it's a way of life. 🚜", "image": "post_images/farmer_market.png"},
    {"content": "Beautiful sunrise at the farm today. ☀️", "image": "post_images/sunrise.png"},
    {"content": "Preparing the soil for the next season.", "image": None},
    {"content": "Support local farmers! Buy fresh.", "image": "post_images/harvest.png"},
    {"content": "Healthy eating starts with healthy produce.", "image": "post_images/farmer_market.png"}
]

# Ensure we have items to sell
items = Item.objects.all()
if not items.exists():
    print("No items found in database. Please run seed_items.py first.")
    exit()

def seed_data():
    print("Seeding users, posts, and products...")
    
    for user_data in users_data:
        username = user_data["username"]
        # Create or Get User
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password("password123") # Default password
            user.is_farmer = user_data["is_farmer"]
            user.location = user_data["location"]
            user.bio = user_data["bio"]
            user.latitude = user_data["latitude"]
            user.longitude = user_data["longitude"]
            user.save()
            print(f"Created user: {username}")
        else:
            print(f"User {username} already exists.")

        # Create Posts (2-3 per user)
        # Delete existing posts to avoid duplicates for this test script
        user.posts.all().delete()
        
        for _ in range(random.randint(2, 3)):
            post_data = random.choice(sample_posts)
            Post.objects.create(author=user, content=post_data["content"], image=post_data["image"])
        
        # Create Products (2-4 per user)
        # Shuffle items to give random products to each user
        user.products.all().delete()
        user_items = random.sample(list(items), k=random.randint(2, 4))
        
        for item in user_items:
            price = round(random.uniform(20.0, 80.0), 2)
            Product.objects.create(
                seller=user,
                item=item,
                description=f"Fresh {item.name} from {user.location}.",
                price=price,
                unit="per kg",
                quantity=random.randint(10, 100),
                is_available=True
            )
            
    print("Seeding complete!")

if __name__ == "__main__":
    seed_data()
