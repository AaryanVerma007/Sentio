with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('id="pdf-single-report"')
if idx != -1:
    start_idx = content.rfind('<!--', 0, idx)
    if start_idx == -1: start_idx = content.rfind('<div', 0, idx)
    
    body_end = content.find('</body>')
    scripts_to_keep = '\n    <script src="script.js"></script>\n'
    
    new_content = content[:start_idx] + scripts_to_keep + content[body_end:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Cleaned up templates!')
else:
    print('No templates found.')
