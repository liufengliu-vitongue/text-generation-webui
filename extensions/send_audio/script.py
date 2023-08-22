import base64
from io import BytesIO
import gradio as gr
from modules import chat, shared
from modules.ui import gather_interface_values
from modules.utils import gradio
import os
from scipy.io import wavfile
from pydub import AudioSegment
import datetime;

input_hijack = {
    'state': False,
    'value': ["", ""]
}


def chat_input_modifier(text, visible_text, state):
    global input_hijack
    if input_hijack['state']:
        input_hijack['state'] = False
        return input_hijack['value']
    else:
        return text, visible_text

    


def generate_chat_audio(audio, name1, name2):
    file_path=audio
    # sample_rate,samples=audio
    # save_url="audio/"
    # ts_str = str(datetime.datetime.now().timestamp()*1000000)
    # file_name=ts_str+".wav"
    # file_name=ts_str+".mp3"
    # file_path = os.path.join(save_url, file_name)
    # wavbuffer = BytesIO()
    # wavfile.write(wavbuffer, sample_rate, samples)
    # wav
    # wavfile.write(file_path, sample_rate, samples)
    # audio_str=base64.b64encode(wavbuffer.getvalue()).decode('utf-8')
    # visible_text = f'<audio src="data:audio/wav;base64,{audio_str}" controls></audio>'
    # mp3
    # sound = AudioSegment.from_wav(wavbuffer)
    # mpegbuffer = BytesIO()
    # sound.export(mpegbuffer, format='mp3')

    f=open(file_path,'rb')
    audio_str=base64.b64encode(f.read()).decode('utf-8')
    f.close()
    # audio_str=base64.b64encode(mpegbuffer.getvalue()).decode('utf-8')
    # sound.export(file_path, format='mp3')
    visible_text = f'<audio src="data:audio/wav;base64,{audio_str}" controls></audio>'

    text = f'{file_path}'
    return text, visible_text


def ui():
    audio_select = gr.Audio(label='Send a audio',source="upload",type="filepath",format="wav")
    # Prepare the input hijack, update the interface values, call the generation function, and clear the audio
    audio_select.upload(
        lambda audio, name1, name2: input_hijack.update({
            "state": True,
            "value": generate_chat_audio(audio, name1, name2)
        }), [audio_select, shared.gradio['name1'], shared.gradio['name2']], None).then(
        gather_interface_values, gradio(shared.input_elements), gradio('interface_state')).then(
        chat.generate_chat_reply_wrapper, shared.input_params, gradio('display', 'history'), show_progress=False).then(
        lambda: None, None, audio_select, show_progress=False)
