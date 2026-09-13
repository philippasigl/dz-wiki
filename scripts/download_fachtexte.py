#!/usr/bin/env python3
"""
Download all Fachtexte from DZ archive.
Handles PDF links that redirect to actual PDF files.
"""

import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://dezernatzukunft.org"
ARCHIVE_URL = f"{BASE_URL}/publikationen"
OUTPUT_DIR = Path(__file__).parent.parent / "publikationen"
DELAY = 0.5  # seconds between requests
MAX_PAGES = 30  # safety cap; loop stops early once a page has no article cards

def get_archive_page(page_num: int) -> str:
    """Fetch an archive listing page (1-indexed; page 1 has no /page: suffix)."""
    url = ARCHIVE_URL if page_num == 1 else f"{ARCHIVE_URL}/page:{page_num}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

def extract_article_links(html: str) -> list:
    """Extract Fachtext article URLs from an archive listing page.

    The listing shows every category (Fachtext, Geldbrief, Dashboard, ...) on
    the same unfiltered page; each card carries its category as visible text
    in `.article-card__category`, so filtering happens here rather than via
    a URL query param (the site's category filter is client-side JS, no
    server-rendered filtered URL exists).
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for card in soup.find_all('a', class_=re.compile(r'\barticle-card\b')):
        href = card.get('href')
        if not href or not href.startswith(BASE_URL):
            continue
        category_tag = card.find(class_='article-card__category')
        category = category_tag.get_text(strip=True) if category_tag else ''
        if 'Fachtext' not in category:
            continue
        if href not in links:
            links.append(href)

    return links

def find_pdf_link(article_url: str) -> tuple:
    """
    Visit article page and find PDF download link.
    Handles redirects to actual PDF files.
    Returns (pdf_url, title, final_pdf_url).
    """
    try:
        response = requests.get(article_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get title
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        pdf_link = None

        # Method 0: current site template marks the PDF card with class "file--pdf"
        file_link = soup.find('a', class_=re.compile(r'\bfile--pdf\b'))
        if file_link and file_link.get('href'):
            pdf_link = file_link['href']

        # Method 1: Look for "Download PDF" links (case insensitive)
        if not pdf_link:
            for link in soup.find_all('a', href=True):
                link_text = link.get_text(strip=True).lower()
                if 'download' in link_text and 'pdf' in link_text:
                    pdf_link = link['href']
                    break
                if link_text == 'pdf' or link_text == 'download':
                    pdf_link = link['href']
                    break

        # Method 2: Look for links containing author-year pattern (common for DZ)
        if not pdf_link:
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Pattern: /author-year-title/ or direct .pdf
                if re.search(r'/[a-z]+-\d{4}-', href.lower()) or href.endswith('.pdf'):
                    pdf_link = href
                    break

        # Method 3: Look for wp-content/uploads PDF links
        if not pdf_link:
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'wp-content/uploads' in href and '.pdf' in href:
                    pdf_link = href
                    break

        # Method 4: Any .pdf link
        if not pdf_link:
            for link in soup.find_all('a', href=True):
                if link['href'].endswith('.pdf'):
                    pdf_link = link['href']
                    break

        if not pdf_link:
            return None, title, None

        # Make absolute URL
        if not pdf_link.startswith('http'):
            pdf_link = urljoin(article_url, pdf_link)

        # Follow redirects to get actual PDF URL
        try:
            head_response = requests.head(pdf_link, allow_redirects=True, timeout=30)
            final_url = head_response.url

            # Check if it's actually a PDF
            content_type = head_response.headers.get('content-type', '')
            if 'pdf' in content_type or final_url.endswith('.pdf'):
                return pdf_link, title, final_url
            else:
                # Try GET request to follow redirects
                get_response = requests.get(pdf_link, allow_redirects=True, timeout=30, stream=True)
                final_url = get_response.url
                if final_url.endswith('.pdf'):
                    return pdf_link, title, final_url
        except requests.RequestException:
            pass

        return pdf_link, title, pdf_link

    except Exception as e:
        print(f"  Error: {e}")
        return None, None, None

def download_pdf(pdf_url: str, output_path: Path) -> bool:
    """Download a PDF file, following redirects."""
    try:
        response = requests.get(pdf_url, timeout=60, stream=True, allow_redirects=True)
        response.raise_for_status()

        # Verify it's a PDF
        content_type = response.headers.get('content-type', '')
        if 'pdf' not in content_type and not response.url.endswith('.pdf'):
            print(f"  Not a PDF: {content_type}")
            return False

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"  Download error: {e}")
        return False

def sanitize_filename(name: str) -> str:
    """Create a safe filename from title."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if len(name) > 100:
        name = name[:100]
    return name

