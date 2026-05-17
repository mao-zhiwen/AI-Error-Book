import requests
import time

# 你的豆包配置（已经填好你的密钥，不用改）
API_KEY = "ark-fd076f37-4604-4345-8574-c1c04980ec85-66355"
API_URL = "https://ark.cn-beijing.volces.com/api/v3/responses"
MODEL = "doubao-seed-1-8-251228"

def ai_chat(prompt, max_retries=3):
    """
    豆包AI对话接口（终极稳定版）
    超时180秒，自动重试3次，打印详细错误日志
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}]
            }
        ],
        "max_output_tokens": 2000  # 限制最大输出，避免超时
    }

    for attempt in range(max_retries):
        try:
            print(f"第{attempt+1}次调用AI...")
            response = requests.post(
                API_URL,
                headers=headers,
                json=data,
                timeout=180  # 超时拉到180秒，绝对够用
            )
            response.raise_for_status()
            result = response.json()
            
            # 正确解析豆包的返回格式
            ai_reply = result["output"][1]["content"][0]["text"]
            print("✅ AI调用成功！")
            return ai_reply
            
        except Exception as e:
            print(f"❌ 第{attempt+1}次调用失败: {str(e)}")
            if attempt < max_retries - 1:
                print(f"等待3秒后重试...")
                time.sleep(3)
    
    return "AI请求超时，请检查网络连接或稍后重试！"