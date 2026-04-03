import streamlit as st
import google.generativeai as genai

# 1. API Setup (सुरक्षित तरीके से)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Please add it in Streamlit Secrets.")
    st.stop()

# 2. मॉडल को थोड़ा 'Instructions' देना ताकि वो बेहतर समझे
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 @TheSarkariMitra")
st.write("आपका डिजिटल सरकारी सहायक।")

# 3. याददाश्त (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट स्क्रीन पर दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. यूज़र का सवाल लेना
if prompt := st.chat_input("कैसे मदद कर सकता हूँ?"):
    # यूज़र का मैसेज स्क्रीन पर दिखाना
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI का जवाब तैयार करना
    with st.chat_message("assistant"):
        try:
            # हम AI को बता रहे हैं कि उसे कैसे जवाब देना है
            full_prompt = f"तुम एक सरकारी सहायक 'Sarkari Mitra' हो। इस सवाल का सरल हिंदी में जवाब दो: {prompt}"
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.write("माफ़ कीजिये, मैं समझ नहीं पाया। कृपया दोबारा पूछें।")
                
        except Exception as e:
            # अगर कोई एरर आए तो उसे साफ़ भाषा में दिखाना
            st.error("Google AI अभी थोड़ा बिजी है। कृपया 5 सेकंड रुक कर दोबारा मैसेज करें।")
            print(f"Error: {e}")
