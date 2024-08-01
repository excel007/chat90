import streamlit as st
import requests
import json

def main():
    st.title("Chat with LLAMA3.1")
    st.caption("_Model ที่นำมาใช้งาน ได้แก่ Ollama + llama3.1 70b")
    st.divider()

    # Initialize session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Use Streamlit chat input to get user input
    prompt = st.chat_input("พิมพ์ข้อความที่นี่")

    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Perform assistant action 
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in assistant_action(prompt):
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def assistant_action(prompt):
    #url = "http://localhost:11434/api/chat" #retrieve from secret
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.1",  # or whichever model you're using
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    with requests.post(url, headers=headers, data=json.dumps(data), stream=True) as r:
        for line in r.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'message' in json_response:
                    content = json_response['message']['content']
                    yield content

if __name__ == "__main__":
    main()
