import openai
import webbrowser
import AppOpener
import datetime
import keyboard
import time
from googletrans import Translator
import speech_recognition as sr
import win32com.client as win
from API_Key import key

chatStr = ""

def chat(query):
    global chatStr

    openai.api_key = key
    chatStr += f"User: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def AI(query):
  """this function takes the user's query and returns the response given by GPT-4"""

  openai.api_key = key

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=query,
    temperature=1,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response["choices"][0]["text"]

def takeCommand():
  """ this function takes voice input from the user and returns the recognized text."""
  
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print('Listening')
    r.adjust_for_ambient_noise(source) 
    audio = r.listen(source)
    try:
      print("Recognizing")
      Query = r.recognize_google(audio, language='en-In')
      return Query
    except Exception as e:
      print(e)
      return "-"

#Note: This say function only works on windows. 
def say(text):
  speak = win.Dispatch("SAPI.SpVoice")
  speak.Speak(text)
  
#For Mac Users
"""
def say(text):
  os.system(f"say '{text}'")
"""

if __name__ == '__main__':

  print("Welcome to Jarvis A.I.")
  say("Welcome to Jarvis AI. How may I help you today?")

  while True:
    query = takeCommand()
    print(f"User said: {query}")

    #Query : Using artificial intelligence .....
    if "artificial intelligence" in query.lower():
      query = query.split("intelligence")[1]
      print(AI(query))

    #Query :  Open .... on browser
    elif "browser" in query.lower():
      website = query.split("open")[1]
      say(f"Opening {website}")
      url = AI(f"What is the website for {website}?").split("is")[1].lstrip(" ")
      webbrowser.open(url)

    #Query : search ..... on youtube
    elif "on youtube" in query.lower():
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.split('search')[1].split('on')[0]}")

    #Query : search ..... on ......
    elif "search" in query.lower():
      website = query.split("on")[1].lstrip(" ")
      url = AI(f"What is the website for {website}?").split("is")[1].lstrip(" ")
      webbrowser.open(url)
      time.sleep(3)
      keyboard.write((query.split("search")[1]).split("on")[0])
      keyboard.press_and_release("enter")

    #You can open a pre-installed application, just by saying : open ....
    elif "open" in query.lower():
      app = query.split("open")[1]
      say(f"Opening {app}")
      AppOpener.open(app)

    #You can also close the app bye saying: Close .....
    elif "close" in query.lower():
      app = query.split("close")[1]
      AppOpener.close(app)

    #Just head on by saying :  What's the time?
    elif "time" in query.lower():
      time = datetime.datetime.now().strftime("%I:%M")
      print(time)
      say(f"Sir the time is {time.split(':')[0]} bajke {time.split(':')[1]} minute")

    #NOTE: Currently the the translate function supports limited languages!
    elif "translate" in query.lower():
      say("Which language you want to translate from?")
      initial = takeCommand()
      say("Which language you want to translate to?")
      final = takeCommand()
      translator = Translator()
      say("Please speak the text to be translated.")
      text = takeCommand()
      translated_text = translator.translate(text, src=initial, dest =final)
      print(f"The Actual Text was {text}")
      print(f"The Translated Text is: {translated_text.text}")

    #Jarvis can type something for you. Just ask : Jarvis, type for me.
    elif "type" in query.lower():
      say("Please speak the text you want to type.")
      text = takeCommand()
      keyboard.write(text)

    elif "bye" in query.lower():
      print("Good Bye! I hope I could be of your help.")
      say("Good Bye! I hope I could be of your help.")
      exit()

    #If you are feeling lonely, feel free to ask Jarvis to entertain you.
    else:
      print("Chatting...")
      chat(query)