import os

path = r'x:\FP\garden\templates\garden\user_garden_final.html'
with open(path, 'r') as f:
    content = f.read()

# Fix all variants of == without spaces
content = content.replace("status=='Planning'", "status == 'Planning'")
content = content.replace("status=='Growing'", "status == 'Growing'")
content = content.replace("status=='Harvested'", "status == 'Harvested'")
content = content.replace('status=="Planning"', 'status == "Planning"')
content = content.replace('status=="Growing"', 'status == "Growing"')
content = content.replace('status=="Harvested"', 'status == "Harvested"')

with open(path, 'w') as f:
    f.write(content)

print('Done. Verifying...')
with open(path, 'r') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'status' in l and 'selected' in l:
        print(f'Line {i+1}: {repr(l)}')
