import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.chat_models import init_chat_model
# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent


load_dotenv()
api_key = os.environ.get('DEEPSEEK_API_KEY')

# client = OpenAI(api_key=api_key,base_url="https://api.deepseek.com")
model = init_chat_model(model="deepseek-chat", temperature=0.9)

# model = init_chat_model(model="gpt-3.5-turbo", model_provider='OpenAI', temperature=0.9, api_key=api_key, base_url="https://api.deepseek.com")


# model = ChatTongyi(model='qwen-max')

# response = model.invoke("你是谁？")
# print(response)

agent = create_agent(model=model)
agent = model.agent("deepseek-chat")   #非流式输出
response1 = agent.invoke({"messages":[{"role": "user", "content": "你是谁？"}]})
print(response1)


meg = agent.stream({'messages':[{"role": "user", "content": "你是谁？"}]},#流式输出
    stream_mode="messages")
for token, metdata in meg:
    if token.content:
        print(token.content, end="", flush=True)