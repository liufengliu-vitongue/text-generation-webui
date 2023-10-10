import json

import requests

from modules.aramus_question import Aramus_question


class AramusModel(object):
    def generate(self, question, state):
        
        new_question = Aramus_question.new_question(question,state)
        
        if len(new_question.strip()) == 0:
            greeting = state["greeting"]
            if len(greeting.strip()) == 0:
                greeting = "Please enter some content, so I can know what you want to know"
            return greeting

        print("request,question:", new_question)
        
        messages_list= state["history"]["internal"]
        messages_body=[]
        for chat_str in messages_list:
            messages_body.append(
                {
                    "role":"user",
                    "content":chat_str[0]
                }
            )
            messages_body.append(
                {
                    "role":"assistant",
                    "content":chat_str[1]
                }
            )

        # send url
        url = 'http://192.168.0.91:3006/aramus_chat'
        # url = "http://37.224.68.132:27006/aramus_chat"
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
                    'chat_input': new_question,
                    'messages': messages_body,
                    'user_info':{}
                }
        print("request data:",data)

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print("http status code:", response.status_code)
            print("http response:", response.content.decode('utf-8'))

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['response']
                print("answer",answer)
                print("chatbot http status code:", response.status_code)
                return answer

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# # # #
# # # # # # send question demo
# question = " failing to do so could also help in promoting the use of covers.\nYou: Can you detail the challenges and root causes that lead to buildings becoming abandoned, and hence contributing to visual pollution?\nAramus:"
# state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "repetition_penalty": 1.2, "ban_eos_token": False}
# result = model.generate(question, state)
# print(result)
