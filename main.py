"""
2023年5月10日
stream接口最好海外服务器部署，测了一下，无法使用，本地+梯子是可以的

【注意】vercel限制了只能timeout 5秒，要么升级付费计划，所以大文本不能用vercel接口，要么改成stream？？？

ChatGpt聊天API使用 - 知乎
https://zhuanlan.zhihu.com/p/611009414

OpenAI API汇总(持续更新) - 朝花夕拾
http://www.melonkid.cn/20230402233348/94999478cd61/

flask中获取request的参数的方法_flask获取请求参数_无艳影的博客-CSDN博客
https://blog.csdn.net/wuyy0224/article/details/124396392

import requests
import json

url = "https://openai.putaojie.top/v1/chat/completions"

payload = {'text': '1+1等于几？用中文回答',
'model': 'gpt-3.5-turbo',
'password': 'your password',
'openai_key': 'your api key',
'max_tokens': '2048',
'temperature': '0.9'}

headers = {
  # 'Content-Type': 'application/json',
  'Authorization': 'Bearer sk-***Ak2'
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.text)
print(response.json())

"""
import flask
import requests
import json
from flask import Flask, render_template, request


app = Flask(__name__)
APP_VERSION = "1.0.0"
TIMEOUT = 180
api_passwords = ["ceM5TkvmZTQGpUr8qQWU", "5jNkLwn!UGmGbUBS58rU"]


@app.route('/')
def test():
    return 'openai'


@app.route('/test')
def aa():
    return 'ok'


@app.route('/version')
def version():
    return APP_VERSION


# post的request.form在vercel拿不到数据，但是不能删掉（删掉提示无法understand）！改成request.get_json()["role"]形式
@app.route('/v1/chat/completions', methods=["GET", "POST"])
def v1():
    password = request.form.get("password")
    text = request.form.get("text", default='hello')
    openai_key = request.form.get("openai_key", default='sk-***Gi')
    role = request.form.get("role", default='user')
    model = request.form.get("model", default="gpt-3.5-turbo")
    max_tokens = request.form.get("max_tokens", default=2048, type=int)
    temperature = request.form.get("temperature", default=0.9, type=float)

    params = request.get_json()
    password = params.get("password", None)
    text = params.get("text", 'hello')
    openai_key = params.get("openai_key", 'sk-***Gi')
    role = params.get("role", 'user')
    model = params.get("model", "gpt-3.5-turbo")
    max_tokens = int(params.get("max_tokens", 2048))
    temperature = float(params.get("temperature", 0.9))

    if password not in api_passwords:
        return "Password failed，请输入正确的密码"

    try:
        url = "https://api.openai.com/v1/chat/completions"

        payload = json.dumps({
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": role,
                    "content": text
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(openai_key)
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=TIMEOUT)
        res = response.json()
        res = json.dumps(res, ensure_ascii=False)
    except Exception as e:
        res = e.__str__()
    return res

if __name__ == "__main__":
    app.run()
