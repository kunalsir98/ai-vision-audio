#voice of agent.py 
#setup text to speech(gtts and eleven labs)

#with gtts 
import os 
from gtts import gTTS

'''def text_to_speech_with_gtts_old(input_text,output_filepath):
    language='en'

    audioobj=gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

input_text='Hi i am kunal how are you'
#text_to_speech_with_gtts_old(input_text=input_text,output_filepath='gtts_testing.mp3')'''

# step2 
import os
from gtts import gTTS
import subprocess
import platform


def text_to_speech_with_gtts(input_text, output_filepath):

    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )

    audioobj.save(output_filepath)

    os_name = platform.system()

    try:
        if os_name == "Windows":
            os.startfile(output_filepath)

        elif os_name == "Darwin":
            subprocess.run(["afplay", output_filepath])

        elif os_name == "Linux":
            subprocess.run(["mpg123", output_filepath])

        else:
            raise OSError("Unsupported operating system")

    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text = "Hi I am Kunal, how are you testing"

text_to_speech_with_gtts(
    input_text=input_text,
    output_filepath="gtts_testing.mp3"
)