import requests
import pandas as pd

def fetch__articles(base_url, page=1, per_page=10):
    res = requests.get(f'{base_url}/api/v1/articles', params={'page': page, per_page: per_page})
    if res.status_code == 200:
        return res.json()
    else:
        return None
    
def main():
    base_url = 'http://[::1]:3000'
    all_articles =[]
    page = 1

    print('hello')
    while True:
        articles = fetch__articles(base_url, page=page)
        if not articles:
            break
        all_articles.extend(articles)
        page += 1

    df_articles = pd.DataFrame(all_articles)
    print (df_articles)

if __name__ == '__main__':
    main()