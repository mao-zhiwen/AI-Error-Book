import requests

# 填写你的密钥
API_KEY = "ark-fd076f37-4604-4345-8574-c1c04980ec85-66355"
API_URL = "https://ark.cn-beijing.volces.com/api/v3/responses"
MODEL = "doubao-seed-1-8-251228"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL,
    "input": [
        {
            "role": "user",
            "content": [{"type": "input_text", "text": "你好"}]
        }
    ]
}

try:
    response = requests.post(API_URL, headers=headers, json=data, timeout=60)
    result = response.json()
    # 正确解析AI回复
    ai_reply = result["output"][1]["content"][0]["text"]
    print("✅ API调用成功！")
    print("AI回复：", ai_reply)
except Exception as e:
    print("解析错误：", e)