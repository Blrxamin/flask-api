from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def get_player_info():
    try:
        # الحصول على ID اللاعب من الطلب
        player_id = request.args.get('id')
        region = request.args.get('region', 'br')  # المنطقة الافتراضية 'br'

        # التحقق من أن ID اللاعب موجود
        if not player_id:
            return jsonify({"error": "Player ID is required"}), 400

        # استدعاء واجهة برمجة التطبيقات الأصلية للحصول على معلومات اللاعب
        url = f"https://api.bielnetwork.com.br/api/player_info?id={player_id}&region=me"
        response = requests.get(url)

        # التحقق من أن الطلب إلى واجهة برمجة التطبيقات الأصلية نجح
        if response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch data from the original API",
                "details": response.text
            }), response.status_code

        # الحصول على البيانات القادمة من واجهة برمجة التطبيقات الأصلية
        player_data = response.json()

        # إضافة رسالة "DEV BY API" في أسفل الاستجابة
        player_data["DEV"] = 'BY API @BL_RX AND @V1P_YK'

        # إعادة البيانات بصيغة JSON مرتبة
        return jsonify(player_data), 200

    except Exception as e:
        # إرجاع خطأ داخلي في حالة حدوث استثناء
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)