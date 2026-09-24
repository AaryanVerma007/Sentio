import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Make all document.getElementById(...).addEventListener safe
content = re.sub(
    r"document\.getElementById\(['\"]([^'\"]+)['\"]\)\.addEventListener",
    r"(document.getElementById('\1') || {addEventListener:()=>{}}).addEventListener",
    content
)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
