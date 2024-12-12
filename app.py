from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/visit', methods=['GET'])
def get_player_info():
    try:
        player_id = request.args.get('id')
        region = request.args.get('region', 'br')

        if not player_id:
            return jsonify({"error": "Player ID is required"}), 400

        url = f"https://api.bielnetwork.com.br/api/player_info?id={player_id}&region={region}"

        for _ in range(100):
            try:
                requests.get(url)
            except Exception as e:
                # تجاوز أي أخطاء أثناء إرسال الطلبات
                pass

        # إعادة رسالة ثابتة بعد إرسال الطلبات
        return jsonify({"message": "VISITORS HAVE BEEN SENT"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)