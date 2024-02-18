import streamlit as st
import os
from textblob import TextBlob
from dotenv import load_dotenv
from gtts import gTTS
load_dotenv()
import requests
from io import BytesIO
import google.generativeai as genai 
from PIL import Image
import pyttsx3
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def generate_audio(text, language):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust the speed as needed
    engine.setProperty('voice', 'te' if language == 'Telugu' else 'en')  # Set the voice based on language

    audio_filename = "response.wav"
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()

    # Read the audio file as bytes
    with open(audio_filename, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return audio_bytes
def input_image_process(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[{
            "mime_type":uploaded_file.type,
            "data":bytes_data
            }]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
st.set_page_config("Health Adivisor App")
st.header("Calorie Advisor")
uploaded_file=st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True) 
    image_data=input_image_process(uploaded_file)

age=(st.text_input("Mention your age"))
if age!="":
    age=int(age)
    
language_options = ["English", "Telugu"]
language_choice = st.radio("Choose language:", language_options)

submit1=st.button("Tell me about total colories")

submit2=st.button("Discover Balanced Alternatives")


input_prompt1=f"""you are a good classifier which means you first need to
            verify if the provided image contains food or not.
            If the image does not contain food you need to give a response like
            Thank you for submitting the image. It seems like the image may not contain any food items. 
            We apologize for any inconvenience caused. Please upload another image containing food items, and we'll be happy to assist you further.  
            otherwise act like a nutritionist where you need to see the food items from the image
            and calculate the total calories, also provide the details of
            every food items with calories intake in below format

            1. Item1 - no of calories
            2. Item 2 - no of calories
            -----
            -----
            Finally you can also mention whether the food is healthy or not based on the user's age 
            user's age:{age} 
            and also mention the percentage split of the ratio of carbohydrates,fats,fibers,sugar and things required in our diet.
            Note: Ensure that to provide consistent calorie information for the same food image across multiple analyses"""


input_prompt2="""
you are a good classifier which means you first need to
     verify if the provided image contains food or not.
             If the image contains food acts as a nutritionist where you need to provide personalized dietary recommendations to promote balanced nutrition.When analyzing uploaded food images,consider suggesting food items that are rich in macronutrients which may be lacking in the uploaded image.Output a list top 10 items names only
    which should be included in the diet to balance that macronutrient else ask the user to upload a proper food image"""



if submit1:
    response=get_gemini_response(input_prompt1,image_data)
    if language_choice == "Telugu":
        response = TextBlob(response).translate(from_lang="en", to="te")  # Translate if Telugu

    st.header(f"{'ప్రతిస్పందన:' if language_choice == 'Telugu' else 'The Response is:'}")
    st.write(response)
    audio_bytes = generate_audio(response, language_choice)  # Generate audio
    #st.audio(audio_bytes, format="audio/mp3", caption="Listen to Response")
    st.audio(audio_bytes, format="audio/mp3")
    #st.audio(audio_bytes, format="audio/wav")
if submit2:
    response2=get_gemini_response(input_prompt2,image_data)
    if language_choice == "Telugu":
        response2 = TextBlob(response2).translate(from_lang="en", to="te")  # Translate if Telugu
    st.header(f"{'సమతుల్య ఆహార పదార్థాలు:' if language_choice == 'Telugu' else 'Suggested Balanced Food Items:'}")
    st.write(response2)
    audio_bytes = generate_audio(response2, language_choice)  # Generate audio
    st.audio(audio_bytes, format="audio/mp3")
    #st.audio(audio_bytes, format="audio/wav")