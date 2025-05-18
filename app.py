from flask import Flask, jsonify
from compiler import Compiler

app = Flask(__name__)

@app.route('/api/message')
def message():
    return jsonify({'message': 'Hello from the Flask backend!'})

@app.route('/api/compiler')
def compiler():
    return Compiler('a=b+c').compile()

if __name__ == '__main__':
    app.run(debug=True)
