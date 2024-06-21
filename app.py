import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
# from openai import OpenAI
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


openai_api_key = os.getenv('OPENAI_API_KEY')
# llm = OpenAI(openai_api_key=openai_api_key, temperature=0.9)#, model="gpt-3.5-turbo"
chat = ChatOpenAI(temperature=0)

# The slack app
slack_bot_key = os.getenv('SLACK_BOT_TOKEN')
app = App(token=slack_bot_key)

@app.message("")
def message_hello(message, say):
  messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content=message['text'])
  ]
  response = chat(messages)
  say(f"Hi, <@{message['user']}>! {response.content}")



if __name__ == '__main__':
  SocketModeHandler(app, os.environ.get('SLACK_APP_TOKEN')).start()