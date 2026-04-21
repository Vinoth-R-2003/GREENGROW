import os
import sys
import django

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from garden.models import Plant, UserPlant, PlantJournal
from market.models import Item, Product
from feed.models import Post, Comment
from chat.models import Message, CallLog

User = get_user_model()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# Users
print_section("USERS")
users = User.objects.all()
print(f"Total Users: {users.count()}\n")
for user in users[:10]:  # Show first 10
    print(f"ID: {user.id} | Username: {user.username} | Email: {user.email}")
    if hasattr(user, 'location') and user.location:
        print(f"  Location: {user.location}")
    print()

# Garden Plants
print_section("GARDEN - PLANTS")
plants = Plant.objects.all()
print(f"Total Plants: {plants.count()}\n")
for plant in plants[:10]:
    print(f"ID: {plant.id} | Name: {plant.name}")
    desc = plant.description[:80] if len(plant.description) > 80 else plant.description
    print(f"  Description: {desc}...")
    print()

# User Plants
print_section("GARDEN - USER PLANTS")
user_plants = UserPlant.objects.all()
print(f"Total User Plants: {user_plants.count()}\n")
for up in user_plants[:10]:
    print(f"User: {up.user.username} | Plant: {up.plant.name}")
    print(f"  Status: {up.status} | Planted: {up.date_planted.strftime('%Y-%m-%d')}")
    if up.notes:
        notes = up.notes[:60] if len(up.notes) > 60 else up.notes
        print(f"  Notes: {notes}...")
    print()

# Plant Journals
print_section("GARDEN - PLANT JOURNALS")
journals = PlantJournal.objects.all()
print(f"Total Plant Journals: {journals.count()}\n")
for journal in journals[:5]:
    print(f"User: {journal.user_plant.user.username} | Plant: {journal.user_plant.plant.name}")
    print(f"  Title: {journal.title}")
    content = journal.content[:80] if len(journal.content) > 80 else journal.content
    print(f"  Content: {content}...")
    print(f"  Date: {journal.entry_date.strftime('%Y-%m-%d')}")
    print()

# Market Items
print_section("MARKET - ITEMS")
items = Item.objects.all()
print(f"Total Items: {items.count()}\n")
for item in items[:10]:
    print(f"ID: {item.id} | Name: {item.name}")
    print()

# Market Products
print_section("MARKET - PRODUCTS")
products = Product.objects.all()
print(f"Total Products: {products.count()}\n")
for product in products[:10]:
    print(f"Seller: {product.seller.username} | Item: {product.item.name}")
    print(f"  Price: ${product.price} {product.unit} | Quantity: {product.quantity}")
    print(f"  Available: {'Yes' if product.is_available else 'No'}")
    if product.description:
        desc = product.description[:60] if len(product.description) > 60 else product.description
        print(f"  Description: {desc}...")
    print()

# Feed Posts
print_section("FEED - POSTS")
posts = Post.objects.all()
print(f"Total Posts: {posts.count()}\n")
for post in posts[:5]:
    print(f"User: {post.author.username}")
    # Handle content safely
    try:
        content = post.content[:100] if len(post.content) > 100 else post.content
        print(f"  Content: {content}...")
    except:
        print(f"  Content: [Contains special characters]")
    print(f"  Likes: {post.likes.count()} | Comments: {post.comments.count()}")
    print(f"  Created: {post.created_at.strftime('%Y-%m-%d %H:%M')}")
    print()

# Comments
print_section("FEED - COMMENTS")
comments = Comment.objects.all()
print(f"Total Comments: {comments.count()}\n")
for comment in comments[:5]:
    print(f"User: {comment.author.username} on Post by {comment.post.author.username}")
    try:
        content = comment.content[:80] if len(comment.content) > 80 else comment.content
        print(f"  Comment: {content}...")
    except:
        print(f"  Comment: [Contains special characters]")
    print(f"  Created: {comment.created_at.strftime('%Y-%m-%d %H:%M')}")
    print()

# Messages
print_section("CHAT - MESSAGES")
messages = Message.objects.all()
print(f"Total Messages: {messages.count()}\n")
for msg in messages[:5]:
    print(f"From: {msg.sender.username} → To: {msg.recipient.username}")
    try:
        content = msg.content[:80] if len(msg.content) > 80 else msg.content
        print(f"  Message: {content}...")
    except:
        print(f"  Message: [Contains special characters]")
    print(f"  Sent: {msg.timestamp.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Read: {'Yes' if msg.is_read else 'No'}")
    print()

# Call Logs
print_section("CHAT - CALL LOGS")
call_logs = CallLog.objects.all()
print(f"Total Call Logs: {call_logs.count()}\n")
for call in call_logs[:5]:
    print(f"From: {call.caller.username} → To: {call.receiver.username}")
    print(f"  Type: {call.call_type.title()} | Status: {call.status}")
    if call.duration:
        print(f"  Duration: {call.duration}s")
    print(f"  Started: {call.started_at.strftime('%Y-%m-%d %H:%M')}")
    print()

print("\n" + "="*60)
print("  DATABASE SUMMARY")
print("="*60)
print(f"Users: {User.objects.count()}")
print(f"Plants: {Plant.objects.count()}")
print(f"User Plants: {UserPlant.objects.count()}")
print(f"Plant Journals: {PlantJournal.objects.count()}")
print(f"Items: {Item.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Posts: {Post.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
print(f"Messages: {Message.objects.count()}")
print(f"Call Logs: {CallLog.objects.count()}")
print("="*60 + "\n")
