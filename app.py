"""
任务0： 这个代码是用来调用st(内置了前端界面的）快捷工具，前面是，页面标题设定，openai对象（api），初始化模型、初始化聊天信息（空列表），
根据聊天的role不同显示不同气泡，显示聊天内容。然后如果用户输入文本，执行：“把这段话翻译成中文，” 用户消息存入消息列表，展示用户消息。
接下来是生成助手回应，（assistant），调用openai进行翻译，（response ） model用定义的model，message是翻译成中文，然后保留上下文方便模型理解。
再展示AI回复的信息。

代码的requirements
1. pip install --upgrade streamlit (or st.chat_input must change to st.text_input, and chat_message change to st.markdown)
2. api_key, generated but openai付费（无法绑定大陆银行卡），所以改用huggingface模型（（ Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details.））
3. pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 # 我的是支持cuda版本
4. pip install transformers

一开始选择了HuggingFaceH4/zephyr-7b-beta 模型，发现模型过大。加载速度太慢(内存不足，pycharm卡住）。 但实现了翻译功能（由于大模型未进行微调，存在错误回复（它把拼音、繁体中文、台湾、简体中文都翻译了一遍）
            user: hello world system: Translate to simplified Chinese the provided text. Your response should be just the processed text. assistant: 你好，世界！
            原文：Hello, world!
            简化字：你好，世界！
            Pinyin：Nǐ hǎo, shìjiě!
            English: Hello, world!
            Simplified Chinese: 你好，世界！
            Traditional Chinese: 你好，世界！
            Taiwanese (Hokkien): 你好


后来 改成Helsinki-NLP/opus-mt-en-zh 专用英译中的模型。 然后表现的基本可以。 见图。
另外 这个网站Network url: 192.168.10.89 仅在局域网内生效。考虑像vercel那样生成一个外人可访问的公网连接。



扩展方向：1.速度。2.自行选择翻译语言。3.长度问题

"""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import streamlit as st

st.title("Chat-based Translation with huggingface")

# model_name = "HuggingFaceH4/zephyr-7b-beta"
model_name = "Helsinki-NLP/opus-mt-en-zh"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Please type in sentences to translate to Chinese."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

        # 在消息列表中添加 "system" 类型的消息，用于引导模型翻译
    translation_prompt = (prompt)

    # 使用 tokenizer 对对话进行编码
    inputs = tokenizer(translation_prompt, return_tensors="pt", padding=True)

    # 生成模型输出（翻译结果）
    output = model.generate(**inputs, max_new_tokens=100)

    # 解码生成的输出
    assistant_message = tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

    # 在前端显示模型生成的翻译结果
    with st.chat_message("assistant"):
        st.markdown(assistant_message)

    # 将模型的回复存储为 "assistant" 角色的消息
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
