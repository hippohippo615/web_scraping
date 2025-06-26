import requests
from bs4 import BeautifulSoup
from typing import List, Dict
#爬取文章內容
BASE_URL = 'https://www.ptt.cc'

def init_session() -> requests.Session:
    """建立一個可跨頁維持 cookies 的 Session，並通過 over-18 驗證。"""
    try:
        session = requests.Session()
        session.post(f'{BASE_URL}/ask/over18', data={'yes': 'yes'})
        print("✅ Session 初始化完成（已通過18歲驗證）")
        return session
    except Exception as e:
        print(f"❌ 初始化 Session 失敗：{e}")
        raise

def fetch_board_index(session: requests.Session, board: str) -> str:
    """下載看板首頁 HTML，傳回純文字。"""
    url = f'{BASE_URL}/bbs/{board}/index.html'
    try:
        resp = session.get(url)
        resp.raise_for_status()
        print(f"✅ 取得 {board} 看板首頁，狀態碼：{resp.status_code}")
        return resp.text
    except Exception as e:
        print(f"❌ 取得看板首頁失敗：{e}")
        raise

def parse_index(html: str) -> List[Dict[str, str]]:
    """從看板首頁 HTML 解析出每篇文章的標題與 URL。"""
    try:
        soup = BeautifulSoup(html, 'lxml')
        items: List[Dict[str,str]] = []
        for a in soup.select('.r-ent .title a'):
            items.append({
                'title': a.get_text(strip=True),
                'url':   BASE_URL + a['href']
            })
        print(f"✅ 共解析出 {len(items)} 篇文章連結")
        return items
    except Exception as e:
        print(f"❌ 解析看板列表失敗：{e}")
        raise

def fetch_article_content(session: requests.Session, url: str) -> str:
    """下載單篇文章並清理 metadata、推文，回傳純文字內容。"""
    try:
        resp = session.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        main = soup.select_one('#main-content')
        if not main:  # 如果 main 是 None，就直接結束函式、回傳空字串
            return ''
        # 移除作者、時間、推文等區塊
        for tag in main.select('div.article-metaline, div.article-metaline-right, div.push'):
            tag.decompose()
        content = main.get_text(strip=True, separator='\n')
        return content
    except Exception as e:
        print(f"⚠️ 下載或解析文章失敗 ({url})：{e}")
        return ''

def main():
    session = init_session()
    html    = fetch_board_index(session, 'NBA')
    links   = parse_index(html)
    articles = []
    for idx, item in enumerate(links, start=1):
        content = fetch_article_content(session, item['url'])
        articles.append({
            'title': item['title'],
            'url':   item['url'],
            'text':  content
        })
    # 範例：印出前兩篇標題與前200字
    for art in articles[:2]:
        print(art['title'])
        print(art['url'])
        print()
        print(art['text'][:200], '…\n')
        print('=' * 50)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] 程式異常結束：{e}")
