
import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("System Error: API Key missing.")
    st.stop()

# 2. Engine Setup (Gemini 2.5)
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Modern UI Setup (बिना किसी स्टाइल एरर के)
st.set_page_config(
    page_title="TheSarkariMitra", 
    page_icon="🤝",
    layout="centered"
)

# Header Section
st.title("Sarthi AI")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.write("दस्तावेज़ों और सरकारी प्रक्रियाओं को समझना अब हुआ आसान।")

# 4. Chat History
# --- Quick Buttons (Is hisse ko line 29 se 49 tak replace karein) ---
st.write("---") 
col1, col2, col3 = st.columns(3)

# बटन दबाने पर क्या एक्शन लेना है, उसके लिए एक वेरिएबल
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

# अगर कोई बटन दबाया गया है, तो उसे चैट इनपुट की तरह इस्तेमाल करें
if button_prompt:
    st.session_state.messages.append({"role": "user", "content": button_prompt})
    with st.chat_message("user"):
        st.markdown(button_prompt)
    
    with st.chat_message("assistant"):
        # यहाँ एआई को कॉल किया जा रहा है
        system_msg = "तुम Sarthi AI हो। सरल Hinglish में जवाब दो।"
        response = model.generate_content(f"{system_msg}\n\nUser: {button_prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & Friendly Response
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    # यूजर का सवाल दिखाना
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # एआई का दोस्ताना जवाब
    with st.chat_message("assistant"):
        try:
            
            system_msg = (
                "तुम 'Sarthi AI' हो—एक भरोसेमंद और विनम्र डिजिटल सहायक। "
                "जवाब बहुत ही सरल Hinglish और पॉइंट्स (1, 2, 3) में दो। "
                "कोशिश करो कि जवाब एकदम सीधा, सटीक और मददगार हो।" 
           ) 

            response = model.generate_content(f"{system_msg}\n\nयूजर का सवाल: {prompt}")

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error("माफ़ी चाहता हूँ, अभी सिस्टम थोड़ा बिज़ी है।") 