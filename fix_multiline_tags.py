
import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to find {{ ... }} tags that span multiple lines
    # We look for {{, then anything non-greedy until }}, where the content contains a newline.
    # We use dotall to match newlines.
    pattern = re.compile(r'(\{\{\s*.*?\s*\}\})', re.DOTALL)
    
    def replacer(match):
        text = match.group(1)
        if '\n' in text:
            # It's multiline. Normalize it.
            # Remove newlines and excess whitespace.
            # But be careful about strings like "line 1 \n line 2" inside the tag.
            # For template tags, it's usually safe to replace \s+ with ' ' unless it's inside a quoted string.
            # However, a simpler approach for this specific issue (variables split across lines)
            # is just to join lines.
            
            # Simple approach: Replace newlines with spaces, then collapse multiple spaces.
            clean = re.sub(r'\s+', ' ', text)
            return clean
        return text

    new_content = pattern.sub(replacer, content)
    
    # Also fix the specific split-string issues likely caused by formatters
    # e.g. default:"Some text \n more text" -> default:"Some text more text"
    # This is harder to regex safely without a parser, but we can target the specific patterns seen.
    
    if new_content != original_content:
        print(f"Fixing {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dirs = [r'e:\Mtaani Connect James\web\templates', r'e:\Mtaani Connect James\templates']
    count = 0
    for base_dir in base_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.html'):
                    path = os.path.join(root, file)
                    if fix_file(path):
                        count += 1
    print(f"Fixed {count} files.")

if __name__ == "__main__":
    main()
