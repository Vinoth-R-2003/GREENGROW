import os
import shutil

# Artifacts directory
artifacts_dir = r"C:\Users\vinot\.gemini\antigravity\brain\95e9f1fa-78f1-424d-aebc-ec60aa06dd74"
# Media directory
target_dir = r"c:\Users\vinot\OneDrive\Documents\GitHub\GREENGROW\FP\media\item_types"

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Mapping of artifact filename parts to target names
mapping = {
    "watermelon": "watermelon.png",
    "grape": "grape.png",
    "pineapple": "pineapple.png",
    "lemon": "lemon.png",
    "blueberry": "blueberry.png",
    "papaya": "papaya.png",
    "pomegranate": "pomegranate.png",
    "orange": "orange.png",
    "kiwi": "kiwi.png",
    "guava": "guava.png",
    "broccoli": "broccoli.png",
    "bell_pepper": "bell_pepper.png",
    "garlic": "garlic.png",
    "ginger": "ginger.png",
    "cucumber": "cucumber.png",
    "radish": "radish.png",
    "sweet_potato": "sweet_potato.png",
}

print(f"Moving artifacts from {artifacts_dir} to {target_dir}...")

for filename in os.listdir(artifacts_dir):
    if filename.endswith(".png"):
        for key, target_name in mapping.items():
            if key in filename:
                src = os.path.join(artifacts_dir, filename)
                dst = os.path.join(target_dir, target_name)
                shutil.copy2(src, dst)
                print(f"Copied {filename} -> {target_name}")
                break

print("Done.")
