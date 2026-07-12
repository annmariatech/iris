import requests
import time


BACKEND_URL = "http://localhost:5001/api/captions"


class CaptionSender:
    """
    Sends captions to the backend server.
    """

    def send(self, lecture_id, timestamp, text):

        payload = {
            "lectureId": lecture_id,
            "timestamp": timestamp,
            "text": text
        }

        try:

            response = requests.post(BACKEND_URL, json=payload)

            if response.status_code == 200 or response.status_code == 201:
                print("✅ Caption sent to backend.")

            else:
                print(f"⚠️ Backend returned {response.status_code}. Retrying...")

                time.sleep(2)

                response = requests.post(BACKEND_URL, json=payload)

                if response.status_code == 200 or response.status_code == 201:
                    print("✅ Caption sent successfully on retry.")

                else:
                    print(f"❌ Failed again ({response.status_code}).")

        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")