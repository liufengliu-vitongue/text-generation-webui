import json
from pathlib import Path

import gradio as gr
import torch

from modules import shared


with open(Path(__file__).resolve().parent / '../css/main.css', 'r') as f:
    css = f.read()
with open(Path(__file__).resolve().parent / '../css/chat.css', 'r') as f:
    chat_css = f.read()
with open(Path(__file__).resolve().parent / '../css/main.js', 'r') as f:
    main_js = f.read()
with open(Path(__file__).resolve().parent / '../css/chat.js', 'r') as f:
    chat_js = f.read()
with open(Path(__file__).resolve().parent / '../css/save_files.js', 'r') as f:
    save_files_js = f.read()

refresh_symbol = '🔄'
delete_symbol = '🗑️'
save_symbol = '💾'

theme = gr.themes.Base(
    primary_hue="yellow",
    secondary_hue="yellow",
    neutral_hue="slate",
    font=['Helvetica', 'ui-sans-serif', 'system-ui', 'sans-serif'],
    font_mono=['IBM Plex Mono', 'ui-monospace', 'Consolas', 'monospace'],
).set(
    body_background_fill='#f9f7f2',
    body_text_color_subdued='#1d1f22',
    background_fill_primary='#f3efe5',
    background_fill_secondary='#f3efe5',
    button_border_width='1px',
    button_large_padding='14px',
    button_large_radius='24px',
    button_small_padding='10px',
    button_small_radius='20px',
    button_primary_background_fill='#b89535',
    button_primary_background_fill_hover='#ebc03f',
    button_primary_border_color='#7e6216',
    button_primary_border_color_hover='#ebc03f',
    button_primary_text_color='#ffffff',
    button_secondary_background_fill='#ffffff',
    button_secondary_background_fill_hover='#ebc03f',
    button_secondary_border_color='#eeeeee',
    button_secondary_border_color_hover='#ebc03f',
    button_cancel_background_fill='#ffffff',
    button_cancel_background_fill_hover='#ebc03f',
    button_cancel_border_color='#eeeeee',
    button_cancel_border_color_hover='#ebc03f',
    checkbox_background_color='#ffffff',
    checkbox_border_color='#f5df9f',
    input_background_fill='#ffffff',
    input_border_color='#eeeeee',
    input_border_width='1px',
    slider_color='#f5df9f',
    table_odd_background_fill='#f3efe5',
)


def list_model_elements():
    elements = [
        'loader',
        'cpu_memory',
        'auto_devices',
        'disk',
        'cpu',
        'bf16',
        'load_in_8bit',
        'trust_remote_code',
        'load_in_4bit',
        'compute_dtype',
        'quant_type',
        'use_double_quant',
        'wbits',
        'groupsize',
        'model_type',
        'pre_layer',
        'triton',
        'desc_act',
        'no_inject_fused_attention',
        'no_inject_fused_mlp',
        'no_use_cuda_fp16',
        'threads',
        'n_batch',
        'no_mmap',
        'low_vram',
        'mlock',
        'n_gpu_layers',
        'n_ctx',
        'n_gqa',
        'rms_norm_eps',
        'llama_cpp_seed',
        'gpu_split',
        'max_seq_len',
        'compress_pos_emb',
        'alpha_value'
    ]

    for i in range(torch.cuda.device_count()):
        elements.append(f'gpu_memory_{i}')

    return elements


def list_interface_input_elements():
    elements = [
        'max_new_tokens',
        'auto_max_new_tokens',
        'seed',
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'do_sample',
        'penalty_alpha',
        'num_beams',
        'length_penalty',
        'early_stopping',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'add_bos_token',
        'ban_eos_token',
        'truncation_length',
        'custom_stopping_strings',
        'skip_special_tokens',
        'stream',
        'tfs',
        'top_a',
    ]

    if shared.args.chat:
        elements += [
            'character_menu',
            'history',
            'name1',
            'name2',
            'greeting',
            'context',
            'chat_generation_attempts',
            'stop_at_newline',
            'mode',
            'instruction_template',
            'name1_instruct',
            'name2_instruct',
            'context_instruct',
            'turn_template',
            'chat_style',
            'chat-instruct_command',
        ]
    else:
        elements.append('textbox')
        if not shared.args.notebook:
            elements.append('output_textbox')

    elements += list_model_elements()
    return elements


def gather_interface_values(*args):
    output = {}
    for i, element in enumerate(list_interface_input_elements()):
        output[element] = args[i]

    if not shared.args.multi_user:
        shared.persistent_interface_state = output

    return output


def apply_interface_values(state, use_persistent=False):
    if use_persistent:
        state = shared.persistent_interface_state

    elements = list_interface_input_elements()
    if len(state) == 0:
        return [gr.update() for k in elements]  # Dummy, do nothing
    else:
        return [state[k] if k in state else gr.update() for k in elements]


class ToolButton(gr.Button, gr.components.IOComponent):
    """
    Small button with single emoji as text, fits inside gradio forms
    Copied from https://github.com/AUTOMATIC1111/stable-diffusion-webui
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_block_name(self):
        return "button"


def create_refresh_button(refresh_component, refresh_method, refreshed_args, elem_class):
    """
    Copied from https://github.com/AUTOMATIC1111/stable-diffusion-webui
    """
    def refresh():
        refresh_method()
        args = refreshed_args() if callable(refreshed_args) else refreshed_args

        for k, v in args.items():
            setattr(refresh_component, k, v)

        return gr.update(**(args or {}))

    refresh_button = ToolButton(value=refresh_symbol, elem_classes=elem_class)
    refresh_button.click(
        fn=refresh,
        inputs=[],
        outputs=[refresh_component]
    )

    return refresh_button


def create_delete_button(**kwargs):
    return ToolButton(value=delete_symbol, **kwargs)


def create_save_button(**kwargs):
    return ToolButton(value=save_symbol, **kwargs)
