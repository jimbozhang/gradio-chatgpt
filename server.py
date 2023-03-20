import gradio as gr
from loguru import logger
from openai.error import AuthenticationError, RateLimitError

from chat_completion import ChatCompletion

bot = ChatCompletion(api_key_path='./openai_api_key')
logger.add('log.txt')

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(show_label=False)
    msg = gr.TextArea(show_label=False, placeholder='Say something to ChatGPT here ...')
    send_btn = gr.Button('Send')
    retry_btn = gr.Button('Retry')
    reset_btn = gr.Button('Reset')

    def send(user_message, history):
        if not user_message:
            return '', history

        logger.info(f'[MSG] {user_message}')

        try:
            response = bot.chat(user_message) if user_message != 'retry' else bot.retry()
        except AuthenticationError:
            response = '''Incorrect API key provided.
                You can find your API key at https://platform.openai.com/account/api-keys,
                and make sure it has been put in `./openai_api_key` of the server.'''
        except RateLimitError:
            response = '''openai.error.RateLimitError:
                That model is currently overloaded with other requests.
                You may want to try clicking the "retry" botton.'''

        logger.info(f'[ANS] {response}')
        return '', history + [[user_message, response]]

    def reset():
        bot.reset()
        logger.info('[RESET]')
        return '', [['', '']]

    def retry(history):
        return send('retry', history)

    send_btn.click(send, inputs=[msg, chatbot], outputs=[msg, chatbot],
                   show_progress=True, )
    reset_btn.click(reset, inputs=None, outputs=[msg, chatbot])
    retry_btn.click(retry, inputs=chatbot, outputs=[msg, chatbot])


demo.launch(share=False)