def main():
    print("DZ Fachtexte Downloader v2")
    print("=" * 50)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get existing files (case-insensitive matching)
    existing = {f.stem.lower() for f in OUTPUT_DIR.glob('*.pdf')}
    print(f"Bereits vorhanden: {len(existing)} PDFs")

    # Collect all article links from Fachtexte pages
    print("\nSammle Fachtexte-Links...")
    all_articles = []

    for page in range(1, MAX_PAGES + 1):
        print(f"  Seite {page}...")
        try:
            html = get_archive_page(page)
            links = extract_article_links(html)
            print(f"    {len(links)} Fachtext-Links gefunden")
            if not links and page > 1:
                break
            all_articles.extend(links)
        except Exception as e:
            print(f"    Fehler: {e}")
            break
        time.sleep(DELAY)

    # Deduplicate
    all_articles = list(dict.fromkeys(all_articles))
    print(f"\nGesamt: {len(all_articles)} Artikel")

    # Process each article
    print("\nVerarbeite Artikel...")
    results = {
        'downloaded': [],
        'skipped': [],
        'no_pdf': [],
        'error': []
    }

    for i, article_url in enumerate(all_articles, 1):
        slug = article_url.rstrip('/').split('/')[-1]
        print(f"\n[{i}/{len(all_articles)}] {slug[:50]}")

        # Find PDF
        pdf_link, title, final_url = find_pdf_link(article_url)

        if not pdf_link:
            print("  Kein PDF gefunden")
            results['no_pdf'].append({'url': article_url, 'title': title})
            continue

        if not title:
            title = slug

        # Create filename
        filename = sanitize_filename(title) + ".pdf"
        output_path = OUTPUT_DIR / filename

        # Check if exists
        if sanitize_filename(title).lower() in existing or output_path.exists():
            print("  Uebersprungen (existiert)")
            results['skipped'].append(filename)
            continue

        # Download
        download_url = final_url if final_url else pdf_link
        print(f"  Lade: {filename[:60]}...")

        if download_pdf(download_url, output_path):
            print("  OK")
            results['downloaded'].append(filename)
            existing.add(sanitize_filename(title).lower())
        else:
            print("  FEHLER")
            results['error'].append({'filename': filename, 'url': download_url})

        time.sleep(DELAY)

    # Summary
    print("\n" + "=" * 50)
    print("Zusammenfassung")
    print("=" * 50)
    print(f"Heruntergeladen: {len(results['downloaded'])}")
    print(f"Uebersprungen:   {len(results['skipped'])}")
    print(f"Kein PDF:        {len(results['no_pdf'])}")
    print(f"Fehler:          {len(results['error'])}")

    if results['no_pdf']:
        print("\nArtikel ohne PDF:")
        for item in results['no_pdf'][:10]:
            print(f"  - {item.get('title', item.get('url', 'Unknown'))}")
        if len(results['no_pdf']) > 10:
            print(f"  ... und {len(results['no_pdf']) - 10} weitere")

    # Save results
    results_file = OUTPUT_DIR / "download_log.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nLog: {results_file}")

    # Final count
    final_count = len(list(OUTPUT_DIR.glob('*.pdf')))
    print(f"\nPDFs gesamt: {final_count}")

if __name__ == '__main__':
    main()
