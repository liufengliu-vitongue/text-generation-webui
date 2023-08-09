import json

import requests
from langdetect import detect

from models.aramus_question import Aramus_question


class AramusModel(object):
    def generate(self, question, state):
        new_question = Aramus_question.new_question(question,state)

        if len(new_question.strip()) == 0:
            greeting = state["greeting"]
            if len(greeting.strip()) == 0:
                greeting = "Please submit the text you wish to have translated"
            return greeting

        print("request,question:", new_question)

        from langdetect import DetectorFactory
        DetectorFactory.seed = 0

        source_lang = detect(new_question)
        source_language = "eng_Latn"
        target_language = "arb_Arab"

        if source_lang == "ar":
            source_language = "arb_Arab"
            target_language = "eng_Latn"

        # 判断语言种类
        print(detect(new_question))

        print("request,question:", new_question, "state:", state)

        # send url
        url = 'http://192.168.0.16:3004/translate/NLLB'
        #url = 'http://37.224.68.132:24004/translate/NLLB'
        headers = {
            'Content-Type': 'application/json',
        }


        data = {'ori_text': new_question,"source_language":source_language,"target_language":target_language}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print("http status code:", response.status_code)
            print("http response:", response.content.decode('utf-8'))

            if response.status_code == 200:
                # 解析响应数据
                output = response.json()
                answer = output['response']
                print("qafinetune http status code:", response.status_code)
                return answer

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
# model = AramusModel()
# # #
# # # # # send question demo
# question = "\nYou: May Public toilets cause visual pollution?"
# state = {"temperature": 0.8, "top_p": 0.9, "top_k": 500, "repetition_penalty": 1.2, "ban_eos_token": False}
# result = model.generate(question, state)
# print(result)
