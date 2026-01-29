
path = r"e:\Mtaani Connect James\web\templates\web\index.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# exact target string with newline
target = """{{ hero.description|default:"Connect with thousands of verified local workers for repairs, gardening,
                    cleaning, and more. Quality guaranteed." }}"""

replacement = """{{ hero.description|default:"Connect with thousands of verified local workers for repairs, gardening, cleaning, and more. Quality guaranteed." }}"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced content.")
else:
    print("Target string not found.")
    # Debug: print surrounding lines
    start = content.find("hero.description")
    if start != -1:
        print("Found nearby content:")
        print(content[start-50:start+200])
