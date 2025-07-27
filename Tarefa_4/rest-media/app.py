from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calcular-media', methods=['POST'])
def calcular_media():
    data = request.get_json()
    nota1 = float(data.get('nota1'))
    nota2 = float(data.get('nota2'))

    media = round((nota1 * 2 + nota2 * 3) / 5, 2)
    return jsonify({'media': media})

if __name__ == '__main__':
    app.run(port=5000)