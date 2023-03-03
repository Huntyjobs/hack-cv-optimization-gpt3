import os
from datetime import datetime, timedelta
from cachetools import TTLCache, cached
import openai

ctl_data = TTLCache(maxsize=1024, ttl=timedelta(hours=24), timer=datetime.now)


@cached(cache=ctl_data)
class Conversation:
    base_array = [{"role": "system", "content": "You are a helpful assistant."}]

    def __init__(
        self,
    ):
        self.chat_array = self.base_array
        self.response = ""

    def conversation_int(self, prompt):
        new_message = {"role": "user", "content": prompt}
        if self.response == "":
            self.chat_array = self.chat_array + [new_message]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.chat_array
            )
            self.response = completion
        else:
            old_response = {
                "role": "assistant",
                "content": self.response["choices"][0]["message"]["content"],
            }
            self.chat_array = self.chat_array + [old_response, new_message]
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.chat_array
            )
            self.response = completion

        return completion
