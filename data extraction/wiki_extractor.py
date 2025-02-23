import os

def run_wikiextractor(wiki_dump_path, output_dir):
    """
    Run WikiExtractor on the provided Wikipedia dump file.
    """
    os.system(f"python -m wikiextractor.WikiExtractor {wiki_dump_path} -o {output_dir} --json")

if __name__ == "__main__":
    wiki_dump_path = "data/raw/enwiki-latest-pages-articles.xml.bz2"
    output_dir = "data/raw/wiki_extracted/"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    run_wikiextractor(wiki_dump_path, output_dir)
    print(f"Extraction complete! Extracted files saved to {output_dir}")
