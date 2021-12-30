grammar = {
    'operator': '((?<=\s)|(?<=^)){key}(?=[\s:])',
    'method': '(?<=([^\u4e00-\u9fa5\w])){key}(?=\(.*\))',
    'lib': {
        'import': '^\s*import.+$',
        'from': '^\s*from.+$',
        'import_cut': '(?<=import\s).+$',
        'from_cut': '(?<=from\s).+(?=\simport)'
    }
}