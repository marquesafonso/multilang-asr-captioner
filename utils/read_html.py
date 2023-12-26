def read_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return content