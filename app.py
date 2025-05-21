from flask import Flask, jsonify,request
from compiler import Compiler
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/message')
def message():
    return jsonify({'message': 'Hello from the Flask backend!'})

@app.route('/',methods=["POST"])
def compiler():
    if request.method == "POST":
        data = request.get_json()
        statement = data.get('text')
        if not statement:
            return jsonify({'error': 'No statement provided'}), 400
        compiler = Compiler(statement)
        result = compiler.compile()
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
