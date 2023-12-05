from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

questions = [
    {"id": 1, "question": "What is your favorite color?"},
    {"id": 2, "question": "Who is your favorite character?"},
    {"id": 3, "question": "What genre is your favorite?"}
]


@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": questions})


if __name__ == '__main__':
    app.run(debug=True)
