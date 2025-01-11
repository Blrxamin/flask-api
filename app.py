import requests
from user_agent import generate_user_agent
from flask import Flask, request, jsonify

app = Flask(__name__)

url = "https://fadai-boma-bot-vtwo-pro.vercel.app/increase_visitors"
headers = {
    'authority': 'fadai-boma-bot-vtwo-pro.vercel.app',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://fadai-boma-bot-vtwo-pro.vercel.app',
    'referer': 'https://fadai-boma-bot-vtwo-pro.vercel.app/home',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': str(generate_user_agent()),
}

@app.route('/visit', methods=['GET'])
def increase_visitors():
    try:
        uid = request.args.get('id')
        
        if not uid:
            return jsonify({"error": "UID is required"}), 400
        
        visit = 1000
        
        for _ in range(10):
            data3 = {'text': f'{uid}@{visit}'}
            response = requests.post(url, headers=headers, json=data3)
            
            if response.status_code != 200:
                return jsonify({"error": f"Error sending visitors"}), response.status_code
        
        return jsonify({"message": f"10k visitors sent to the player: {uid}             BY API : BL_RX AND @V1P_YK"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
