import argparse

import gradio as gr
from loguru import logger

from chat_completion import ChatCompletion

parser = argparse.ArgumentParser()
parser.add_argument('--api_key_path', type=str, default='./openai_api_key')
parser.add_argument('--log_path', type=str, default='./log.txt')
parser.add_argument('--share', action='store_true', default=False)
parser.add_argument('--welcome', type=str, default='Say something to ChatGPT here ...')
parser.add_argument('--title', type=str, default='ChatGPT')
parser.add_argument('--setting', type=str, default=None)
args = parser.parse_args()

bot = ChatCompletion(api_key_path=args.api_key_path)
logger.add(args.log_path)

with gr.Blocks(title=args.title) as demo:
    chatbot = gr.Chatbot(show_label=False)
    msg = gr.TextArea(show_label=False, placeholder=args.welcome)
    send_btn = gr.Button('Send')
    retry_btn = gr.Button('Retry')
    reset_btn = gr.Button('Reset')

    def send(user_message, history):
        if not user_message:
            return '', history

        logger.info(f'[MSG] {user_message}')
        response = bot(user_message, setting=args.setting) if user_message != 'retry' else bot.retry()
        logger.info(f'[ANS] {response}')
        return '', history + [[user_message, response]]

    def reset():
        bot.reset()
        logger.info('[RESET]')
        return '', [['', '']]

    def retry(history):
        return send('retry', history)

    send_btn.click(send, inputs=[msg, chatbot], outputs=[msg, chatbot], show_progress=True)
    reset_btn.click(reset, inputs=None, outputs=[msg, chatbot])
    retry_btn.click(retry, inputs=chatbot, outputs=[msg, chatbot])


demo.launch(share=args.share)
