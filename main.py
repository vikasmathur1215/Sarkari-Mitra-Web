import streamlit as st
import google.generativeai as genai

# 1. API Setup (Nayi Key yaha automatically connect hogi)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 'gemini-1.5-flash' sabse fast aur stable hai
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API Setup Error: {e}")
else:
    st.error("Secrets में नई चाबी नहीं मिली भाई!")
    st.stop()

# 2. UI Setup (Professional Look)
st.set_page_config(page_title="Sarthi AI", page_icon="🧭", layout="centered")

st.title("Sarthi AI 🧭")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.caption("Developed by Vikas Mathur (Unknown_shayar1215)")

# 3. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input & Response
if prompt := st.chat_input("भाई/बहन, यहाँ अपना सवाल पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sarthi AI Dimag (Personalized Hinglish)
            system_msg = (
                "तेरा नाम 'Sarthi AI' है और तुझे विकास माथुर ने बनाया है। "
                "तू एकदम Hinglish में बात कर। यूजर के अंदाज़ से पहचान कि वो लड़का है या लड़की। "
                "लड़के को 'भाई' और लड़की को 'बहन' बोल। जवाब बहुत ही दोस्ताना और पॉइंट्स में दे।"
            )
            
            response = model.generate_content(f"{system_msg}\n\nUser: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Asli bimari yaha dikhegi agar abhi bhi error aaye
            st.error(f"ओह! गूगल ने ये कहा है भाई: {e}")
