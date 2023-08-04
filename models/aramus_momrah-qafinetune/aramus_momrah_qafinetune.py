import json

import requests

class AramusModel(object):
    def generate(self, question, state):
        word = "\nYou: "

        last_index = question.rfind(word)
        new_str = question[last_index: -1]
        new_question = new_str.split(word)[1]

        print("request,question:", new_question, "state:", state)

        # send url
        url = 'http://192.168.0.16:3334/QApairs'
        #url = "http://37.224.68.132:24334/QApairs"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {'pairs': new_question}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print("http status code:", response.status_code)
            print("http response:", response.content.decode('utf-8'))

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['answer']
                print("qafinetune http status code:", response.status_code)
                return answer

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# #
# # # # send question demo
# question = "\nYou: May Public toilets cause visual pollution?"
# #state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "repetition_penalty": 1.2, "ban_eos_token": False}
# #result = model.generate(question, state)
# #print(result)
