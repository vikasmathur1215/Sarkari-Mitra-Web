import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में API Key नहीं मिली!")
    st.stop()

st.title("🤖 @TheSarkariMitra - Model Checker")

# 2. उपलब्ध मॉडल्स की लिस्ट चेक करना
st.write("विकाश भाई, आपके प्रोजेक्ट के लिए ये मॉडल्स उपलब्ध हैं:")

try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            st.code(m.name) # स्क्रीन पर नाम दिखाएगा
            
    if available_models:
        st.success(f"कुल {len(available_models)} मॉडल्स मिल गए!")
        # सबसे पहला वर्किंग मॉडल चुनना
        selected_model = available_models[0]
        st.info(f"हम ऑटोमैटिकली '{selected_model}' इस्तेमाल करेंगे।")
    else:
        st.warning("कोई भी मॉडल नहीं मिला। कृपया बिलिंग चेक करें।")

except Exception as e:
    st.error(f"चेक करने में गलती हुई: {e}")

# 3. टेस्टिंग चैट (ताकि तुरंत पता चल जाए)
if prompt := st.chat_input("अब यहाँ कुछ लिखकर टेस्ट करें..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(available_models[0])
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"जवाब देने में दिक्कत: {e}")
