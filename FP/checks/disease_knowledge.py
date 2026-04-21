"""
Disease Knowledge Base for the 38 PlantVillage Classes.

Each entry maps a class name to structured information about the plant,
disease (if any), severity, symptoms, treatment recommendations, and
yield impact.
"""

# The 38 class names exactly as they appear in the training data
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
]

# Comprehensive knowledge base for each class
DISEASE_DATABASE = {
    'Apple___Apple_scab': {
        'plant': 'Apple',
        'disease_name': 'Apple Scab',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Olive-green or brown spots on leaves',
            'Velvety or scab-like lesions on fruit',
            'Premature leaf drop',
            'Distorted or cracked fruit',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Twigs'],
        'spread_risk': 'High',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply fungicide (captan or myclobutanil) at regular intervals during spring\n"
            "2. Remove and destroy fallen leaves to reduce fungal spore load\n"
            "3. Prune trees to improve air circulation\n"
            "4. Choose scab-resistant apple varieties for future planting\n"
            "5. Avoid overhead irrigation to keep foliage dry"
        ),
    },
    'Apple___Black_rot': {
        'plant': 'Apple',
        'disease_name': 'Black Rot',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Brown-to-black expanding lesions on fruit',
            'Frogeye leaf spots with purple borders',
            'Cankers on branches',
            'Mummified fruit on tree',
        ],
        'affected_parts': ['Fruit', 'Leaves', 'Branches'],
        'spread_risk': 'High',
        'stage': 'Advanced',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Remove and destroy all mummified fruits and infected branches\n"
            "2. Apply copper-based fungicides during dormant season\n"
            "3. Maintain good sanitation practices around the orchard\n"
            "4. Prune cankers at least 15 inches below visible infection\n"
            "5. Ensure proper tree nutrition to boost natural resistance"
        ),
    },
    'Apple___Cedar_apple_rust': {
        'plant': 'Apple',
        'disease_name': 'Cedar Apple Rust',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Bright orange-yellow spots on leaves',
            'Small raised spots on fruit',
            'Tube-like structures on leaf undersides',
            'Premature defoliation in severe cases',
        ],
        'affected_parts': ['Leaves', 'Fruit'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Average',
        'yield_potential': 'Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Remove nearby cedar or juniper trees (alternate host) within a 2-mile radius\n"
            "2. Apply myclobutanil or mancozeb fungicide from pink bud stage through petal fall\n"
            "3. Plant rust-resistant apple varieties\n"
            "4. Maintain proper tree spacing for adequate air circulation\n"
            "5. Monitor weather conditions — infections increase in warm, wet springs"
        ),
    },
    'Apple___healthy': {
        'plant': 'Apple',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Continue regular watering and balanced fertilization\n"
            "2. Maintain a preventive fungicide spray schedule during growing season\n"
            "3. Prune annually to encourage air circulation and light penetration\n"
            "4. Monitor for early signs of pests and diseases\n"
            "5. Apply mulch to conserve moisture and suppress weeds"
        ),
    },
    'Blueberry___healthy': {
        'plant': 'Blueberry',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Maintain soil pH between 4.5-5.5 for optimal growth\n"
            "2. Apply mulch with pine bark or sawdust to retain moisture\n"
            "3. Prune old canes annually to stimulate new growth\n"
            "4. Protect berries with netting from bird damage\n"
            "5. Provide consistent irrigation, especially during fruit development"
        ),
    },
    'Cherry_(including_sour)___Powdery_mildew': {
        'plant': 'Cherry',
        'disease_name': 'Powdery Mildew',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'White powdery coating on leaves',
            'Leaf curling and distortion',
            'Stunted new growth',
            'Premature leaf drop',
        ],
        'affected_parts': ['Leaves', 'Young shoots', 'Fruit'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply sulfur-based or potassium bicarbonate fungicide\n"
            "2. Improve air circulation by proper pruning and spacing\n"
            "3. Avoid overhead watering to keep foliage dry\n"
            "4. Remove and destroy severely infected plant parts\n"
            "5. Apply neem oil as an organic treatment option"
        ),
    },
    'Cherry_(including_sour)___healthy': {
        'plant': 'Cherry',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Water deeply and infrequently to encourage deep root growth\n"
            "2. Fertilize with balanced fertilizer in early spring\n"
            "3. Prune annually during dormant season\n"
            "4. Monitor for signs of brown rot, leaf spot, and pests\n"
            "5. Use protective netting during fruiting season to prevent bird damage"
        ),
    },
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
        'plant': 'Corn (Maize)',
        'disease_name': 'Gray Leaf Spot (Cercospora)',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Rectangular gray-to-tan lesions on leaves',
            'Lesions bounded by leaf veins',
            'Lower leaves affected first',
            'Significant leaf area loss in severe cases',
        ],
        'affected_parts': ['Leaves'],
        'spread_risk': 'High',
        'stage': 'Advanced',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Plant resistant corn hybrids in future seasons\n"
            "2. Rotate crops — avoid planting corn after corn\n"
            "3. Apply foliar fungicides (strobilurin or triazole) if detected early\n"
            "4. Till crop residue to reduce overwintering spores\n"
            "5. Ensure adequate spacing between rows for air circulation"
        ),
    },
    'Corn_(maize)___Common_rust_': {
        'plant': 'Corn (Maize)',
        'disease_name': 'Common Rust',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small, round-to-elongated reddish-brown pustules on both leaf surfaces',
            'Pustules may turn dark brown to black as they mature',
            'Chlorosis around pustule sites',
            'Heavy infection leads to premature drying of leaves',
        ],
        'affected_parts': ['Leaves', 'Leaf sheaths'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Average',
        'yield_potential': 'Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Plant rust-resistant corn varieties\n"
            "2. Apply fungicide (triazole or strobilurin) if infection is detected before tasseling\n"
            "3. Scout fields regularly for early detection\n"
            "4. Maintain balanced fertilization — avoid excess nitrogen\n"
            "5. Remove and destroy heavily infected plants in small plantings"
        ),
    },
    'Corn_(maize)___Northern_Leaf_Blight': {
        'plant': 'Corn (Maize)',
        'disease_name': 'Northern Leaf Blight',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Long, cigar-shaped gray-green lesions on leaves',
            'Lesions may be 1-6 inches long',
            'Infected areas turn tan as they mature',
            'Severe infection causes extensive leaf death',
        ],
        'affected_parts': ['Leaves'],
        'spread_risk': 'High',
        'stage': 'Advanced',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Use resistant corn hybrids (Ht genes)\n"
            "2. Apply foliar fungicides during early infection stages\n"
            "3. Practice crop rotation to reduce inoculum\n"
            "4. Manage residue through tillage to reduce overwintering spores\n"
            "5. Maintain optimal planting density to reduce humidity"
        ),
    },
    'Corn_(maize)___healthy': {
        'plant': 'Corn (Maize)',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Continue balanced fertilization, especially nitrogen at key growth stages\n"
            "2. Monitor soil moisture and irrigate during dry periods\n"
            "3. Scout regularly for pests like corn borers and rootworms\n"
            "4. Practice crop rotation with legumes to improve soil health\n"
            "5. Ensure adequate planting density for optimal yield"
        ),
    },
    'Grape___Black_rot': {
        'plant': 'Grape',
        'disease_name': 'Black Rot',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Brown circular lesions on leaves with dark borders',
            'Black shriveled mummified berries',
            'Small dark spots on shoots',
            'Rapid spread in warm, humid conditions',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Shoots'],
        'spread_risk': 'High',
        'stage': 'Advanced',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Remove and destroy all mummified berries and infected canes\n"
            "2. Apply fungicides (myclobutanil or mancozeb) from bud break through veraison\n"
            "3. Improve canopy management — prune to allow air circulation\n"
            "4. Maintain a clean vineyard floor\n"
            "5. Choose resistant grape varieties for new plantings"
        ),
    },
    'Grape___Esca_(Black_Measles)': {
        'plant': 'Grape',
        'disease_name': 'Esca (Black Measles)',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Tiger-stripe pattern on leaves (interveinal chlorosis)',
            'Dark spots on berries',
            'Sudden vine wilting in severe cases (apoplexy)',
            'Internal wood decay',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Wood/Trunk'],
        'spread_risk': 'Medium',
        'stage': 'Advanced',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. No cure exists — manage by removing severely affected vines\n"
            "2. Apply wound protectants after pruning to prevent fungal entry\n"
            "3. Prune during dry weather only\n"
            "4. Avoid excessive vine stress (water stress, over-cropping)\n"
            "5. Consider trunk renewal by training a new shoot from the base"
        ),
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        'plant': 'Grape',
        'disease_name': 'Leaf Blight (Isariopsis Leaf Spot)',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Dark brown spots on leaves',
            'Spots may coalesce causing large necrotic areas',
            'Premature defoliation',
            'Reduced photosynthesis',
        ],
        'affected_parts': ['Leaves'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply copper-based fungicides at first sign of infection\n"
            "2. Remove and destroy infected leaves and debris\n"
            "3. Improve vineyard ventilation through proper canopy management\n"
            "4. Avoid overhead irrigation\n"
            "5. Maintain balanced vine nutrition to improve disease resistance"
        ),
    },
    'Grape___healthy': {
        'plant': 'Grape',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Maintain regular pruning and canopy management\n"
            "2. Apply dormant-season fungicide spray as a preventive measure\n"
            "3. Monitor for early signs of powdery mildew and downy mildew\n"
            "4. Ensure proper trellising for optimal sun exposure\n"
            "5. Irrigate consistently during fruit development"
        ),
    },
    'Orange___Haunglongbing_(Citrus_greening)': {
        'plant': 'Orange (Citrus)',
        'disease_name': 'Huanglongbing (Citrus Greening)',
        'disease_detected': True,
        'disease_type': 'Bacterial',
        'severity': 'critical',
        'overall_health': 'Critical',
        'symptoms': [
            'Blotchy yellow mottling on leaves (asymmetric)',
            'Lopsided, small, and bitter fruit',
            'Green fruit that fails to ripen properly',
            'Twig dieback and stunted growth',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Whole tree'],
        'spread_risk': 'High',
        'stage': 'Severe',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. There is no cure — remove and destroy severely infected trees immediately\n"
            "2. Control Asian citrus psyllid (vector) with systemic insecticides\n"
            "3. Use disease-free nursery stock for new plantings\n"
            "4. Apply nutritional sprays (zinc, manganese, iron) to support remaining trees\n"
            "5. Report to agricultural authorities if this is a new detection in your area"
        ),
    },
    'Peach___Bacterial_spot': {
        'plant': 'Peach',
        'disease_name': 'Bacterial Spot',
        'disease_detected': True,
        'disease_type': 'Bacterial',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small, dark, water-soaked lesions on leaves',
            'Leaf spots may cause shot-hole appearance',
            'Sunken, cracked spots on fruit',
            'Premature defoliation',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Twigs'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply copper bactericides during dormant season\n"
            "2. Use oxytetracycline sprays during the growing season\n"
            "3. Plant resistant peach varieties\n"
            "4. Avoid overhead irrigation and working with wet plants\n"
            "5. Ensure proper tree spacing for air circulation"
        ),
    },
    'Peach___healthy': {
        'plant': 'Peach',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Thin fruit early to improve size and quality\n"
            "2. Apply dormant fungicide spray to prevent peach leaf curl\n"
            "3. Prune annually for shape and to remove dead wood\n"
            "4. Monitor for oriental fruit moth and peach tree borers\n"
            "5. Provide consistent irrigation during fruit development"
        ),
    },
    'Pepper,_bell___Bacterial_spot': {
        'plant': 'Bell Pepper',
        'disease_name': 'Bacterial Spot',
        'disease_detected': True,
        'disease_type': 'Bacterial',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small, water-soaked spots on leaves',
            'Raised, scab-like lesions on fruit',
            'Defoliation in severe cases',
            'Reduced fruit quality',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Stems'],
        'spread_risk': 'High',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Use pathogen-free seeds and transplants\n"
            "2. Apply copper-based bactericides as a preventive spray\n"
            "3. Practice crop rotation — avoid planting peppers in the same spot for 2-3 years\n"
            "4. Remove and destroy infected plant debris\n"
            "5. Avoid overhead irrigation; use drip irrigation instead"
        ),
    },
    'Pepper,_bell___healthy': {
        'plant': 'Bell Pepper',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Provide consistent watering — peppers are sensitive to drought stress\n"
            "2. Apply balanced fertilizer with calcium to prevent blossom end rot\n"
            "3. Use mulch to regulate soil temperature and retain moisture\n"
            "4. Support plants with stakes if heavy with fruit\n"
            "5. Monitor for aphids, mites, and whiteflies"
        ),
    },
    'Potato___Early_blight': {
        'plant': 'Potato',
        'disease_name': 'Early Blight',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Dark brown concentric ring lesions on older leaves (target-spot pattern)',
            'Yellowing around lesions',
            'Lower leaves affected first',
            'Dark lesions on tubers',
        ],
        'affected_parts': ['Leaves', 'Stems', 'Tubers'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply chlorothalonil or mancozeb fungicide at first sign of infection\n"
            "2. Practice crop rotation with non-solanaceous crops\n"
            "3. Remove and destroy infected lower leaves\n"
            "4. Ensure adequate plant spacing for air circulation\n"
            "5. Avoid overhead irrigation; water at base of plants"
        ),
    },
    'Potato___Late_blight': {
        'plant': 'Potato',
        'disease_name': 'Late Blight',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'critical',
        'overall_health': 'Critical',
        'symptoms': [
            'Large, dark, water-soaked lesions on leaves',
            'White fuzzy growth on leaf undersides in humid conditions',
            'Rapid browning and collapse of foliage',
            'Brown, firm rot on tubers',
        ],
        'affected_parts': ['Leaves', 'Stems', 'Tubers'],
        'spread_risk': 'High',
        'stage': 'Severe',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Apply preventive fungicides (mancozeb, chlorothalonil) before infection occurs\n"
            "2. Destroy all infected plant material immediately — do not compost\n"
            "3. Plant certified disease-free seed potatoes\n"
            "4. Avoid planting near tomatoes (also susceptible)\n"
            "5. Harvest tubers in dry conditions and cure before storage"
        ),
    },
    'Potato___healthy': {
        'plant': 'Potato',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Hill soil around stems as plants grow to protect tubers from light\n"
            "2. Maintain consistent moisture — irregular watering causes knobby tubers\n"
            "3. Apply balanced fertilizer at planting time\n"
            "4. Monitor for Colorado potato beetles and aphids\n"
            "5. Harvest when foliage yellows and dies back naturally"
        ),
    },
    'Raspberry___healthy': {
        'plant': 'Raspberry',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Remove spent canes after fruiting for summer-bearing varieties\n"
            "2. Train canes to a trellis for support and air circulation\n"
            "3. Mulch to suppress weeds and conserve moisture\n"
            "4. Apply balanced fertilizer in early spring\n"
            "5. Monitor for spider mites and Japanese beetles"
        ),
    },
    'Soybean___healthy': {
        'plant': 'Soybean',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Rotate soybeans with corn or other non-legume crops\n"
            "2. Test soil pH and maintain between 6.0-7.0\n"
            "3. Scout for soybean cyst nematode and sudden death syndrome\n"
            "4. Use seed treatments for early-season protection\n"
            "5. Monitor for soybean aphids and bean leaf beetles"
        ),
    },
    'Squash___Powdery_mildew': {
        'plant': 'Squash',
        'disease_name': 'Powdery Mildew',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'White powdery patches on upper leaf surfaces',
            'Yellowing and browning of affected leaves',
            'Reduced plant vigor',
            'Premature leaf death',
        ],
        'affected_parts': ['Leaves', 'Stems'],
        'spread_risk': 'High',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply potassium bicarbonate or sulfur-based fungicide\n"
            "2. Spray neem oil or milk solution (1:9 ratio) as an organic option\n"
            "3. Plant resistant squash varieties\n"
            "4. Ensure proper plant spacing for good airflow\n"
            "5. Water at the base of plants — avoid wetting foliage"
        ),
    },
    'Strawberry___Leaf_scorch': {
        'plant': 'Strawberry',
        'disease_name': 'Leaf Scorch',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small, dark purple spots on upper leaf surfaces',
            'Spots enlarge and merge, causing a burned or scorched appearance',
            'Margins of leaves may dry out and curl',
            'Reduced runner production',
        ],
        'affected_parts': ['Leaves', 'Runners', 'Petioles'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Remove and destroy infected leaves and plant debris\n"
            "2. Apply copper-based fungicide as a preventive measure\n"
            "3. Renovate strawberry beds after harvest by mowing and thinning\n"
            "4. Plant resistant strawberry varieties\n"
            "5. Avoid overhead irrigation to reduce leaf wetness"
        ),
    },
    'Strawberry___healthy': {
        'plant': 'Strawberry',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Renovate beds after harvest for June-bearing varieties\n"
            "2. Apply straw mulch for winter protection and weed suppression\n"
            "3. Fertilize with balanced fertilizer after renovation\n"
            "4. Monitor for slugs, spider mites, and tarnished plant bugs\n"
            "5. Replace strawberry plants every 3-4 years for best production"
        ),
    },
    'Tomato___Bacterial_spot': {
        'plant': 'Tomato',
        'disease_name': 'Bacterial Spot',
        'disease_detected': True,
        'disease_type': 'Bacterial',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small, dark, water-soaked spots on leaves',
            'Spots may have yellow halos',
            'Raised, scab-like lesions on fruit',
            'Defoliation in severe cases',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Stems'],
        'spread_risk': 'High',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Use disease-free seed and transplants\n"
            "2. Apply copper-based bactericides preventively\n"
            "3. Practice crop rotation — avoid solanaceous crops for 2-3 years\n"
            "4. Remove and destroy infected plant material\n"
            "5. Use drip irrigation instead of overhead watering"
        ),
    },
    'Tomato___Early_blight': {
        'plant': 'Tomato',
        'disease_name': 'Early Blight',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Dark brown target-like concentric ring lesions on older leaves',
            'Yellowing around lesions',
            'Lower leaves affected first, progressing upward',
            'Dark sunken spots on fruit near the stem end',
        ],
        'affected_parts': ['Leaves', 'Stems', 'Fruit'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Average',
        'yield_potential': 'Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply chlorothalonil or copper fungicide at first sign of symptoms\n"
            "2. Remove infected lower leaves to slow disease spread\n"
            "3. Mulch around plant base to prevent soil splash\n"
            "4. Stake or cage plants to improve air circulation\n"
            "5. Practice crop rotation and avoid planting tomatoes in the same spot"
        ),
    },
    'Tomato___Late_blight': {
        'plant': 'Tomato',
        'disease_name': 'Late Blight',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'critical',
        'overall_health': 'Critical',
        'symptoms': [
            'Large, dark, irregular water-soaked lesions on leaves',
            'White fuzzy growth on undersides of leaves',
            'Rapid foliage collapse',
            'Brown-black firm rot on fruit',
        ],
        'affected_parts': ['Leaves', 'Stems', 'Fruit'],
        'spread_risk': 'High',
        'stage': 'Severe',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Apply fungicide (chlorothalonil or copper) at first sign — act immediately\n"
            "2. Remove and destroy all infected plants — do not compost\n"
            "3. Avoid overhead watering — use drip irrigation\n"
            "4. Plant resistant tomato varieties\n"
            "5. Monitor weather — late blight thrives in cool, wet conditions"
        ),
    },
    'Tomato___Leaf_Mold': {
        'plant': 'Tomato',
        'disease_name': 'Leaf Mold',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Pale green-to-yellow spots on upper leaf surfaces',
            'Olive-green velvety mold on leaf undersides',
            'Leaves may curl and drop prematurely',
            'Most common in greenhouse or high-humidity conditions',
        ],
        'affected_parts': ['Leaves'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Average',
        'yield_potential': 'Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Improve ventilation in greenhouses — reduce humidity below 85%\n"
            "2. Remove and destroy infected leaves\n"
            "3. Apply chlorothalonil or copper-based fungicide\n"
            "4. Increase plant spacing for better air circulation\n"
            "5. Water early in the day to allow foliage to dry"
        ),
    },
    'Tomato___Septoria_leaf_spot': {
        'plant': 'Tomato',
        'disease_name': 'Septoria Leaf Spot',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small, circular spots with dark brown borders and gray centers on leaves',
            'Tiny black dots (pycnidia) visible in spot centers',
            'Lower leaves affected first',
            'Severe defoliation reduces fruit quality',
        ],
        'affected_parts': ['Leaves', 'Stems'],
        'spread_risk': 'High',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Remove and destroy affected lower leaves immediately\n"
            "2. Apply chlorothalonil or copper-based fungicide every 7-10 days\n"
            "3. Mulch around plants to prevent soil splash onto leaves\n"
            "4. Practice crop rotation — avoid planting tomatoes in same area for 3 years\n"
            "5. Water at plant base using drip irrigation"
        ),
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        'plant': 'Tomato',
        'disease_name': 'Spider Mite Infestation (Two-spotted)',
        'disease_detected': True,
        'disease_type': 'Pest',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Tiny yellow or white stippling on leaf surfaces',
            'Fine webbing on leaf undersides and between leaves',
            'Leaves turn bronze, dry out, and drop',
            'Stunted plant growth in severe cases',
        ],
        'affected_parts': ['Leaves', 'Stems'],
        'spread_risk': 'High',
        'stage': 'Moderate',
        'yield_impact': 'Below Average',
        'yield_potential': 'Below Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Spray plants with a strong jet of water to dislodge mites\n"
            "2. Apply insecticidal soap or neem oil to affected plants\n"
            "3. Introduce predatory mites (Phytoseiulus persimilis) as biological control\n"
            "4. Avoid broad-spectrum pesticides that kill beneficial predators\n"
            "5. Maintain adequate irrigation — drought-stressed plants attract mites"
        ),
    },
    'Tomato___Target_Spot': {
        'plant': 'Tomato',
        'disease_name': 'Target Spot',
        'disease_detected': True,
        'disease_type': 'Fungal',
        'severity': 'medium',
        'overall_health': 'Fair',
        'symptoms': [
            'Small brown spots with concentric rings (target pattern) on leaves',
            'Spots enlarge and may merge',
            'Lower canopy affected first',
            'Fruit may develop sunken lesions',
        ],
        'affected_parts': ['Leaves', 'Stems', 'Fruit'],
        'spread_risk': 'Medium',
        'stage': 'Moderate',
        'yield_impact': 'Average',
        'yield_potential': 'Average',
        'plant_vigor': 'Moderate',
        'recommendations': (
            "1. Apply broad-spectrum fungicide (chlorothalonil or azoxystrobin)\n"
            "2. Remove lower infected leaves to slow disease spread\n"
            "3. Ensure good air circulation through staking and spacing\n"
            "4. Avoid overhead irrigation\n"
            "5. Practice crop rotation and remove plant debris at season end"
        ),
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'plant': 'Tomato',
        'disease_name': 'Tomato Yellow Leaf Curl Virus (TYLCV)',
        'disease_detected': True,
        'disease_type': 'Viral',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Severe upward curling and cupping of leaves',
            'Yellowing of leaf edges',
            'Stunted, bushy growth',
            'Dramatically reduced fruit production',
        ],
        'affected_parts': ['Leaves', 'Whole plant'],
        'spread_risk': 'High',
        'stage': 'Advanced',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Remove and destroy infected plants immediately — no cure\n"
            "2. Control whiteflies (the vector) with insecticidal soap or neem oil\n"
            "3. Use reflective mulch to repel whiteflies\n"
            "4. Plant TYLCV-resistant tomato varieties\n"
            "5. Use fine mesh insect netting to protect transplants"
        ),
    },
    'Tomato___Tomato_mosaic_virus': {
        'plant': 'Tomato',
        'disease_name': 'Tomato Mosaic Virus (ToMV)',
        'disease_detected': True,
        'disease_type': 'Viral',
        'severity': 'high',
        'overall_health': 'Poor',
        'symptoms': [
            'Mosaic pattern of light and dark green on leaves',
            'Leaf distortion and fern-like appearance',
            'Stunted growth',
            'Reduced and uneven fruit ripening',
        ],
        'affected_parts': ['Leaves', 'Fruit', 'Whole plant'],
        'spread_risk': 'High',
        'stage': 'Advanced',
        'yield_impact': 'Poor',
        'yield_potential': 'Poor',
        'plant_vigor': 'Weak',
        'recommendations': (
            "1. Remove and destroy infected plants — the virus has no cure\n"
            "2. Disinfect tools, hands, and equipment with 10% bleach solution\n"
            "3. Do not use tobacco products near tomato plants (TMV cross-infection)\n"
            "4. Plant TMV/ToMV-resistant tomato varieties\n"
            "5. Wash hands thoroughly before handling healthy plants"
        ),
    },
    'Tomato___healthy': {
        'plant': 'Tomato',
        'disease_name': 'None',
        'disease_detected': False,
        'disease_type': 'None',
        'severity': 'healthy',
        'overall_health': 'Good',
        'symptoms': [],
        'affected_parts': [],
        'spread_risk': 'Low',
        'stage': 'N/A',
        'yield_impact': 'Excellent',
        'yield_potential': 'Excellent',
        'plant_vigor': 'Strong',
        'recommendations': (
            "1. Support plants with cages or stakes for proper growth\n"
            "2. Water consistently at 1-2 inches per week, at the base\n"
            "3. Apply balanced fertilizer every 2-3 weeks during fruiting\n"
            "4. Prune suckers for indeterminate varieties for bigger fruit\n"
            "5. Monitor regularly for early signs of blight, wilt, and pests"
        ),
    },
}


def get_info_for_class(class_name):
    """Retrieve the knowledge base entry for a given class name."""
    return DISEASE_DATABASE.get(class_name, None)


def get_class_index(class_name):
    """Return the index of a class name in CLASS_NAMES, or -1 if not found."""
    try:
        return CLASS_NAMES.index(class_name)
    except ValueError:
        return -1
