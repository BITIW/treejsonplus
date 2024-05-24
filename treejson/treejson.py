import json
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_arguments():
    parser = argparse.ArgumentParser(description='Отобразить структуру JSON в виде дерева.')
    parser.add_argument('-L', '--level', type=int, default=999, help='Опуститься только на указанное количество уровней.')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Количество потоков для обработки.')
    return parser.parse_args()

def load_json():
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Пожалуйста, предоставьте допустимый JSON-документ.", file=sys.stderr)
        sys.exit(1)

def show_structure(root, depth, level=1, indent_chars=""):
    tasks = []
    with ThreadPoolExecutor() as executor:
        if isinstance(root, list):
            for i, value in enumerate(root):
                display_key = str(i)
                is_last = i == len(root) - 1
                tasks.append(executor.submit(print_tree_node, display_key, value, indent_chars, is_last, depth, level))
        elif isinstance(root, dict):
            for i, (key, value) in enumerate(root.items()):
                is_last = i == len(root) - 1
                tasks.append(executor.submit(print_tree_node, key, value, indent_chars, is_last, depth, level))

        for task in as_completed(tasks):
            task.result()

def print_tree_node(key, value, indent_chars, is_last, depth, level):
    tree_char = '└── ' if is_last else '├── '
    print(indent_chars + tree_char + key + (' []' if isinstance(value, list) else ''))
    
    if isinstance(value, (dict, list)) and level < depth:
        new_indent_chars = indent_chars + ('    ' if is_last else '│   ')
        show_structure(value, depth, level + 1, new_indent_chars)

def main():
    args = parse_arguments()
    Structure = load_json()
    print("." + (" []" if isinstance(Structure, list) else ""))
    show_structure(Structure, args.level)

if __name__ == "__main__":
    main()