### 任务0： 
这个代码是用来调用st(内置了前端界面的）快捷工具，前面是，页面标题设定，openai对象（api），初始化模型、初始化聊天信息（空列表），
根据聊天的role不同显示不同气泡，显示聊天内容。然后如果用户输入文本，执行：“把这段话翻译成中文，” 用户消息存入消息列表，展示用户消息。
接下来是生成助手回应，（assistant），调用openai进行翻译，（response） model用定义的model，message是翻译成中文，然后保留上下文方便模型理解。
再展示AI回复的信息。
### 任务1：
调试代码中，首先要升级steamlit，否则有些方法会报错。
1. pip install --upgrade streamlit (or st.chat_input must change to st.text_input, and chat_message change to st.markdown)
2. 解决openai的api_key。生成后发现openai报错，权限问题。（无法绑定大陆银行卡导致这个问题不可修复），所以改用huggingface模型（（ Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details.））
3. pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 # 我的是支持cuda版本
4. pip install transformers

调试过程中，
一开始选择了HuggingFaceH4/zephyr-7b-beta 模型，发现模型过大。加载速度太慢(内存不足，pycharm卡住）。
但实现了翻译功能（由于大模型未进行微调，存在错误回复（它把拼音、繁体中文、台湾、简体中文都翻译了一遍）

    user: hello world system: Translate to simplified Chinese the provided text. Your response should be just the processed text. assistant: 你好，世界！
    原文：Hello, world!
    简化字：你好，世界！
    Pinyin：Nǐ hǎo, shìjiě!
    English: Hello, world!
    Simplified Chinese: 你好，世界！
    Traditional Chinese: 你好，世界！
    Taiwanese (Hokkien): 你好


后来 改成Helsinki-NLP/opus-mt-en-zh 专用英译中的模型。 然后表现的可以接受。

### 任务2：
这个网站Network url: xxx 仅在局域网内生效（或者localhost)。考虑像vercel那样生成一个外部可访问的公网连接。从vercel和streamlit cloud中，
选择streamlit cloud部署。

### 任务3：
包括github搞一个repo：xxx
在streamcloud里面：xxx做成一个应用，
生成中国内部可以访问的 xxx  可以输入英文翻译成中文。

### 任务4：扩展方向，暂未完成
1. 访问速度（目前大陆可访问，但是速度较慢）。
2. 自行选择翻译语言（目前是输入中文会翻译错误）。
3. 翻译的准确度有待提高（需微调模型）。
4. 嵌入其他应用或网页中（扩展）。