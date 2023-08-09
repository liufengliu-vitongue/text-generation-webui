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
