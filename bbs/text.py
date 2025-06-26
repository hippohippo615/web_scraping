import requests
from bs4 import BeautifulSoup
#爬取bbs文章內容
base = 'https://www.ptt.cc'
index = base + '/bbs/NBA/index.html'
session = requests.Session()
# 模擬已滿18歲
session.post(base + '/ask/over18', data={'yes':'yes'})

res = session.get(index)
soup = BeautifulSoup(res.text, 'lxml')

articles = []  # 存 {title, url, content}

for a in soup.select('.r-ent .title a'):
    title = a.get_text()
    link  = a['href']
    url   = base + link

    # 取文章內文
    r2 = session.get(url)
    s2 = BeautifulSoup(r2.text, 'lxml')
    #選擇 id="main-content" 的元素
    main = s2.select_one('#main-content')

    # 移除 metadata & 推文
    for tag in main.select('div.article-metaline, div.article-metaline-right, div.push'):
        tag.decompose()

    content = main.get_text(strip=True, separator='\n')
    articles.append({
        'title': title,
        'url'  : url,
        'text' : content
    })

# 範例：只印前兩篇的標題與前 200 字
for art in articles:
    print(art['title'])
    print(art['url'])
    print()
    print(art['text'][:200], '…\n')
    print("="*50)