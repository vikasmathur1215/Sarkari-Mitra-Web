import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("System Error: API Key missing.")
    st.stop()

# 2. Session State Initialize (Isse AttributeError khatam hoga)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. UI Setup
st.set_page_config(page_title="Sarthi AI", page_icon="🧭")
st.title("Sarthi AI")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.write("दस्तावेज़ों और सरकारी प्रक्रियाओं को समझना अब हुआ आसान।")

# 4. Quick Buttons
st.write("---") 
col1, col2, col3 = st.columns(3)
button_prompt = None

with col1:
    if st.button("📄 Resume"):
        button_prompt = "मुझे एक प्रोफेशनल Resume बनाना है, मेरी मदद करो।"
with col2:
    if st.button("🏠 Rent Draft"):
        button_prompt = "मुझे एक Rent Agreement का ड्राफ्ट बना कर दो।"
with col3:
    if st.button("📜 Affidavit"):
        button_prompt = "मुझे एक सामान्य Affidavit का फॉर्मेट चाहिए।"

# बटन दबाने पर AI जवाब देगा
if button_prompt:
    st.session_state.messages.append({"role": "user", "content": button_prompt})
    # AI Response Trigger
    system_msg = "तुम Sarthi AI हो—एक भरोसेमंद सहायक। जवाब सरल Hinglish और पॉइंट्स में दो।"
    response = model.generate_content(f"{system_msg}\n\nUser: {button_prompt}")
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_msg = "तुम Sarthi AI हो। सरल Hinglish और पॉइंट्स में जवाब दो।"
            response = model.generate_content(f"{system_msg}\n\nयूजर का सवाल: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("माफ़ी चाहता हूँ, अभी सिस्टम थोड़ा बिज़ी है।")
