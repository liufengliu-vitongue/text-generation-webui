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

        print("qat5base new question:", new_question)
        # send url
        url = 'http://192.168.0.111:3588/predict'
        #url = "http://37.224.68.132:25588/predict"
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
                print("qat5base http status code:", response.status_code)
                return answer

        except Exception as e:
            print("post request error ：{0}".format(e))
            # 处理请求异常，返回空字符串或其他错误信息
            return "Sorry, the feature is not supported at the moment"

# # test
#model = AramusModel()
# # #
# # # # # send question demo
#question = "111233sdfsdf,sdfsad\nYou: What are the elements of 5 visual pollution categories?\nAramus:"
#state = {'max_new_tokens': 200, 'auto_max_new_tokens': False, 'seed': -1.0, 'temperature': 0.7, 'top_p': 0.9, 'top_k': 20, 'typical_p': 1, 'epsilon_cutoff': 0, 'eta_cutoff': 0, 'repetition_penalty': 1.15, 'repetition_penalty_range': 0, 'encoder_repetition_penalty': 1, 'no_repeat_ngram_size': 0, 'min_length': 0, 'do_sample': True, 'penalty_alpha': 0, 'num_beams': 1, 'length_penalty': 1, 'early_stopping': False, 'mirostat_mode': 0, 'mirostat_tau': 5, 'mirostat_eta': 0.1, 'add_bos_token': True, 'ban_eos_token': False, 'truncation_length': 2048, 'custom_stopping_strings': '', 'skip_special_tokens': True, 'stream': True, 'tfs': 1, 'top_a': 0, 'character_menu': 'None', 'history': {'internal': [], 'visible': []}, 'name1': 'You', 'name2': 'Aramus', 'greeting': '', 'context': 'This is a conversation with your Assistant. It is a computer program designed to help you with various tasks such as answering questions, providing recommendations, and helping with decision making. You can ask it anything you want and it will do its best to give you accurate and relevant information.', 'chat_generation_attempts': 1, 'stop_at_newline': False, 'mode': 'chat', 'instruction_template': 'None', 'name1_instruct': '', 'name2_instruct': '', 'context_instruct': '', 'turn_template': '', 'chat_style': 'cai-chat', 'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>', 'loader': 'Transformers', 'cpu_memory': 0, 'auto_devices': False, 'disk': False, 'cpu': False, 'bf16': False, 'load_in_8bit': False, 'trust_remote_code': False, 'load_in_4bit': False, 'compute_dtype': 'float16', 'quant_type': 'nf4', 'use_double_quant': False, 'wbits': 'None', 'groupsize': 'None', 'model_type': 'None', 'pre_layer': 0, 'triton': False, 'desc_act': False, 'no_inject_fused_attention': False, 'no_inject_fused_mlp': False, 'no_use_cuda_fp16': False, 'threads': 0, 'n_batch': 512, 'no_mmap': False, 'low_vram': False, 'mlock': False, 'n_gpu_layers': 0, 'n_ctx': 2048, 'n_gqa': 0, 'rms_norm_eps': 0, 'llama_cpp_seed': 0.0, 'gpu_split': '', 'max_seq_len': 2048, 'compress_pos_emb': 1, 'alpha_value': 1}
#result = model.generate(question, state)
#print(result)
