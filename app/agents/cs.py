from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage, AIMessageChunk, AIMessage
from langchain.chat_models import init_chat_model
import os
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


from app.common.logger import logger

model = init_chat_model(
    model = 'qwen3.5-plus',
    model_provider = 'openai',
    base_url =os.getenv('DASHSCOPE_BASE_URL'),
    api_key = os.getenv('DASHSCOPE_API_KEY'),

)







from langchain_tavily import TavilySearch
web_sh = TavilySearch(
    max_results = 5,
    topic = 'general',
)
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# connection = sqlite3.connect('rs/ps_c.db', check_same_thread = False)
# checkp = SqliteSaver(connection)
# checkp.setup()

checkpointer = SqliteSaver(sqlite3.connect("db/ps_c.db", check_same_thread=False))
# 自动建表
checkpointer.setup()


from langchain.agents import create_agent
sys_p = "你是坤坤"

agent = create_agent(
    model = model,
    tools = [web_sh],
    system_prompt = sys_p,
    checkpointer = checkpointer,
)





# 流式对话
async def search_recipes(prompt: str, image: str, thread_id: str):
    """调用agent搜索食谱"""
    logger.info(f"[用户]: {prompt}, image: {image}, thread_id: {thread_id}")
    try:
        # 判断是否有图片，封装不同格式的消息
        if not image or image.strip() == "":
            message = HumanMessage(content=prompt)
        else:
            message = HumanMessage(content=[
                {"type": "image", "url": image},
                {"type": "text", "text": prompt}
            ])

        # 流式调用Agent
        for chunk, metadata in agent.stream(
            {"messages": [message]},
            {"configurable": {"thread_id": thread_id}},
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield chunk.content

    except Exception as e:
        logger.error(f"\n[错误]: {str(e)}")
        yield "信息检索失败，试试看手动输入食物列表？"

# 清空会话
def clear_messages(thread_id: str):
    """清空会话"""
    logger.info(f"清空历史消息，thread_id: {thread_id}")
    checkpointer.delete_thread(thread_id)

# 查询会话历史
def get_messages(thread_id: str) -> list[dict[str, str]]:
    """获取会话历史"""
    logger.info(f"获取历史消息，thread_id: {thread_id}")

    # 根据 thread_id 查询 checkpoint
    checkpoint = checkpointer.get({"configurable": {"thread_id": thread_id}})

    # 如果不存在，返回空列表
    if not checkpoint:
        return []

    # 安全获取 messages
    channel_values = checkpoint.get("channel_values")
    if not channel_values:
        return []

    messages = channel_values.get("messages", [])
    if not messages:
        return []

    # 转换消息格式
    result = []
    for msg in messages:
        if not msg.content:
            continue

        if isinstance(msg, HumanMessage):
            result.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            result.append({"role": "assistant", "content": msg.content})

    return result





# 本地试跑脚本：只在直接执行本文件时运行，被 import（例如启动 Web 服务）时跳过
if __name__ == "__main__":
    from langchain.messages import HumanMessage

    mm_m = HumanMessage([
        {'type':'text',"text":"给我挑一个"},
        {"type":'image',"url":"--"},
    ])
    config = {'configurable':{"thread_id":"thread_1"}}

    resp = agent.invoke({"messages":[mm_m]},config)
    for message in resp["messages"]:
        message.pretty_print()
    resp = agent.invoke({
        'messages':[HumanMessage(content="说详细点")]},config
        )
    for message in resp['messages']:
        message.pretty_print()