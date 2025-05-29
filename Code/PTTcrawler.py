import requests
from bs4 import BeautifulSoup

PTT_URL = 'https://www.ptt.cc'
BOARD = 'lifeismoney'
OUTPUT_FILE = 'ptt_lifeismoney_100.txt'

def get_articles_from_index(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    entries = soup.select('div.r-ent')
    articles = []
    for entry in entries:
        title_tag = entry.select_one('div.title a')
        if title_tag:
            title = title_tag.text.strip()
            link = title_tag['href']
            articles.append({
                'title': title,
                'link': PTT_URL + link
            })
    return articles, soup

def get_prev_page_url(soup):
    btns = soup.select('div.btn-group-paging a')
    for btn in btns:
        if '上頁' in btn.text:
            return PTT_URL + btn['href']
    return None

def get_article_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    main_content = soup.select_one('#main-content')
    for tag in main_content(['div', 'span']):
        tag.decompose()
    lines = main_content.get_text().splitlines()
    filtered_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == '--':
            break
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)

def get_latest_100_articles():
    url = f'{PTT_URL}/bbs/{BOARD}/index.html'
    all_articles = []

    while len(all_articles) < 100:
        articles, soup = get_articles_from_index(url)
        all_articles.extend(articles)
        if len(all_articles) >= 100:
            break
        url = get_prev_page_url(soup)
        if not url:
            break

    return all_articles[:100]

# 主程式執行並寫入檔案
articles = get_latest_100_articles()

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for idx, article in enumerate(articles, 1): #從 1 開始編號
        content = get_article_content(article['link'])
        f.write(f"文章：{article['title']}\n")
        f.write(f"連結：{article['link']}\n")
        f.write("內文：\n")
        f.write(content + "\n\n")
        # 可選：顯示進度
        # print(f"第{idx:03d}篇已儲存：{article['title']}")
print(f"\n✅ 所有文章已存入 {OUTPUT_FILE}")
