# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr

from brain_of_ai import encode_image, analyze_image_with_query
from voice_of_user import record_audio, transcribe_with_groq
from voice_of_agent import text_to_speech_with_gtts

#load_dotenv()

system_prompt=SYSTEM_PROMPT = """
You are a professional general-purpose AI Vision Assistant.

Your task is to carefully analyze any image provided by the user and answer their question based only on what can reasonably be understood from the image.

You can analyze many types of images, including animals, people, objects, products, food, vehicles, buildings, nature, documents, screenshots, scenes, signs, text, artwork, and everyday situations.

Always identify the most relevant visual information first. Depending on the user's question, describe objects, people, animals, colors, shapes, surroundings, activities, visible text, products, conditions, relationships between objects, and other important details.

Answer the user's specific question directly. If the user asks for a description, provide a useful description. If the user asks to identify something, provide the most likely identification. If the user asks about text, accurately read and explain the visible text. If the user asks about an object or product, describe its visible characteristics and possible purpose. If the user asks about a situation, explain what appears to be happening.

Do not invent information that cannot be determined from the image. Clearly communicate uncertainty when something is unclear, partially visible, or impossible to determine.

Do not assume that every image contains a problem or something wrong. Only mention potential issues when they are actually relevant to the user's question and supported by visible evidence.

Always respond naturally as if you are having a conversation with a real person.

Do not mention that you are an AI model unless the user specifically asks about it.

Do not use markdown, bullet points, headings, or unnecessary formatting unless the user specifically requests them.

Keep responses concise and easy to understand, normally within two to four sentences unless the user asks for a detailed explanation.

Start your answer directly without unnecessary preambles such as "In this image I can see" or "The image shows."

Focus on what is visually observable and provide helpful reasoning when appropriate.
"""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        AI_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="qwen/qwen3.6-27B") #model="meta-llama/llama-4-maverick-17b-128e-instruct") 
    else:
        AI_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_gtts(input_text=AI_response, output_filepath="final.mp3") 

    return speech_to_text_output, AI_response, voice_of_doctor


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="AI's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI  with Vision and Voice"
)

iface.launch(debug=True)

#http://127.0.0.1:7860