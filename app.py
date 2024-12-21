from flask import Flask, jsonify, request
import requests
import time
import threading

app = Flask(__name__)

def get_player_info(player_id):
    url = f"https://scaninfo.net/infofreefire/{player_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to retrieve player information. Please try again later."}

def send_requests_in_background(player_id):
    for i in range(1000):
        print(f"Sending request number: {i+1}")
        result = get_player_info(player_id)
        time.sleep(1)
    print("Successfully sent 1000 visitors!")

@app.route('/visit', methods=['GET'])
def send_requests():
    player_id = request.args.get('player_id')
    
    if not player_id:
        return jsonify({"error": "Player ID is required!"}), 400
    
    player_data = get_player_info(player_id)
    
    if "error" in player_data:
        return jsonify(player_data), 400

    player_name = player_data.get("Account Name", "Unknown")
    server = player_data.get("Account Region", "Unknown")
    player_id_actual = player_data.get("Account UID", "Unknown")

    response_data = {
        "message": "1000 visitors are being sent...",
        "player_info": {
            "name": player_name,
            "server": server,
            "id": player_id_actual
        }
    }

    thread = threading.Thread(target=send_requests_in_background, args=(player_id,))
    thread.daemon = True
    thread.start()

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)
