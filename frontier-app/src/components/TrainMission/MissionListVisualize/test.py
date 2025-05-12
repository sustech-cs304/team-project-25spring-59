import requests

# 请求的 URL
url = "http://localhost:8000/generate-user-records"

# 请求体参数
payload = {
    "user_id": 1
}

# 请求头
headers = {
    "Content-Type": "application/json"
}

# 发送 POST 请求
try:
    response = requests.post(url, json=payload, headers=headers)

    # 打印响应状态码
    print(f"Status Code: {response.status_code}")

    # 打印返回的 JSON 数据
    try:
        response_data = response.json()
        print("Response JSON:")
        print(response_data)
    except ValueError:
        print("返回内容不是有效的 JSON：")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
