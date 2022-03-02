from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import json
import os

app_file = os.path.abspath(__file__)
dir_name = os.path.dirname(app_file).replace("\\", "/")


class DB:
    def __init__(self) -> None:
        self.path = {
            "seq": dir_name + '/seq.json',
            "db": dir_name + '/db.json'
        }

    def get_seq(self) -> dict:
        try:
            with open(self.path["seq"], "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(e)
            return {"seq": 0}

    def set_seq(self, seq: int) -> None:
        try:
            with open(self.path["seq"], "w", encoding="utf-8") as file:
                json.dump({"seq": seq}, file, ensure_ascii=False)

        except Exception as e:
            print(e)
            return []

    def get_db(self) -> list:
        try:
            with open(self.path["db"], "r", encoding="utf-8") as file:
                return list(json.load(file))
        except Exception as e:
            print(e)
            return []

    def set_db(self, rows: list) -> None:
        try:
            with open(self.path["db"], "w", encoding="utf-8") as file:
                json.dump(rows, file, ensure_ascii=False)
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
        response['rows'] = db.get_db()
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
        rows = db.get_db()
        seq = db.get_seq()["seq"]
        row = {
            '_id': str(seq),
            'title': meta['title'],
            'description': meta['description'],
            'image': meta['image'],
            'url': url,
            'comment': data['comment']
        }
        rows.append(row)
        db.set_db(rows)
        db.set_seq(seq+1)
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
        _id = data["_id"]
        rows = db.get_db()
        rows = list(filter(lambda row: row["_id"] != _id, rows))
        db.set_db(rows)
    except Exception as error:
        response['success'] = False
        response['error'] = str(error)
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
