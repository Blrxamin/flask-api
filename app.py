from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

url = "https://api.bielnetwork.com.br/api/player_info"

# Function to send 1000 requests to the API
def send_visitors(player_id):
    for _ in range(1000):
        try:
            response = requests.get(url, params={"id": player_id, "region": "me"})
            if response.status_code != 200:
                print(f"Error while sending: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

@app.route('/visit', methods=['GET'])
def visit_player():
    player_id = request.args.get('id')

    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    response = requests.get(url, params={"id": player_id, "region": "me"})
    if response.status_code == 200:
        data = response.json()
        basic_info = data.get("basicInfo", {})
        player_name = basic_info.get("nickname", "Unknown")
        level = basic_info.get("level", "Unknown")

        # Start the process to send 1000 requests in the background
        threading.Thread(target=send_visitors, args=(player_id,)).start()

        # Respond to the user immediately
        return jsonify({
            "player_name": player_name,
            "level": level,
            "message": "1000 visitors started. BY API : @BL_RX AND @V1P_YK"
        })
    else:
        return jsonify({"error": f"Failed to fetch player data: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)