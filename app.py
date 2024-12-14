from flask import Flask, request, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

# دالة غير متزامنة لإرسال الطلبات
async def send_request(session, url, i, results):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # استخراج المعلومات المطلوبة فقط
                player_info = {
                    "accountId": data.get("basicInfo", {}).get("accountId", "Unknown"),
                    "nickname": data.get("basicInfo", {}).get("nickname", "Unknown"),
                    "level": data.get("basicInfo", {}).get("level", "Unknown")
                }
                results.append(player_info)  # تخزين بيانات اللاعب
            else:
                results.append({"request": i + 1, "status": "Failed"})
    except Exception as e:
        results.append({"request": i + 1, "error": str(e)})

# المسار الرئيسي
@app.route('/visit', methods=['GET'])
def visit():
    player_id = request.args.get('id')
    region = request.args.get('region', 'br')
    
    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    # الرابط الخاص بالـ API
    url = f"https://api.bielnetwork.com.br/api/player_info?id={player_id}&region={region}"

    # إعداد النتائج
    results = []

    # إرسال 1000 طلب باستخدام asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_async_requests():
        async with aiohttp.ClientSession() as session:
            tasks = [send_request(session, url, i, results) for i in range(1000)]
            await asyncio.gather(*tasks)

    loop.run_until_complete(run_async_requests())

    # استخراج أول نتيجة إذا كانت ناجحة
    if results:
        player_info = results[0] if isinstance(results[0], dict) else {}
        account_id = player_info.get("accountId", "Unknown")
        nickname = player_info.get("nickname", "Unknown")
        level = player_info.get("level", "Unknown")
    else:
        account_id = nickname = level = "Unknown"

    # إرجاع رسالة بعد إرسال 1000 طلب مع المعلومات المطلوبة فقط
    return jsonify({
        "message": f"1000 visitors sent to player with ID {player_id} from region {region}!",
        "accountId": account_id,
        "nickname": nickname,
        "level": level,
        "DEV_API": "@BL_RX AND @V1P_YK"  # إضافة الرسالة من الأسفل
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 