import requests
import logging
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[logging.StreamHandler()])

class FreeFireVisitorBot:
    def __init__(self, url, max_workers=100):
        self.url = url
        self.max_workers = max_workers
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_requests = 0
        self.failed_responses = []

    def send_request(self, id_value, attempt):
        try:
            response = requests.get(f"{self.url}{id_value}")
            self.total_requests += 1
            if response.status_code == 200:
                self.successful_requests += 1
                print(f"\r{colored(f'Requests Sent: {self.total_requests} | Successful: {self.successful_requests} | Failed: {self.failed_requests}', 'green')}", end="")
            else:
                self.failed_requests += 1
                self.failed_responses.append((attempt + 1, response.status_code))
                print(f"\r{colored(f'Requests Sent: {self.total_requests} | Successful: {self.successful_requests} | Failed: {self.failed_requests}', 'yellow')}", end="")
        except requests.RequestException as e:
            self.failed_requests += 1
            self.failed_responses.append((attempt + 1, str(e)))
            print(f"\r{colored(f'Requests Sent: {self.total_requests} | Successful: {self.successful_requests} | Failed: {self.failed_requests}', 'red')}", end="")

    def execute_requests(self, id_value, max_requests=1000):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.send_request, id_value, i) for i in range(max_requests)]
            for future in futures:
                future.result()

    def get_summary(self):
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "failed_responses": self.failed_responses
        }

@app.route('/info', methods=['GET'])
def info():
    id_value = request.args.get('id')

    if not id_value:
        return jsonify({"error": "Player ID is required"}), 400

    api_url = "https://info-api-rzx-team-seven.vercel.app/info?id="
    visitor_bot = FreeFireVisitorBot(api_url, max_workers=100)

    visitor_bot.execute_requests(id_value, max_requests=1000)

    summary = visitor_bot.get_summary()

    return jsonify({
        "message": "Requests completed successfully",
        "summary": summary
    })

if __name__ == "__main__":
    app.run(debug=True)