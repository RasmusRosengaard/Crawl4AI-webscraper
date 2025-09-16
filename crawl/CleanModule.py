from bs4 import BeautifulSoup
import html
from pathlib import Path
import re

def main():
    root_folder = Path("html")
    output_folder = Path("clean_html")

    for html_file in root_folder.rglob("*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")
        paragraphs = []

        for p in soup.find_all("p"):
            text = p.get_text(separator=" ", strip=True)
            text = html.unescape(text)
            text = re.sub(r'\s+', ' ', text)  
            if text.endswith('.') and len(text.split()) >= 4:
                paragraphs.append(text)

        if not paragraphs:
            print(f"Skipping empty file: {html_file}")
            continue

        relative_path = html_file.relative_to(root_folder)
        output_file = output_folder / relative_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(paragraphs))

        print(f"Cleaned {html_file} -> {output_file}")

if __name__ == "__main__":
    main()
