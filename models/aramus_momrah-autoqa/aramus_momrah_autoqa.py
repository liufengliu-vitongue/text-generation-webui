import json

import requests


class AramusModel(object):
    def generate(self, question, state):
        word = "\nYou: "
        word_bot = "\nAramus:"

        print("org request question:", question)

        last_index = question.rfind(word)
        new_str = question[last_index: -1]
        new_question_bot = new_str.split(word)[1]

        bot_index = new_question_bot.rfind(word_bot)
        new_question = new_question_bot[0: bot_index]

        print("request,question:", new_question)

        # send url
        url = 'http://192.168.0.48:3941/momrah_gpt/visual_pollution_qa'

        #url = 'http://37.224.68.132:23941/momrah_gpt/visual_pollution_qa'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {'question': new_question}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print("autoqa http status code:", response.status_code)

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['answer']

                print("autoqa http answer:", answer)
                return answer
            else: return 'system error'

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# #
# # # send question demo
# question = "\nYou: May Public toilets cause visual pollution?"
# state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "repetition_penalty": 1.2, "ban_eos_token": False}
# result = model.generate(question, state)
# print(result)
