color = [
    '#6699cc',
    '#66cc99',
    '#9966cc',
    '#99cc66',
    '#cc6699',
    '#cc9966',
    '#99ccff',
    '#99ffcc',
    '#ccff99',
    '#cc99ff',
    '#ff99cc',
    '#ffcc99',
]

def safe(name):
    return re.sub(r'[/.:]', '_', name)
