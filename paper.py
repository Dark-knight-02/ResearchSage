import urllib.parse
import urllib.request
import feedparser
import os
from PyPDF2 import PdfMerger



def download_and_merge_pdfs(urls, query):
    pdf_filename = f"{query.replace(' ', '_')}.pdf"
    save_path = os.path.join('arxiv_pdfs', pdf_filename)
    merger = PdfMerger()
    for url in urls:
        response = urllib.request.urlopen(url)
        with open("/tmp/temp_pdf.pdf", "wb") as f:
            f.write(response.read())
        merger.append("/tmp/temp_pdf.pdf")
    merged_path = pdf_filename
    merger.write(merged_path)
    merger.close()

def merge_pdfs(folder_path, output_path):
    merger = PdfMerger()

    for item in os.listdir(folder_path):
        if item.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, item)
            merger.append(pdf_path)
            print(f"Added {pdf_path}")

    merger.write(output_path)
    merger.close()
    print(f"All PDFs merged into {output_path}")

def download_pdf(pdf_url, save_path):
    try:
        with urllib.request.urlopen(pdf_url) as response, open(save_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Downloaded PDF to {save_path}")
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")


def get_arxiv_articles(query, start_year, end_year, max_results=5):
    base_url = 'http://export.arxiv.org/api/query?'
    # Construct start and end dates
    start_date = f'{start_year}0101'
    end_date = f'{end_year}1231'
    # Construct the search query with date range
    search_query = f'all:{query} AND submittedDate:[{start_date} TO {end_date}]'
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': max_results
    }
    url = base_url + urllib.parse.urlencode(params)
    response = urllib.request.urlopen(url).read()
    feed = feedparser.parse(response)

    articles = []
    for entry in feed.entries:
        article_id = entry.id.split('/abs/')[-1]
        pdf_url = f'https://arxiv.org/pdf/{article_id}.pdf'
        article = {
            'title': entry.title,
            'authors': [author.name for author in entry.authors],
            'summary': entry.summary,
            'published': entry.published,
            'link': entry.link,
            'pdf_url': pdf_url,
            'article_id': article_id
        }
        articles.append(article)
        pdf_filename = f"{article['article_id'].replace('/', '_')}.pdf"
        save_path = os.path.join('arxiv_pdfs', pdf_filename)
        download_pdf(article['pdf_url'], save_path)
        pdf_filename2 = f"{query.replace(' ', '_')}.pdf"
        save_path2 = os.path.join('arxiv_pdfs', pdf_filename2)
        merge_pdfs('arxiv_pdfs', save_path2)
    
    
    return articles




if __name__ == '__main__':
    topic = 'machine learning'   # Replace with your topic of interest
    start_year = '2020'          # Start year
    end_year = '2022'            # End year
    max_results = 5              # Number of articles to retrieve

    articles = get_arxiv_articles(topic, start_year, end_year, max_results)

    # Create a directory to save PDFs
    os.makedirs('arxiv_pdfs', exist_ok=True)

    for idx, article in enumerate(articles, start=1):
        print(f"Article {idx}:")
        print(f"Title     : {article['title']}")
        print(f"Authors   : {', '.join(article['authors'])}")
        print(f"Published : {article['published']}")
        print(f"Link      : {article['link']}")
        print(f"PDF URL   : {article['pdf_url']}")
        print(f"Summary   : {article['summary'][:200]}...")
        print("\n" + "-"*80 + "\n")

        # Download the PDF
        pdf_filename = f"{article['article_id'].replace('/', '_')}.pdf"
        save_path = os.path.join('arxiv_pdfs', pdf_filename)
        download_pdf(article['pdf_url'], save_path)