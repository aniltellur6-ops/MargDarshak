import os
import glob

files = glob.glob('agents/**/*.py', recursive=True)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'gemini-2.5-flash' in content:
        content = content.replace('gemini-2.5-flash', 'gemini-3.6-flash')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Replaced in {file}")
