
# Model setup with System Instruction
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="तुम एक सरकारी सहायक 'TheSarkariMitra' हो। सरकारी योजनाओं और आधार कार्ड जैसे कामों के बारे में सरल हिंदी में सटीक जानकारी दो।"
)

# ... baaki code ...

if prompt := st.chat_input("अपनी समस्या यहाँ लिखें..."):
    # ...
    with st.chat_message("assistant"):
        try:
            # Ab sirf prompt bhejna kafi hai kyunki system instruction upar de di hai
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # ...
