import requests
import time
import hashlib
import base64
import yaml

from flask import Flask, request, jsonify, Response

def load_yaml(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = yaml.full_load(f)
        return data

def save_yaml(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        yaml.dump(data, f)

app = Flask(__name__)

@app.route('/v2/voice', methods=['GET'])
def get_voice():
    '''
    Using Vbee API TTS to get .wav voice file.

    # Required Params:

    voice:
    • hn_male_xuantin_vdts_48k-hsmm: Giọng nam Miền Bắc
    • hn_female_xuanthu_news_48k-hsmm: Giọng nữ Miền Bắc
    • hn_female_thutrang_phrase_48k-hsmm: Giọng nữ Miền Bắc
    • sg_male_xuankien_vdts_48k-hsmm: Giọng nam Miền Nam
    • sg_female_xuanhong_vdts_48k-hsmm: Giọng nữ Miền Nam

    # Optional Params

    rate: range from 0.1 to 1.9
    '''

    # Check Bearer Token for authorization
    if request.headers['Authorization'] != 'Bearer ' + BEARER_TOKEN:
        return Response("Access Denied !")

    TIME = time.time()
    MD5_KEY = hashlib.md5(f"{PRIVATE_KEY}:{APP_ID}:{TIME}".encode()).hexdigest()

    data = request.json

    input_text = data['input_text']
    voice = "hn_male_xuantin_vdts_48k-hsmm" if 'voice' not in data else data['voice']

    params = {
        # required
        "input_text": input_text,
        "voice": voice,
        "app_id": APP_ID,
        "time": TIME,
        "key": MD5_KEY,
        "user_id": USER_ID,

        # optional
        # "rate": 1.0,
        # "service_type": 1,
        # "input_type": "text",
        # "audio_type": "wav",
        # "bit_rate": 128000,
        # "sample_rate": 48000
    }

    params.update(data)

    if len(input_text) < 1000:
        response = requests.get(API_URL, params=params, timeout=300)
    else:
        response = requests.post(API_URL, params=params, timeout=300)

    if response.status_code == 200:
        
        b64_string = base64.b64encode(response.content).decode('utf-8')

        # with open('voice.wav', 'wb') as f:
        #     f.write(base64.b64decode(b64_string))
        return jsonify({
            "audio": b64_string
            })
    else:
        return jsonify({})

if __name__ == '__main__':
    config = load_yaml('config.yaml')

    BEARER_TOKEN = config['bearer_token']
    API_URL = config['api_url']
    APP_ID = config['app_id']
    USER_ID = config['user_id']
    PRIVATE_KEY = config['private_key']
    
    app.run(debug=True, threaded=True)