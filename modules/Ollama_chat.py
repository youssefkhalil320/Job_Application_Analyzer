import json
import httpx

# url = "http://localhost:11435/api/generate"

# data = {
#     "model": "llama3",
#     "prompt": "why is the sky blue?"
# }

# response = httpx.post(url, data=json.dumps(data), headers={
#                       'Content-Type': 'application/json'})
# response_lines = [line for line in response.text.strip().split('\n') if line]
# response_dicts = [json.loads(line) for line in response_lines]
# print(''.join(response_dict.get('response', '')
#       for response_dict in response_dicts))

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests
from fastapi.testclient import TestClient

app = FastAPI(debug=True)


class Itemexample(BaseModel):
    name: str
    prompt: str
    instruction: str
    is_offer: Union[bool, None] = None


class Item(BaseModel):
    model: str
    prompt: str


urls = ["http://localhost:11435/api/generate"]

headers = {
    "Content-Type": "application/json"
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat/{llms_name}")
def update_item(llms_name: str, item: Item):
    if llms_name == "llama3":
        url = urls[0]
        payload = {
            "model": "llama3",
            "prompt": "Why is the sky blue?",
            "stream": False
        }
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))
        if response.status_code == 200:
            return {"data": response.text, "llms_name": llms_name}
        else:
            print("error:", response.status_code, response.text)
            return {"item_name": item.model, "error": response.status_code, "data": response.text}
    return {"item_name": item.model, "llms_name": llms_name}


# Using TestClient to call the endpoint and print the response
client = TestClient(app)

# Define the payload
payload = {
    "model": "llama3",
    "prompt": "Why is the sky blue?"
}

# Make the POST request
response = client.post("/chat/llama3", json=payload)

# Print the response
print(response.json())
