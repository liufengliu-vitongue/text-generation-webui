import json

import requests


class Aramus_question:

    @staticmethod
    def new_question(question, state):

        print("org request:", question)
        you_name = state['name1']
        bot_name = state['name2']

        print("you_name:", you_name, "bot_name:", bot_name)

        word = f"\n{you_name}: "
        word_bot = f"\n{bot_name}:"

        last_index = question.rfind(word)
        you_question = question[last_index:]
        new_question_bot = you_question.split(word)[1]

        new_question = new_question_bot

        print("last_question :", new_question)
        if new_question.__contains__(word_bot):
            # last you or bot by bot chat numbers
            bot_chat_num = new_question.count(bot_name)
            print("bot_chat_num", bot_chat_num)

            if bot_chat_num == 1:
                new_question = new_question.replace(word_bot, "")
            else:
                new_question = ""

        return new_question

    def translate_language(question,source_lang):

        from_language = "eng_Latn"
        to_language = "arb_Arab"

        if source_lang == "ar":
            from_language = "arb_Arab"
            to_language = "eng_Latn"

        print("request,question:", question)

        # send url
        url = 'http://192.168.0.175:3030/translate/NLLB'
        #url = 'http://37.224.68.132:26030/translate/NLLB'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {'ori_text': question,"source_language":from_language,"target_language":to_language}

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

