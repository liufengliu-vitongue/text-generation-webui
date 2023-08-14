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

        new_question_en = Aramus_question.translate_language(new_question, "ar")


        # send url
        url = 'http://192.168.0.111:3000/api/query'
        #url = 'http://37.224.68.132:24007/api/query'

        data = {'query': new_question_en}

        try:
            response = requests.post(url, data=data, timeout=(30, 60))
            print("http status code:", response.status_code)
            print("http response:", response.content.decode('utf-8'))

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['answer']
                answer_ar = Aramus_question.translate_language(answer, "en")

                print("incontextgpt_ar http answer:", answer_ar)
                return answer_ar

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# # # #
# # # # # # send question demo
# question = "\nYou: May Public toilets cause visual pollution? \nAramus: "
# state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "repetition_penalty": 1.2, "ban_eos_token": False}
# result = model.generate(question, state)
# print(result)
