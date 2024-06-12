import json
import httpx

url = "http://localhost:11435/api/generate"

data = {
    "model": "llama3",
    "prompt": "why is the sky blue?"
}

response = httpx.post(url, data=json.dumps(data), headers={
                      'Content-Type': 'application/json'})
response_lines = [line for line in response.text.strip().split('\n') if line]
response_dicts = [json.loads(line) for line in response_lines]
print(''.join(response_dict.get('response', '')
      for response_dict in response_dicts))
