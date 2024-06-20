import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

app = App(token=os.environ.get('SLACK_BOT_TOKEN'))

@app.message("")
def message_hello(message, say):
  response = process_message(message['text'])
  say(f"Hi, <@{message['user']}>! {response}")


def process_message(txt):
  client = OpenAI()
# client.api_key = os.getenv('OPENAI_API_KEY')
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are an efficient assistant."},
      {"role": "user", "content": txt}
    ]
  )
  return (completion.choices[0].message)


if __name__ == '__main__':
  SocketModeHandler(app, os.environ.get('SLACK_APP_TOKEN')).start()