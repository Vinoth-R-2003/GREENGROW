from django.core.management.base import BaseCommand
from garden.models import Plant

class Command(BaseCommand):
    help = 'Populates the Garden module with initial plant data'

    def handle(self, *args, **kwargs):
        plants = [
            {
                "name": "Tomato",
                "description": "The tomato is the edible, often red, berry of the plant Solanum lycopersicum, commonly known as a tomato plant. It is a staple in many cuisines worldwide.",
                "uses": "Tomatoes are excellent in salads, sauces, soups, and sandwiches. They can be preserved by drying or canning. Rich in lycopene and Vitamin C, they offer great health benefits.",
                "how_to_grow": "Plant in full sun with well-draining soil. Start seeds indoors 6-8 weeks before the last frost. Transplant when soil is warm, spacing plants 2-3 feet apart. Water regularly and provide support with cages or stakes.",
                "how_to_use": "Wash thoroughly before eating fresh. For cooking, they can be chopped, pureed, or roasted. Remove seeds if desired for smoother sauces.",
                "image": "garden/plants/tomato.png"
            },
            {
                "name": "Potato",
                "description": "The potato is a starchy tuber of the plant Solanum tuberosum and is a root vegetable native to the Americas.",
                "uses": "Potatoes are versatile and can be baked, boiled, mashed, fried, or roasted. They are a primary source of carbohydrates.",
                "how_to_grow": "Plant seed potatoes in early spring in loose, well-drained soil. Bury them about 4 inches deep and 12 inches apart. Hill up soil around the stems as they grow to encourage more tubers.",
                "how_to_use": "Scrub clean before cooking. Peel if desired, though skins contain nutrients. Store in a cool, dark place to prevent sprouting.",
                "image": "garden/plants/potato.png"
            },
            {
                "name": "Carrot",
                "description": "The carrot (Daucus carota subsp. sativus) is a root vegetable, usually orange in color, though purple, black, red, white, and yellow cultivars exist.",
                "uses": "Carrots can be eaten raw as a snack, added to salads, or cooked in soups and stews. They are famously good for eye health due to high beta-carotene content.",
                "how_to_grow": "Sow seeds directly into the garden in deep, loose soil free of stones. Thin seedlings to 3 inches apart. Keep soil moist for germination. Harvest when tops are about an inch in diameter.",
                "how_to_use": "Wash and peel (if skin is tough). Eat raw with dip, julienne for salads, or roast with honey and herbs.",
                "image": "garden/plants/carrot.png"
            },
            {
                "name": "Spinach",
                "description": "Spinach (Spinacia oleracea) is a leafy green flowering plant native to central and western Asia. It is loaded with nutrients and antioxidants.",
                "uses": "Use fresh leaves in salads or sandwiches. Cooked spinach is great in quiches, pasta dishes, and soups.",
                "how_to_grow": "Sow seeds in cool weather (early spring or late summer). It prefers full sun to partial shade and nitrogen-rich soil. Harvest outer leaves regularly to prolong production.",
                "how_to_use": "Rinse thoroughly to remove grit. Sauté lightly with garlic and olive oil, or steam for a minute to wilt."
            },
            {
                "name": "Lettuce",
                "description": "Lettuce (Lactuca sativa) is an annual plant of the daisy family, Asteraceae. It is most often grown as a leaf vegetable, but sometimes for its stem and seeds.",
                "uses": "The foundation of most salads. Can also be used in wraps or as a garnish. Different varieties bring texture and color to dishes.",
                "how_to_grow": "Sow seeds thinly in rows. Lettuce loves cool weather and consistent moisture. Mulch to keep soil cool. Harvest leaves as needed or cut the whole head.",
                "how_to_use": "Wash leaves and dry well using a salad spinner. Tear by hand rather than cutting to prevent browning if storing for later."
            },
            {
                "name": "Cucumber",
                "description": "Cucumber (Cucumis sativus) is a widely-cultivated creeping vine plant in the Cucurbitaceae gourd family that bears usually cylindrical fruits.",
                "uses": "Perfect for pickling or slicing fresh into salads. They add a refreshing crunch to sandwiches and water.",
                "how_to_grow": "Plant in warm soil after frost danger has passed. Needs fertile soil and regular water. Vines may need trellising. Harvest often to encourage more fruit.",
                "how_to_use": "Wash well. Peel if the skin is thick or waxed. Slice for salads or cut into spears for pickling."
            },
            {
                "name": "Bell Pepper",
                "description": "Bell pepper (also known as sweet pepper, pepper, or capsicum) is the fruit of plants in the Grossum cultivar group of the species Capsicum annuum.",
                "uses": "Great raw in salads or with dip. Cooked, they are essential in fajitas, stir-fries, and stuffed pepper recipes.",
                "how_to_grow": "Start seeds indoors or buy transplants. Plant in a sunny spot with warm soil. Keep watered but not soggy. Support heavy fruiting branches.",
                "how_to_use": "Remove the stem and seeds. Slice into strips or dice. Roasting them brings out sweetness and makes skin easy to peel."
            },
            {
                "name": "Onion",
                "description": "The onion (Allium cepa), also known as the bulb onion or common onion, is a vegetable that is the most widely cultivated species of the genus Allium.",
                "uses": "A fundamental ingredient in almost every cuisine for base flavor. Can be caramelized, fried, pickled, or eaten raw in salads.",
                "how_to_grow": "Plant sets or seeds in early spring. They need full sun and well-drained soil. Keep weed-free. Stop watering when tops fall over before harvesting.",
                "how_to_use": "Peel the outer papery skin. Chop or slice as needed. Chilling onions before cutting can reduce eye irritation."
            },
            {
                "name": "Garlic",
                "description": "Garlic (Allium sativum) is a species of bulbous flowering plant in the genus Allium. Its close relatives include the onion, shallot, leek, chive, and Chinese onion.",
                "uses": "Used primarily as a seasoning or condiment. Roasted garlic spreads like butter and has a milder flavor.",
                "how_to_grow": "Plant cloves in the fall for harvest the next summer. Plant point side up, 2 inches deep. Needs cold period to form bulbs.",
                "how_to_use": "Crush, mince, or slice cloves. Sauté briefly do not burn or it becomes bitter. Add late in cooking for stronger flavor."
            },
            {
                "name": "Basil",
                "description": "Basil (Ocimum basilicum), also called sweet basil, is a culinary herb of the family Lamiaceae (mints).",
                "uses": "Essential for pesto, caprese salad, and tomato sauces. Adds fresh aromatic flavor to pizzas and pastas.",
                "how_to_grow": "Plant in warm soil and full sun. Pinch off flower buds to encourage bushy leaf growth. Very sensitive to frost.",
                "how_to_use": "Rinse gently. Add fresh at the end of cooking to preserve flavor. Freeze in oil or dry for long-term storage."
            }
        ]

        self.stdout.write('Starting plant population...')

        for plant_data in plants:
            plant, created = Plant.objects.update_or_create(
                name=plant_data['name'],
                defaults=plant_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created plant: {plant.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated plant: {plant.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated plant data'))
