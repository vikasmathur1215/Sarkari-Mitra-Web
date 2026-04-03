 model.generate_content(instruction)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # अगर अभी भी Quota का एरर आए, तो समझो गूगल बिलिंग अपडेट कर रहा है
            st.error(f"Error: {e}")
            st.info("विकाश भाई, एक बार 'Reboot app' बटन ज़रूर दबाएं।")
