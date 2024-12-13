from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/player_info', methods=['GET'])
def get_player_info():
    try:
        player_id = request.args.get('id')
        region = request.args.get('region', 'br')

        if not player_id:
            return jsonify({"error": "Player ID is required"}), 400

        url = f"https://api.bielnetwork.com.br/api/player_info?id={player_id}&region={region}"

        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from the original API", "details": response.text}), response.status_code

        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)