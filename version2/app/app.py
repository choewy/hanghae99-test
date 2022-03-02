from base64 import encode
from tkinter import E
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup


class DB:
    def __init__(self) -> None:
        self.rows = [
            {
                "_id": "1",
                "title": "GitHub: Where the world builds software",
                "description": "GitHub is where over 73 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and feat...",
                "image": "https://github.githubassets.com/images/modules/site/social-cards/github-social.png",
                "url": "https://www.github.com/",
                "comment": "깃헙!"
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
