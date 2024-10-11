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

    translation_prompt = (prompt)

    inputs = tokenizer(translation_prompt, return_tensors="pt", padding=True)

    output = model.generate(**inputs, max_new_tokens=100)

    assistant_message = tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

    with st.chat_message("assistant"):
        st.markdown(assistant_message)

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
