from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hp_lvl', methods=['GET'])
def get_player_info():
    return jsonify({"message": "hp نيك امك"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)