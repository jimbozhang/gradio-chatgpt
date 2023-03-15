import linecache
from typing import Optional, List, Dict

import openai


class ChatCompletion:
    def __init__(self, model: str = 'gpt-3.5-turbo',
                 api_key: Optional[str] = None, api_key_path: str = './openai_api_key'):
        if api_key is None:
            openai.api_key = api_key
            api_key = linecache.getline(api_key_path, 2).strip('\n')
            if len(api_key) == 0:
                raise EnvironmentError
        openai.api_key = api_key

        self.model = model
        self.system_messages = []
        self.user_messages = []

    def chat(self, msg: str, setting: Optional[str] = None, model: Optional[str] = None) -> str:
        if setting is not None:
            self.system_messages.append(setting)
        self.user_messages.append(msg)

        return self._run(model)

    def retry(self, model: Optional[str] = None) -> str:
        return self._run(model)

    def reset(self):
        self.system_messages.clear()
        self.user_messages.clear()

    def _make_message(self) -> List[Dict]:
        sys_messages = [{'role': 'system', 'content': msg} for msg in self.system_messages]
        user_messages = [{'role': 'user', 'content': msg} for msg in self.user_messages]
        return sys_messages + user_messages

    def _run(self, model: Optional[str] = None) -> str:
        if model is None:
            model = self.model
        response = openai.ChatCompletion.create(model=model, messages=self._make_message())
        return response['choices'][0]['message']['content']
