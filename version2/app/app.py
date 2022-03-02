from base64 import encode
from tkinter import E
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup


class DB:
    def __init__(self) -> None:
        self.rows = [
            {
                "_id": "0",
                "title": "성장을 위한 기록장",
                "description": "프로그래밍 공부를 하며 습득한 정보와 회고를 기록하는 기술 블로그",
                "image": "https://tistory1.daumcdn.net/tistory/4516741/attach/ea4d2cd059eb42fda36d9a3989d5a401",
                "url": "https://choewy.tistory.com/",
                "comment": "내 블로그"
            },
            {
                "_id": "1",
                "title": "스파르타코딩클럽",
                "description": "왕초보 8주 완성! 웹/앱/게임 빠르게 배우고 내것을 만드세요!",
                "image": "https://static.spartacodingclub.kr/043a96e34c19/static/css/images/ogimage2.jpg?t=1633489494",
                "url": "https://spartacodingclub.kr/",
                "comment": "스파르타 코딩클럽"
            },
            {
                "_id": "2",
                "title": "네이버",
                "description": "네이버 메인에서 다양한 정보와 유용한 컨텐츠를 만나 보세요",
                "image": "https://s.pstatic.net/static/www/mobile/edit/2016/0705/mobile_212852414260.png",
                "url": "https://naver.com",
                "comment": "123"
            }
        ]
        self.len = len(self.rows)

    def load(self) -> None:
        return self.rows

    def push(self, row: dict) -> None:
        self.rows.append(row)
        self.len += 1

    def pop(self, idx: int) -> None:
        try:
            del self.rows[idx]
            self.len -= 1
        except Exception as e:
            print(e)


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


db = DB()
b_soup = BSoup()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles', methods=['GET'])
def read_memo():
    response = {'success': True}

    try:
        response['rows'] = db.load()
    except Exception as error:
        response['success'] = False
        response['error'] = str(error)
    finally:
        return jsonify(response)


@app.route('/article', methods=['POST'])
def post_memo():
    response = {'success': True}

    try:
        data = request.form
        url = data['url']
        meta = b_soup.scrap_meta_data(url)
        row = {
            '_id': str(db.len),
            'title': meta['title'],
            'description': meta['description'],
            'image': meta['image'],
            'url': url,
            'comment': data['comment']
        }
        db.push(row)
    except Exception as error:
        response['success'] = False
        response['error'] = str(error)
    finally:
        return jsonify(response)


@app.route("/delete", methods=["POST"])
def post_delete():
    response = {'success': True}
    try:
        data = request.form
        idx = int(data["_id"])
        db.pop(idx)
    except Exception as error:
        response['success'] = False
        response['error'] = str(error)
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
