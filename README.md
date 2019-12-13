# vbee_api

## Installation and Usage
### Install requirements
```
pip3 install -r requirements.txt
```
### Setup
- **Step 1**: Copy `sample_config.yaml` to `config.yaml`.
- **Step 2**: Edit `config.yaml` to include your private_key and app_id.

### Usage

#### Run server
```
python3 vbee_api_server.py
```

#### Send request
```
curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" <api_url>/v2/voice -d {"input_text": "insert your text here !"}
```

**Response**:
```json
{
    "audio": ${base64_string}
}

```

**Write to file**
```python
with open('voice.wav', 'wb') as f:
    f.write(base64.b64decode(b64_string))
```