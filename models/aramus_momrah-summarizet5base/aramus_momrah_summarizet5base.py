import json

import requests

from models.aramus_question import Aramus_question


class AramusModel(object):
    def generate(self, question, state):
        new_question = Aramus_question.new_question(question,state)

        if len(new_question.strip()) == 0:
            greeting = state["greeting"]
            if len(greeting.strip()) == 0:
                greeting = "Please enter some content, so I can know what you want to know"
            return greeting

        print("request,question:", new_question)

        # send url
        url = 'http://192.168.0.111:3578/summarize'
        #url = "http://37.224.68.132:24009/summarize"
        headers = {
            'Content-Type': 'application/json',
        }


        data = {'question': new_question}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print("http status code:", response.status_code)
            print("http response:", response.content.decode('utf-8'))

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['Answer']
                print("qafinetune http status code:", response.status_code)
                return answer

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# # # #
# # # # # # send question demo
# question = "\nYou: There are several damaged vehicles left on our streets. It never looks good and reduces public space. What is the plan to address this? First Round of Reasoning: Abandoned or damaged vehicles on streets are a form of visual pollution. This might occur because owners avoid removing their vehicles due to cost or lack of awareness.Second Round of Reasoning: The national plan proposes solutions like defining scopes and service level agreements  with traffic authorities, increasing fines, raising community awareness, clarifying guidelines for vehicle removal, developing a rebate scheme, and applying escalating consequences for non-compliance"
# state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "repetition_penalty": 1.2, "ban_eos_token": False}
# result = model.generate(question, state)
# print(result)
