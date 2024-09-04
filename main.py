import base64
import streamlit as st
import requests

# Streamlit UI
st.title("Text to Speech Converter")

url = "https://model-4w79lm13.api.baseten.co/development/predict"
headers={"Authorization": f"Api-Key {st.secrets.get('api_key')}"}
auth_key = st.secrets.get("auth_key")


# Text input field
access_token = st.text_input("Enter access token:")
text_input = st.text_area("Enter your text here:", height=150)
file_selector = st.file_uploader("Upload a reference audio file", type=["wav"])

# Button to send request
if st.button("Convert to Speech"):
    if auth_key == access_token:
        if text_input:
            try:
                with st.spinner("Converting text to speech..."):
                    file_data = file_selector.read()
                    encoded_data = base64.b64encode(file_data)
                    encoded_str = encoded_data.decode("utf-8")
                        
                    data = {"text": text_input, "audio_ref": encoded_str, "top_p": 0.001}

                    # Sending the request to the API
                    response = requests.post(url, headers=headers, json=data, timeout=30)
                    print("response done")
                    # Check if the response is successful
                    if response.status_code == 200:
                        audio_data = base64.b64decode(response.json()['result'])
                        # print(audio_data)
                        print("making audio element")
                        # Play the received audio data
                        st.audio(audio_data, format='audio/mp3')

                    else:
                        st.error(f"Error: {response.status_code} - {response.text}, please try again")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter some text to convert.")
    else:
        st.warning("Invalid access token. Please make sure it is correct as what was given.")
