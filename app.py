from flask import Flask, request, jsonify
import requests
import asyncio
import aiohttp

app = Flask(__name__)

url = "https://api.bielnetwork.com.br/api/player_info"

# Function to send 1000 requests asynchronously
async def send_visitors(player_id):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(1000):
            tasks.append(fetch_data(session, player_id))
        await asyncio.gather(*tasks)

# Function to fetch the player data
async def fetch_data(session, player_id):
    try:
        async with session.get(url, params={"id": player_id, "region": "me"}) as response:
            if response.status != 200:
                print(f"Error while sending: {response.status}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/visit', methods=['GET'])
def visit_player():
    player_id = request.args.get('id')

    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    # Fetch player data synchronously first
    response = requests.get(url, params={"id": player_id, "region": "me"})
    if response.status_code == 200:
        data = response.json()
        basic_info = data.get("basicInfo", {})
        player_name = basic_info.get("nickname", "Unknown")
        level = basic_info.get("level", "Unknown")

        # Run the 1000 visitors task asynchronously using asyncio.run() to create the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_visitors(player_id))

        return jsonify({
            "player_name": player_name,
            "level": level,
            "message": "1000 visitors started. BY API : @BL_RX AND @V1P_YK"
        })
    else:
        return jsonify({"error": f"Failed to fetch player data: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)