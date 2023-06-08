
import json
from rasa.core.actions.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import datetime 
from typing import Any, Text, Dict, List
from playsound import playsound 
from botsaid import bottalk
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from idna import ulabel
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from typing import Text, List, Any, Dict
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from bs4 import BeautifulSoup
import requests


headers = requests.utils.default_headers()


chrome_options = webdriver.ChromeOptions(); 
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
driver = webdriver.Chrome(options=chrome_options);  
driver.minimize_window()


def stream(MusicName):
	MusicName = MusicName
	driver.get(f"https://m.youtube.com/results?search_query={MusicName}")
	# driver.get(f'https://music.youtube.com/search?q={MusicName}')
	driver.implicitly_wait(3)
	# video = driver.find_element(
	# 	"xpath", "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string")
	video =driver.find_element(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
	video.click()

def stop():
	driver.quit()
        
def pauseAndPlay():
	pause_button = driver.find_element(By.XPATH, '//*[@id="movie_player"]/div[1]/video')
	pause_button.click()
	

def getToday():
    url = 'http://www.thoitiethanoi.com/'
    req = requests.get(url, headers)
    # lay trang web
    bs = BeautifulSoup(req.content, 'html.parser')
    cardcontent = bs.find(class_='weather-content')
    infos = cardcontent.find_all(class_='weather-infos')
    weather = []
    card = infos[0]
    title = card.find('h3').get_text()
    icon = card.find('img')
    celsius = card.find(class_='w-celsius').get_text()
    desc = card.find(class_='w-desc').get_text()
    text = card.find_all(class_='w-text')
    high = text[0].get_text()
    low = text[1].get_text()
    high = high.replace(':', " là ")
    low = low.replace(':', " là ")
    weather = f'Dạ thưa anh, tình hình {title}. Nhiệt độ ngoài trời là {celsius}. Ngoài trời {desc}.Nhiệt độ {high} .Nhiệt độ {low}'
    return weather




class ActionAskTime(Action): 
    def name(self) -> Text: 
        return "action_ans_time"
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        dispatcher.utter_message(text=f'Bây giờ là {hour} giờ, {minute} phút ạ')
        return []


class Action(Action): 
    def name(self) -> Text: 
        return "action_batnhac"
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bottalk('Bài nhạc tủ của anh sẽ được bật ngay sau đây ạ.')
        time.sleep(2)
        playsound('/home/justtuananh/AI4TUAN/rasa/ListMusic/binz1977.wav')
    

        # dispatcher.utter_message(text=f'Bây giờ là {hour} giờ, {minute} phút ạ')
        return []
    
class ActionGPT(Action): 
    def name(self) : 
        return "action_askGPT"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,domain):
    
        # Extract the user's message as a single entity
        
        text = tracker.latest_message.get("text")
        
        # Send a GET request to ChatGPT to retrieve the answer to the user's message
        from revChatGPT.V3 import Chatbot
        chatbot = Chatbot(api_key="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")

         # Use the OpenAI API to generate a response
        response = chatbot.ask(text)

#         # Extract the response text from the API response
        
        
        # Format the answer as a message and send it back to the user
        message = f"Câu trả lời đây ạ : {response}"
        bottalk(message)
        # dispatcher.utter_message(text=message)

# class Action_Youtube(Action):

#     def name(self) -> Text:
#         return "action_askYouTube"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         music_name = tracker.get_slot("music_name")
#         if not music_name:
#             dispatcher.utter_message(text="Em không nghe rõ , anh nói lại được không ạ")
#         else:
#             stream(music_name)
#             dispatcher.utter_message(text="Anh đợi em chút , em bật cho anh liền ")
#         return []

# class Youtube_Form(FormAction):
#     """Example of a custom form action"""

#     def name(self):
#         """Unique identifier of the form"""
#         return "action_youtube_form"
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ['music_name']
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do after all required slots are filled"""
#         stream('music_name')
#         dispatcher.utter_message("Anh đợi em một xí , em bật nhạc cho anh liền đây ạ .")
#         return []

class ValidateYoutubeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_youtube_form"

    # async def extract_outdoor_seating(
    #     self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    # ) -> Dict[Text, Any]:
    #     # text_of_last_user_message = tracker.latest_message.get("text")
    #     stream("music_name")
    #     # sit_outside = "outdoor" in text_of_last_user_message

    #     return {"outdoor_seating": sit_outside}
    # dispatcher.utter_message(text=f"Anh chờ em xíu, em đang bật bài {slot_value} cho anh ạ.")   

    async def validate_music_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker : Tracker, 
        domain: DomainDict
    ) -> Dict[Text, Any]:
        stream(slot_value)
        # dispatcher.utter_message(text=f"Anh chờ em xíu, em đang bật bài {slot_value} cho anh ạ.")
        bottalk(f"Anh chờ em xíu, em đang bật bài {slot_value} cho anh ạ.")
        return []
    
class ActionStopMusic(Action): 
    def name(self) -> Text: 
        return "action_stop_music"
    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pauseAndPlay()
        bottalk('Em đã tắt nhạc ạ.')
        # dispatcher.utter_message(text=f'Em đã tắt nhạc ạ')
        return []

class ActionAnsWeatherToday(Action): 
    def name(self) -> Text: 
        return "action_ans_weathertoday"
    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        weather = getToday()
        bottalk(weather)
        # dispatcher.utter_message(text=weather)
        return []








# class ActionChatGPT(Action):
#     def name(self):
#         return "action_chat_gpt"

#     def run(self, dispatcher, tracker, domain):
#         # Get the user's input message
#         user_input = tracker.latest_message['text']

#         # Set up the OpenAI API client
#         from revChatGPT.V3 import Chatbot
#         chatbot = Chatbot(api_key="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")

#         # Use the OpenAI API to generate a response
#         response = chatbot.ask(user_input)

#         # Extract the response text from the API response
#         response_text = response.choices[0].text.strip()

#         # Send the response back to the user
#         dispatcher.utter_message(text=response_text, template="utter_question")

#         return [SlotSet("response_generated", True)]
