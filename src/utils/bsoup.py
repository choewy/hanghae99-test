import requests
from bs4 import BeautifulSoup


class BSoup:
    def __init__(self) -> None:
        self.agents = ["Mozilla/5.0",
                       "(Windows NT 10.0; Win64; x64)AppleWebKit/537.36",
                       "(KHTML, like Gecko)",
                       "Chrome/73.0.3683.86",
                       "Safari/537.36"]
        self.headers = {'User-Agent': " ".join(self.agents)}

    def scrap_meta_data(self, url: str) -> dict:
        data = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')
        og_description = soup.select_one('meta[property="og:description"]')

        return {"title": og_title['content'],
                "image": og_image['content'],
                'description': og_description['content']}