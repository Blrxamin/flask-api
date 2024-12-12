from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/visit', methods=['GET'])
def get_player_info():
    try:
        # الحصول على معرّف اللاعب والمنطقة من المعاملات في الاستعلام
        player_id = request.args.get('id')
        region = request.args.get('region', 'br')

        # التأكد من وجود معرّف اللاعب
        if not player_id:
            return jsonify({"error": "Player ID is required"}), 400

        # بناء عنوان URL الخاص بالـ API
        url = f"https://api.bielnetwork.com.br/api/player_info?id={player_id}&region={region}"

        # إرسال 100 طلب إلى الـ API
        for _ in range(100):
            try:
                response = requests.get(url, timeout=10)  # إضافة مهلة للاتصال
                # طباعة استجابة الـ API للمساعدة في تتبع الأخطاء
                print(f"Request Response: {response.status_code} - {response.text}")
            except requests.exceptions.Timeout:
                print("Request timed out.")
            except requests.exceptions.RequestException as e:
                # طباعة تفاصيل الخطأ في حال حدوثه
                print(f"Error during request: {e}")
        
        # إعادة رسالة ثابتة بعد إرسال الطلبات
        return jsonify({"message": "VISITORS HAVE BEEN SENT"}), 200

    except Exception as e:
        # معالجة أي أخطاء أخرى قد تحدث
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # تشغيل تطبيق Flask
    app.run(port=5000, debug=True)