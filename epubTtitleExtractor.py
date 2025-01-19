import os
import zipfile
import argparse
import re

def extract_title_from_toc(epub_path):
    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            toc_path = 'OEBPS/toc.xhtml'
            if toc_path in z.namelist():
                with z.open(toc_path) as toc_file:
                    toc_content = toc_file.read().decode('utf-8')
                    title_match = re.search(r'<title>(.*?)</title>', toc_content, re.IGNORECASE)
                    if title_match:
                        return title_match.group(1)
            toc_path = 'OEBPS/Text/toc.xhtml'
            if toc_path in z.namelist():
                with z.open(toc_path) as toc_file:
                    toc_content = toc_file.read().decode('utf-8')
                    title_match = re.search(r'<title>(.*?)</title>', toc_content, re.IGNORECASE)
                    if title_match:
                        return title_match.group(1)
            opf_path = 'EPUB/content.opf'
            if opf_path in z.namelist():
                with z.open(opf_path) as opf_file:
                    opf_content = opf_file.read().decode('utf-8')
                    title_match = re.search(r'<dc:title.*?>(.*?)</dc:title>', opf_content, re.IGNORECASE)
                    if title_match:
                        return title_match.group(1)

            ncx_path = 'OEBPS/toc.ncx'
            if ncx_path in z.namelist():
                with z.open(ncx_path) as ncx_file:
                    ncx_content = ncx_file.read().decode('utf-8')
                    doc_title_match = re.search(r'<docTitle>\s*(.*?)\s*</docTitle>', ncx_content, re.DOTALL | re.IGNORECASE)
                    if doc_title_match:
                        # Remove any remaining XML tags within <docTitle>
                        clean_title = re.sub(r'<.*?>', '', doc_title_match.group(1)).strip()
                        return clean_title
    except Exception as e:
        print(f"Error processing {epub_path}: {e}")
    return None


def scan_folder_for_epubs(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith('.epub')
    ]

def write_output(output_path, titles):
    try:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            for epub_name, title in titles.items():
                print(f"{epub_name}={title}")
                out_file.write(f'{epub_name} = "{title}"\n')
    except Exception as e:
        print(f"Error writing output file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract titles from EPUB files.")
    parser.add_argument('-f', '--folder', required=True, help="Folder to scan for EPUB files.")
    parser.add_argument('-o', '--output', required=True, help="Output file to write titles.")
    args = parser.parse_args()

    folder = args.folder
    output_file = args.output

    epub_files = scan_folder_for_epubs(folder)
    titles = {}

    for epub_path in epub_files:
        epub_name = os.path.splitext(os.path.basename(epub_path))[0]
        title = extract_title_from_toc(epub_path)
        if title:
            titles[epub_name] = title.replace(',', ' ')
        else:
            titles[epub_name] = "<Title not found>"

    write_output(output_file, titles)

if __name__ == "__main__":
    main()
