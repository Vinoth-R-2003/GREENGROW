import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from garden.models import Plant, UserPlant, PlantJournal
from market.models import Item, Product
from feed.models import Post, Comment
from chat.models import Message, CallLog

User = get_user_model()

# Get table name from command line argument
if len(sys.argv) < 2:
    print("\nUsage: python show_table.py <table_name>")
    print("\nAvailable tables:")
    print("  users       - View all users")
    print("  plants      - View all plants")
    print("  userplants  - View user's garden plants")
    print("  journals    - View plant journals")
    print("  items       - View market items")
    print("  products    - View market products")
    print("  posts       - View feed posts")
    print("  comments    - View comments")
    print("  messages    - View chat messages")
    print("  calls       - View call logs")
    print("\nExample: python show_table.py users")
    sys.exit(0)

table = sys.argv[1].lower()

if table == 'users':
    print("\n" + "="*80)
    print("USERS TABLE")
    print("="*80)
    for user in User.objects.all():
        print(f"ID: {user.id:3d} | Username: {user.username:15s} | Email: {user.email:30s} | Location: {user.location if hasattr(user, 'location') and user.location else 'N/A'}")

elif table == 'plants':
    print("\n" + "="*80)
    print("PLANTS TABLE")
    print("="*80)
    for plant in Plant.objects.all():
        print(f"ID: {plant.id:3d} | Name: {plant.name}")

elif table == 'userplants':
    print("\n" + "="*80)
    print("USER PLANTS TABLE")
    print("="*80)
    for up in UserPlant.objects.all():
        print(f"User: {up.user.username:15s} | Plant: {up.plant.name:20s} | Status: {up.status:10s} | Planted: {up.date_planted}")

elif table == 'journals':
    print("\n" + "="*80)
    print("PLANT JOURNALS TABLE")
    print("="*80)
    for journal in PlantJournal.objects.all():
        print(f"User: {journal.user_plant.user.username:15s} | Plant: {journal.user_plant.plant.name:20s} | Title: {journal.title}")

elif table == 'items':
    print("\n" + "="*80)
    print("MARKET ITEMS TABLE")
    print("="*80)
    for item in Item.objects.all():
        print(f"ID: {item.id:3d} | Name: {item.name}")

elif table == 'products':
    print("\n" + "="*80)
    print("MARKET PRODUCTS TABLE")
    print("="*80)
    for product in Product.objects.all():
        print(f"Seller: {product.seller.username:15s} | Item: {product.item.name:15s} | Price: ${product.price:6.2f} | Qty: {product.quantity:3d} | Available: {product.is_available}")

elif table == 'posts':
    print("\n" + "="*80)
    print("FEED POSTS TABLE")
    print("="*80)
    for post in Post.objects.all():
        content = post.content[:50] + "..." if len(post.content) > 50 else post.content
        print(f"User: {post.author.username:15s} | Content: {content} | Likes: {post.likes.count()} | Comments: {post.comments.count()}")

elif table == 'comments':
    print("\n" + "="*80)
    print("COMMENTS TABLE")
    print("="*80)
    for comment in Comment.objects.all():
        print(f"User: {comment.author.username:15s} | Post by: {comment.post.author.username:15s} | Comment: {comment.content[:50]}")

elif table == 'messages':
    print("\n" + "="*80)
    print("CHAT MESSAGES TABLE")
    print("="*80)
    for msg in Message.objects.all():
        print(f"From: {msg.sender.username:15s} → To: {msg.recipient.username:15s} | Message: {msg.content[:50]} | Read: {msg.is_read}")

elif table == 'calls':
    print("\n" + "="*80)
    print("CALL LOGS TABLE")
    print("="*80)
    if CallLog.objects.count() == 0:
        print("No call logs found.")
    else:
        for call in CallLog.objects.all():
            print(f"From: {call.caller.username:15s} → To: {call.receiver.username:15s} | Type: {call.call_type} | Status: {call.status}")

else:
    print(f"\nError: Unknown table '{table}'")
    print("Run 'python show_table.py' to see available tables.")

print()
