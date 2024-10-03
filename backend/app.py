from flask import Flask, request, jsonify, send_from_directory
from openai_assistant import OpenAIAssistant
from dotenv import load_dotenv
from cat_api import CatAPI

load_dotenv()
app = Flask(__name__, static_folder='../frontend', static_url_path='')

openai_assistant = OpenAIAssistant()
cat_api = CatAPI()

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = openai_assistant.get_response(user_input)
    return jsonify({'response': response})

@app.route('/get_cat', methods=['GET'])
def get_cat():
    breed = request.args.get('breed', default=None)
    limit = request.args.get('limit', default=1, type=int)
    cats = cat_api.get_cats(breed, limit)
    return jsonify({'cats': cats})

if __name__ == '__main__':
    app.run(debug=True)