from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data for questions and answers
questions = [
    {"id": 1, "question": "What is your favorite color?", "variants": ["blue", "green", "red", "pink"]},
    {"id": 2, "question": "Who is your favorite character?", "variants": ["Killua", "Gon", "Kurapika", "Hisoka"]}
]


@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": questions})


if __name__ == '__main__':
    app.run(debug=True)
