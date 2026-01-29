import os

def replace_purple_with_emerald(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'purple' in content:
                    new_content = content.replace('purple', 'emerald')
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {path}")

# Target directories
dirs = [
    r"e:\Mtaani Connect James\web\templates\web",
    r"e:\Mtaani Connect James\templates"
]

for d in dirs:
    if os.path.exists(d):
        replace_purple_with_emerald(d)
    else:
        print(f"Directory not found: {d}")
