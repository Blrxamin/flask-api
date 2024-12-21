from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

cookies = {
    'source': 'mb',
    '_gid': 'GA1.2.1236421304.1706295770',
    '_gat_gtag_UA_137597827_4': '1',
    'session_key': 'hnl4y8xtfe918iiz2go67z85nsrvwqdn',
    '_ga': 'GA1.2.1006342705.1706295770',
    'datadome': '3AmY3lp~TL1WEuDKCnlwro_WZ1C6J66V1Y0TJ4ITf1Hvo4833Fh4LF3gHrPCKFJDPUPoXh2dXQHJ_uw0ifD8jmCaDltzE5T3zzRDbXOKH9rPNrTFs29DykfP3cfo7QGy',
    '_ga_R04L19G92K': 'GS1.1.1706295769.1.1.1706295794.0.0.0',
}

headers = {
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://shop.garena.sg',
    'Referer': 'https://shop.garena.sg/app/100067/idlogin',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'x-datadome-clientid': 'DLm2W1ajJwdv~F~a_1d_1PyWnW6ns7GY5ChVcZY3HJ9r6D29661473aQaL2~3Nfh~Vf3m7rie7ObIb1_3eRN7J0G6uFZhMq5pM2jA828fE1dS7rZ7H3MWGQ5vGraAQWd',
}

def get_player_info(UID):
    json_data = {
        'app_id': 100067,
        'login_id': UID,
        'app_server_id': 0,
    }
    response = requests.post('https://shop.garena.sg/api/auth/player_id_login', cookies=cookies, headers=headers, json=json_data)
    return response.json()

def check_account_status(player_id):
    url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/plain, */*",
        'authority': "ff.garena.com",
        'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
        'referer': "https://ff.garena.com/en/support/",
        'sec-ch-ua': "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'x-requested-with': "B6FksShzIgjfrYImLpTsadjS86sddhFH",
    }
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/check_banned', methods=['GET'])
def player_details():
    player_id = request.args.get('player_id')
    if not player_id:
        return jsonify({"error": "Please provide a player_id parameter."}), 400
    
    try:
        player_info = get_player_info(player_id)
        nickname = player_info.get('nickname', 'Unknown')
        region = player_info.get('region', 'Unknown')
        
        account_status = check_account_status(player_id)
        is_banned = account_status.get('data', {}).get('is_banned', 0)
        status_text = "NOT BANNED" if is_banned == 0 else "BANNED"
        
        response_data = {
            "player_name": nickname,
            "region": region,
            "status": status_text,
            "player_id": player_id
        }
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
