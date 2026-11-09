from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from ipywidgets import FileUpload
from ipython.display import display
import base64


upload = FileUpload(accept='D:\develop\pyhton pd\1.ai应用实例\images\image_1.jpg', multiple=False)
display(upload)
print(upload.value)
uploaded_file = upload.value[0]
content_mv = uploaded_file['content']
img_bytes = bytes(content_mv)
img_bs4 = base64.b64decode(img_bytes).decode('utf-8')



# @tool
# def get_wteather(location: str) -> str:
#     """获取天气信息"""
#     return f"{location}的天气晴朗，温度25度。"

# agent = create_agent(model="deepseek-chat" , tools=[get_wteather])
# response = agent.invoke({"messages":[

#     SystemMessage(content="你是一个ai"),
#     HumanMessage(content="我是你爹"),
#     AIMessage(content="--"),
#     HumanMessage(content="深圳天气怎么样")
#     ]})

# # print(response)
# for message in response["messages"]:
#     message.pretty_print()



# model = init_chat_model(model="deepseek-chat",
#                         model_provider='openai',
#                         base_url="https://api.deepseek.com",
#                         api_key=os.environ.get('DEEPSEEK_API_KEY'))

# agent = create_agent(model=model)   
# message = HumanMessage([
#         {"type": "text", "text": "描述一下图片"},
#         {"type": "image", "url": "D:\develop\pyhton pd/1.ai应用实例\images\image_1.jpg"}
#         ])

# stream = agent.stream({"messages":[message]},
#                       stream_mode="messages") #流式输出
# for chunk, metadata in stream:
#     if chunk.content:
#         print(chunk.content, end="", flush=True)



moltimodal_quesion = HumanMessage(content=[
    {"type": "image",
    "base64": img_bs4,
    "mime_type": "./1.ai应用实例\images\jpg",},
    {"type": "text", "text": "描述一下图片"}])

for chunk, metadata in agent.stream(
    {"messages":[moltimodal_quesion]},
    stream_mode="messages"):
    print(chunk.content, end="", flush=True)

