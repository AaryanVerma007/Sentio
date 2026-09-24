import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace getElementById calls for missing elements with fallback to dummy div
elements_to_mock = ['macroLoading', 'battleResults', 'exportBtn', 'macroShareBtn', 'loadingTerminal', 'closeContactBtn', 'contactOverlay', 'contactSubmitBtn', 'topBarCmdHint']

for el in elements_to_mock:
    content = re.sub(
        r"const " + el + r"\s*=\s*document\.getElementById\(['\"]" + el + r"['\"]\);",
        f"const {el} = document.getElementById('{el}') || document.createElement('div');",
        content
    )
    content = re.sub(
        r"let " + el + r"\s*=\s*document\.getElementById\(['\"]" + el + r"['\"]\);",
        f"let {el} = document.getElementById('{el}') || document.createElement('div');",
        content
    )

# Fix closeContactBtn listener (which wasn't a variable)
content = content.replace("document.getElementById('closeContactBtn').addEventListener", "(document.getElementById('closeContactBtn')||{addEventListener:()=>{}}).addEventListener")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
