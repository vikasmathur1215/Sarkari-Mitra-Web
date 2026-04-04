import streamlit as st
import google.generativeai as genai

# 1. API Setup (Isme ab hum error detail bhi dekhenge)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API Setup Error: {e}")
else:
    st.error("Secrets में API Key नहीं मिली भाई!")
    st.stop()

# 2. Page Setup
st.set_page_config(page_title="Sarthi AI", page_icon="🧭")

# 3. Instruction
system_instruction = (
    "तेरा नाम 'Sarthi AI' है और तुझे विकास माथुर ने बनाया है। "
    "एकदम Hinglish में 'भाई/बहन' बोलकर जवाब दे।"
)

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input & Response
if prompt := st.chat_input("भाई/बहन, यहाँ सवाल पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Asli error yaha dikhega
            st.error(f"Error: {e}")
