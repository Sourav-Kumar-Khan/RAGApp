from gtts import gTTS
import io
import pygame

def text_to_speech(text, language='en'):
    """
    Convert text to speech using gTTS and play the audio directly from memory.
    
    :param text: The text to convert to speech
    :param language: The language of the text (default is English)
    """
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False, tld='co.in')
    
    # Save the audio to a bytes buffer
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load the audio from the bytes buffer
    pygame.mixer.music.load(fp)
    
    # Play the audio
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Clean up
    pygame.mixer.quit()

# # Example usage
# if __name__ == "__main__":
#     sample_text = "Hello Sourav, this is a test of the in-memory text-to-speech function."
#     text_to_speech(sample_text)



## Speech to text converter
import speech_recognition as sr

def speech_to_text():
    # Create a recognizer object
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        
        # Adjust for ambient noise and record audio
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        print("Could not request results from the speech recognition service; {0}".format(e))
        return None

# Example usage
if __name__ == "__main__":
    result = speech_to_text()
    if result:
        print("Converted text:", result)