import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import os
import openai
from st_copy_to_clipboard import st_copy_to_clipboard
# Function to transcribe audio segments
def dotflo_ai(prompt, token=2048):
    print("Asking GPT")
    #print(prompt)
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "This is a poem in hindi, convert it into multi line like a poem and only return the poem results. Give proper punctuation"+prompt}],max_tokens=token)

    generated_text = response.choices[0]['message']['content']

    return generated_text

def transcribe_audio_segments(audio_file_path):
    # Load audio using pydub
    audio = AudioSegment.from_file(audio_file_path)

    # Define segment duration in milliseconds (10 seconds in this example)
    segment_duration = 10000

    # Split audio into segments
    segments = []
    for start_time in range(0, len(audio), segment_duration):
        end_time = start_time + segment_duration
        segment = audio[start_time:end_time]
        segments.append(segment)

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Transcribe each segment
    transcriptions = []
    for i, segment in enumerate(segments):
        # Export segment as temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            segment.export(temp_file.name, format="wav")
            with sr.AudioFile(temp_file.name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="hi-IN")
                transcriptions.append(text)
        os.remove(temp_file.name)  # Delete temporary file after use

    # Combine transcriptions into a single result
    full_transcription = " ".join(transcriptions)
    return full_transcription

# Streamlit app
def main():
    st.title("👩 ✍️ NJ's Audio Transcriber")

    # File upload
    uploaded_file = st.file_uploader("Upload an audio file (.m4a, .mp3, .wav)")

    if uploaded_file is not None:
        # Process when file is uploaded
        st.write("File uploaded successfully:")
        st.audio(uploaded_file)

        # Temporarily save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            st.success("File saved temporarily")

            # Transcribe audio segments
            st.write("Transcribing audio...")
            transcription_result = transcribe_audio_segments(temp_file.name)

            # Display transcription result
            finaltext=dotflo_ai(transcription_result)
            st.subheader("Transcription Result:")
            st_copy_to_clipboard(finaltext)
            st.text_area("Transcription", finaltext, height=200, key="transcription_result")
         
           

    else:
        st.info("Please upload an audio file")

if __name__ == "__main__":
    main()
