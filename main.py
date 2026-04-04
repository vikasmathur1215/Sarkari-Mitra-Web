
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
if "messages" not in st.session_state:
    st.session_state.messages = []
# Quick Buttons for User
st.write("---") # एक पतली लाइन
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Resume"):
        # यह बटन दबाते ही चैट में अपने आप लिखा जाएगा
        st.session_state.messages.append({"role": "user", "content": "मुझे एक जॉब के लिए प्रोफेशनल Resume बनाना है, मेरी मदद करो।"})
        st.rerun()

with col2:
    if st.button("🏠 Rent Draft"):
        st.session_state.messages.append({"role": "user", "content": "मुझे एक Rent Agreement का ड्राफ्ट बना कर दो।"})
        st.rerun()

with col3:
    if st.button("📜 Affidavit"):
        st.session_state.messages.append({"role": "user", "content": "मुझे एक सामान्य Affidavit का फॉर्मेट चाहिए।"})
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