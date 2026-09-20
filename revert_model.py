import os
import glob

files = glob.glob('agents/**/*.py', recursive=True)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'gemini-1.5-flash' in content:
        content = content.replace('gemini-1.5-flash', 'gemini-3.5-flash')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Reverted in {file}")
