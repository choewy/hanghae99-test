from flask import Flask, render_template, jsonify, request
from src.utils.bsoup import BSoup
from src.utils.mongo import MongoDB
from dotenv import load_dotenv
import os


load_dotenv()
port = os.environ.get("FLASK_PORT")
uri = os.environ.get("MONGO_URI")
mongodb = MongoDB(uri)
b_soup = BSoup()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles', methods=['GET'])
def read_memo():
    response = {'success': True}

    try:
        response['rows'] = mongodb.find_many()
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


@app.route('/article', methods=['POST'])
def post_memo():
    response = {'success': True}

    try:
        data = request.form
        url = data['url']
        meta = b_soup.scrap_meta_data(url)

        mongodb.insert_one({
            'title': meta['title'],
            'description': meta['description'],
            'image': meta['image'],
            'url': url,
            'comment': data['comment']
        })
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


@app.route("/delete", methods=["POST"])
def post_delete():
    response = {'success': True}

    try:
        data = request.form
        _id = data['_id']
        mongodb.delete_one(_id)
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=int(port), debug=True)