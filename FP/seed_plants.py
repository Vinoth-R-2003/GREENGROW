import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')
django.setup()

from garden.models import Plant

plants_data = [
    {
        "name": "Tomato",
        "description": "A popular juicy fruit often treated as a vegetable in cooking.",
        "uses": "Salads, sauces, soups, sandwiches, and fresh eating.",
        "how_to_grow": "Needs full sun and well-drained soil. Provide support with stakes or cages. Water consistently at the base.",
        "how_to_use": "Wash before use. Can be eaten raw or cooked in various dishes.",
        "image": "item_types/tomato.png"
    },
    {
        "name": "Carrot",
        "description": "A root vegetable, usually orange in color, though purple, black, red, white, and yellow cultivars exist.",
        "uses": "Raw snacks, salads, soups, stews, juices, and desserts like carrot cake.",
        "how_to_grow": "Sow seeds directly in loose, sandy soil. Requires consistent moisture and thinning of seedlings.",
        "how_to_use": "Peel or scrub clean. Can be eaten raw, boiled, roasted, or steamed.",
        "image": "item_types/carrot.png"
    },
    {
        "name": "Spinach",
        "description": "A leafy green flowering plant native to central and western Asia.",
        "uses": "Salads, smoothies, sautéed as a side dish, and in pastas.",
        "how_to_grow": "Prefers cool weather. Sow in rich, moist soil in partial shade to full sun.",
        "how_to_use": "Wash thoroughly to remove grit. Use raw or cook quickly.",
        "image": "item_types/spinach.png"
    },
    {
        "name": "Apple",
        "description": "A sweet, edible fruit produced by an apple tree (Malus domestica).",
        "uses": "Fresh eating, pies, juices, cider, and sauces.",
        "how_to_grow": "Requires cross-pollination with another apple variety. Prune annually and watch for pests.",
        "how_to_use": "Wash and eat fresh, or peel and core for cooking.",
        "image": "garden/plants/apple.png"
    },
    {
        "name": "Mango",
        "description": "A tropical stone fruit known as the 'king of fruits'.",
        "uses": "Fresh eating, smoothies, desserts, salsas, and chutneys.",
        "how_to_grow": "Thrives in warm, tropical climates with plenty of sun and well-draining soil.",
        "how_to_use": "Peel and slice away from the large flat pit.",
        "image": "garden/plants/mango.png"
    },
    {
        "name": "Potato",
        "description": "A starchy tuberous crop from the perennial nightshade Solanum tuberosum.",
        "uses": "Boiled, baked, fried, mashed, and in salads.",
        "how_to_grow": "Plant 'seed potatoes' in deep, loose soil. Hill the soil around the plants as they grow.",
        "how_to_use": "Wash and peel if desired. Must be cooked before eating.",
        "image": "item_types/potato.png"
    },
    {
        "name": "Strawberry",
        "description": "A widely grown hybrid species of the genus Fragaria.",
        "uses": "Fresh eating, desserts, jams, and smoothies.",
        "how_to_grow": "Requires full sun and well-drained soil rich in organic matter. Mulch with straw to keep fruit off the ground.",
        "how_to_use": "Wash and remove the green hull before eating.",
        "image": "garden/plants/strawberry.png"
    },
    {
        "name": "Broccoli",
        "description": "An edible green plant in the cabbage family whose large flowering head is eaten as a vegetable.",
        "uses": "Steamed, roasted, in stir-frys, and raw with dip.",
        "how_to_grow": "Cool-season crop. Prefers full sun and rich, moist soil.",
        "how_to_use": "Wash and cut into florets. Stems are also edible if peeled."
    },
    {
        "name": "Banana",
        "description": "An elongated, edible fruit – botanically a berry – produced by several kinds of large herbaceous flowering plants.",
        "uses": "Fresh eating, smoothies, baking (banana bread), and desserts.",
        "how_to_grow": "Requires a tropical climate with high humidity, plenty of water, and rich soil.",
        "how_to_use": "Peel and eat.",
        "image": "garden/plants/banana.png"
    },
    {
        "name": "Bell Pepper",
        "description": "Fruit of the species Capsicum annuum, available in green, red, yellow, and orange.",
        "uses": "Salads, stir-frys, stuffing, and roasting.",
        "how_to_grow": "Needs warm weather and full sun. Keep soil moist and well-fertilized.",
        "how_to_use": "Remove seeds and inner ribs before slicing."
    },
    {
        "name": "Onion",
        "description": "A vegetable that is the most widely cultivated species of the genus Allium.",
        "uses": "A staple base for soups, stews, stir-frys, and salads.",
        "how_to_grow": "Can be grown from seeds, sets, or transplants. Requires well-drained soil and weed control.",
        "how_to_use": "Peel the outer papery skin and chop or slice.",
        "image": "item_types/onion.png"
    },
    {
        "name": "Cucumber",
        "description": "A widely-cultivated creeping vine plant in the Cucurbitaceae gourd family.",
        "uses": "Salads, pickling, and fresh snacks.",
        "how_to_grow": "Needs full sun and plenty of water. Provide a trellis for climbing varieties.",
        "how_to_use": "Wash and slice. Some prefer peeling the skin."
    },
    {
        "name": "Grape",
        "description": "A fruit, botanically a berry, of the deciduous woody vines of the flowering plant genus Vitis.",
        "uses": "Fresh eating, raisins, juice, and jelly.",
        "how_to_grow": "Requires a sturdy trellis or arbor. Needs full sun and regular pruning.",
        "how_to_use": "Wash thoroughly and eat fresh."
    },
    {
        "name": "Watermelon",
        "description": "A flowering plant species of the Cucurbitaceae family and the name of its edible fruit.",
        "uses": "Fresh eating, juices, and fruit salads.",
        "how_to_grow": "Needs a long, warm growing season and lots of space for the vines to spread.",
        "how_to_use": "Cut into wedges or cubes."
    },
    {
        "name": "Lemon",
        "description": "A species of small evergreen tree in the flowering plant family Rutaceae.",
        "uses": "Flavoring, juices, zest, and garnishes.",
        "how_to_grow": "Thrives in warm, sunny climates. Can be grown in pots in cooler areas if moved indoors in winter.",
        "how_to_use": "Squeeze for juice or grate the skin for zest."
    },
    {
        "name": "Garlic",
        "description": "A species of bulbous flowering plant in the genus Allium.",
        "uses": "Flavoring in almost all savory cuisines.",
        "how_to_grow": "Plant cloves in the fall in well-drained soil. Requires a cold period to develop bulbs.",
        "how_to_use": "Peel individual cloves and mince or crush."
    },
    {
        "name": "Blueberry",
        "description": "Perennial flowering plants with blue or purple berries.",
        "uses": "Fresh eating, baking, jams, and smoothies.",
        "how_to_grow": "Requires acidic soil (pH 4.5-5.5). Best grown in full sun.",
        "how_to_use": "Wash gently before eating."
    },
    {
        "name": "Cabbage",
        "description": "A leafy green, red, or white biennial plant grown as an annual vegetable crop.",
        "uses": "Coleslaw, sauerkraut, stir-frys, and soups.",
        "how_to_grow": "Cool-weather crop. Requires consistent moisture and firm soil.",
        "how_to_use": "Remove outer leaves and slice or shred.",
        "image": "item_types/cabbage.png"
    },
    {
        "name": "Pineapple",
        "description": "A tropical plant with an edible fruit and the most economically significant plant in the family Bromeliaceae.",
        "uses": "Fresh eating, juices, desserts, and savory dishes (like pizza).",
        "how_to_grow": "Can be grown from the top of a store-bought pineapple. Needs warm temperatures and full sun.",
        "how_to_use": "Remove the tough outer skin and core."
    },
    {
        "name": "Basil",
        "description": "A culinary herb of the family Lamiaceae (mints).",
        "uses": "Pesto, salads, pasta dishes, and garnishes.",
        "how_to_grow": "Thrives in warm weather and full sun. Pinch off flower buds to encourage leafy growth.",
        "how_to_use": "Use fresh leaves for the best flavor; add at the end of cooking."
    },
    {
        "name": "Mint",
        "description": "A genus of plants in the family Lamiaceae, known for its aromatic leaves.",
        "uses": "Teas, cocktails (mojitos), desserts, and savory middle-eastern dishes.",
        "how_to_grow": "Very hardy and can be invasive; best grown in pots. Prefers moist soil and partial shade.",
        "how_to_use": "Pluck leaves as needed. Great fresh or dried."
    },
    {
        "name": "Rosemary",
        "description": "A woody, perennial herb with fragrant, evergreen, needle-like leaves.",
        "uses": "Seasoning for meats, roasted vegetables, and breads.",
        "how_to_grow": "Requires well-drained soil and full sun. It is drought-tolerant once established.",
        "how_to_use": "Strip the needles from the woody stem and chop finely."
    },
    {
        "name": "Dragon Fruit",
        "description": "The fruit of several different cactus species indigenous to the Americas.",
        "uses": "Fresh eating, smoothies, and decorative garnishes.",
        "how_to_grow": "A climbing cactus that needs support and a warm, tropical climate.",
        "how_to_use": "Slice in half and scoop out the speckled flesh with a spoon."
    },
    {
        "name": "Passion Fruit",
        "description": "A tropical fruit known for its intense aroma and tangy flavor.",
        "uses": "Juices, desserts, cocktails, and yogurt toppings.",
        "how_to_grow": "Grown on a vigorous climbing vine. Needs full sun and protection from strong winds.",
        "how_to_use": "Cut in half and scoop out the pulpy seeds."
    }
]

def seed_plants():
    print("Starting plant seeding with images...")
    count = 0
    for data in plants_data:
        plant, created = Plant.objects.update_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'uses': data['uses'],
                'how_to_grow': data['how_to_grow'],
                'how_to_use': data['how_to_use'],
                'image': data.get('image', '')
            }
        )
        if created:
            count += 1
            print(f"Added: {plant.name}")
        else:
            print(f"Updated: {plant.name}")
    
    print(f"Successfully processed {len(plants_data)} plants.")

if __name__ == "__main__":
    seed_plants()
