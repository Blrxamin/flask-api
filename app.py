from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# النقطة النهائية للـ Proxy API
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
            return jsonify({"error": "Failed to fetch data", "details": response.text}), response.status_code

        data = response.json()
        data['BY_API'] = "@BL_RX AND @V1P_YK"  # إضافة الرسالة المطلوبة

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)