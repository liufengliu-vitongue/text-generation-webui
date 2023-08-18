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

        print("qafalcon7b-ar new question:", new_question)

        # send url
        url = 'http://192.168.0.111:3788/generate'
        #url = "http://37.224.68.132:25788/generate"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {'question': new_question}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data),timeout=(30, 60))
            print("http status code:", response.status_code)
            print("http response:", response.content.decode('utf-8'))

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['answer']
                print("qafalcon7b-ar answer:", answer)
                return answer

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# # # # #
# # # # # # # send question demo
# question = "\nYou: هل يمكن للشارع غير النظيف أن يسبب التلوث البصري؟ \nAramus:"
# state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "name1":"You", "name2":"Aramus", "repetition_penalty": 1.2, "ban_eos_token": False}
# result = model.generate(question, state)
# print(result)

