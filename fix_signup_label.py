
path = r"e:\Mtaani Connect James\templates\registration\signup.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I suspect there might be a invisible character or something in the split line
# Let's just rewrite the problematic block entirely.
target_block = """        <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2 ml-1">{{ field.label
            }}</label>"""

replacement_block = """        <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2 ml-1">{{ field.label }}</label>"""

if target_block in content:
    new_content = content.replace(target_block, replacement_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed signup label.")
else:
    # Try a regex approach or manual cleanup if exact match fails
    print("Target block not found, trying fuzzy fix.")
    import re
    new_content = re.sub(r'\{\{\s*field\.label\s*\}\}', '{{ field.label }}', content, flags=re.DOTALL)
    # Also fix the weird split in my previous view
    new_content = new_content.replace('{{ field.label\n            }}', '{{ field.label }}')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fuzzy fix applied.")
