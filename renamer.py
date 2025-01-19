import os
import argparse

def load_titles(output_file):
    titles = {}
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    name, title = line.split('=', 1)
                    titles[name.strip()] = title.strip().strip('"')
    except Exception as e:
        print(f"Error reading output file: {e}")
    return titles

def rename_files_in_folder(folder, titles):
    try:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                file_name, file_ext = os.path.splitext(file)
                if file_name in titles:
                    new_name = f"{titles[file_name]}{file_ext}"
                    new_path = os.path.join(folder, new_name)
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file} -> {new_name}")
    except Exception as e:
        print(f"Error renaming files: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename files in a folder based on an output file.")
    parser.add_argument('-f', '--folder', required=True, help="Folder containing files to rename.")
    parser.add_argument('-o', '--output', required=True, help="Output file with names and titles.")
    args = parser.parse_args()

    folder = args.folder
    output_file = args.output

    titles = load_titles(output_file)
    rename_files_in_folder(folder, titles)

if __name__ == "__main__":
    main()
