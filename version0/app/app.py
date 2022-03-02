from flask import Flask, render_template, jsonify, request
from utils.mongo import MongoDB
from utils.bsoup import BSoup

db = MongoDB()
b_soup = BSoup()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles', methods=['GET'])
def read_memo():
    response = {'success': True}

    try:
        response['rows'] = db.find_many()
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
        doc = {
            'title': meta['title'],
            'description': meta['description'],
            'image': meta['image'],
            'url': url,
            'comment': data['comment']
        }
        db.insert_one(doc)
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
        db.delete_one(_id)
    except Exception as error:
        response['success'] = False
        response['error'] = str(error)
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
