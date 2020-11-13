# Final report portal screen linked to home screen with navigation drawer
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.theming import ThemableBehavior
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.taptargetview import MDTapTargetView
import helpers
import os
import mail
import urllib3
import joblib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from ibm_watson import NaturalLanguageUnderstandingV1
# An IBM CLOUD SERVICE
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, \
    ConceptsOptions, EmotionOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions
from ibm_watson import IAMTokenManager
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator
import nltk

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
import pandas as pd
import gensim
import gensim.corpora as corpora

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

import nltk

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
import csv
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from stop_words import get_stop_words
import re
import liwc
from array import *

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
en_stop.extend(['from', 'subject', 're', 'edu', 'use'])
texts = []

tokenizer = RegexpTokenizer(r'\w+')
from stop_words import get_stop_words

en_stop = get_stop_words('en')
en_stop.extend(['from', 'subject', 're', 'edu', 'use'])

lemmatizer = WordNetLemmatizer()
texts = []
from nltk.corpus import wordnet


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


# ibm watson access keys
authenticator = IAMAuthenticator('add authentication id')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='add version',
    authenticator=authenticator
)

iam_token_manager = IAMTokenManager(apikey='add api key')
token = iam_token_manager.get_token()
authenticator1 = BearerTokenAuthenticator(token)
natural_language_understanding1 = NaturalLanguageUnderstandingV1(version='add version',
                                                                 authenticator=authenticator1)
natural_language_understanding.set_service_url(
    'add service url')
natural_language_understanding.set_disable_ssl_verification(True)


def listtostring(s):
    str1 = " "
    return (str1.join(s))


finalpath = ""
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

Window.size = (300, 500)

# HOME SCREEN
navigation_helper = """
Screen:
    id: home
    name: 'home'
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "HOME"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                    Widget:
                    DrawerList:
                        id: features
                        MDList:
                            OneLineIconListItem:
                                text: "Conversational Analyser"
                                on_release: root.manager.current = 'conv_upload'
                                IconLeftWidget:
                                    icon: "chat-processing"
                                    on_release: root.manager.current = 'conv_upload'
                            OneLineIconListItem:
                                text: "Stats"
                                on_release: root.manager.current = 'news_home'
                                IconLeftWidget:
                                    icon: "chart-line"
                                    on_release: root.manager.current = 'news_home'
                            OneLineIconListItem:
                                text: "Report Portal"
                                on_release: root.manager.current = 'portal'
                                IconLeftWidget:
                                    icon: "notebook-outline"
                                    on_release: root.manager.current = 'portal'
                    ScrollView:
                    MDBottomNavigation:
                        MDBottomNavigationItem:
                            name: 'contact'
                            icon: 'phone'
                        MDBottomNavigationItem:
                            name: 'query'
                            icon: 'comment-question'
                        MDBottomNavigationItem:
                            name: 'account'
                            icon: 'account'
                        MDBottomNavigationItem:
                            name: 'settings'
                            icon: 'settings'
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"
                MDLabel:
                    text: "CHAT ANALYSER"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                ScrollView:
                    DrawerList:
                        id: md_list
                        MDList:
                            OneLineIconListItem:
                                text: "How to use"
                                IconLeftWidget:
                                    icon: "help"
                            OneLineIconListItem:
                                text: "FAQ"
                                IconLeftWidget:
                                    icon: "frequently-asked-questions"
                            OneLineIconListItem:
                                text: "About this app"
                                IconLeftWidget:
                                    icon: "application"
                            OneLineIconListItem:
                                text: "Privacy policy"
                                IconLeftWidget:
                                    icon: "security"
                            OneLineIconListItem:
                                text: "Logout"
                                IconLeftWidget:
                                    icon: "login"
"""

# UPLOAD FILE SCREEN
conv_upload = """
Screen:
    id: conv_upload
    name: 'conv_upload'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Upload File'
            left_action_items: [["alert-circle-outline", lambda x: app.info()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H6"
            halign: "center"        
        MDRoundFlatIconButton:
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: app.file_manager_open()
        MDLabel:
            text: ""
            font_style:"H6"
            halign: "center"
        MDRaisedButton:
            text: "NEXT"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: root.manager.current = 'conv_home'
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'home'
"""

# REPORT PORTAL
screen_helper = """
Screen:
    id: portal
    name: 'portal'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Report Portal'
            left_action_items: [["alert-circle-outline", lambda x: app.info()]]
            elevation:10
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'home'
"""

# LOGIN SCREEN
login_helper = """
Screen:
    id: login
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Login'
            elevation:10
        Widget:
        MDTextButton:
            text: 'Click here to sign up'
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            on_press: root.manager.current = 'signup'
        MDBottomAppBar:
            MDToolbar:
                icon: 'kodi'
                type: 'bottom'
"""

# SIGNUP PAGE
signup_helper = """
Screen:
    id: signup
    name: 'signup'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Signup'
            elevation:10
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'kodi'
                type: 'bottom'
"""

# STATISTICS SCREEN
newsscraping = """
Screen:
    id: news_home
    name: 'news_home'
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: 'TRENDING ARTICLES ON WOMEN'
                        left_action_items: [['alert-circle-outline', lambda x: app.info4()]]
                        elevation:2
                    MDLabel:
                        text: ""
                        font_style:"H6"
                        halign: "center"
                    MDLabel:
                        text: "Active Social Media Users"
                        halign: "center"
                    MDLabel:
                        text: "3.80"
                        font_style:"H3"
                        halign: "center"
                    MDLabel:
                        text: "BILLION"
                        halign: "center"
                    BoxLayout:
                        orientation: 'horizontal'
                        MDFloatingActionButton:
                            id: button1
                            icon: "plus"
                            pos: 10, 10
                            on_release: app.tap_target_start1()
                    DrawerList:
                        id: features1
                        MDList:
                            OneLineIconListItem:
                                text: "Iraq urged to investigate attacks on women human rights defenders"
                                on_release: root.manager.current = 'news_1'
                                IconLeftWidget:
                                    icon: "square"
                                    on_release: root.manager.current = 'news_1'
                            OneLineIconListItem:
                                text: "Thailand: More than 100 companies pledge to strengthen women’s economic empowerment"
                                on_release: root.manager.current = 'news_2'
                                IconLeftWidget:
                                    icon: "square"
                                    on_release: root.manager.current = 'news_2'
                            OneLineIconListItem:
                                text: "Most countries failing to protect women from COVID-19 economic and social fallout"
                                on_release: root.manager.current = 'news_3'
                                IconLeftWidget:
                                    icon: "square"
                                    on_release: root.manager.current = 'news_3'
                    ScrollView:
                    MDBottomNavigation:
                        MDBottomNavigationItem:
                            name: 'query'
                            icon: 'comment-question'
                        MDBottomNavigationItem:
                            name: 'home'
                            icon: 'home'
                            on_tab_release: root.manager.current = 'home'
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"
                MDLabel:
                    text: "ARTICLES ON WOMEN"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
"""

# STATS 1
screen_helper4 = """
Screen:
    id: news_1
    name: 'news_1'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Iraq urged to investigate attacks on women human rights defenders'
            left_action_items: [["alert-circle-outline", lambda x: app.info1()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H6"
            halign: "center"
        MDLabel:
            text: "UN-appointed independent rights experts have urged the Iraqi authorities to investigate the murder of a female human rights defender, and the attempted killing of another, targeted “simply because they are women”."
            halign: "center"
            font_style: "H6"
            theme_text_color: "Custom"
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'news_home'
"""

# STATS 2
screen_helper5 = """
Screen:
    id: news_2
    name: 'news_2'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Thailand: More than 100 companies pledge to strengthen women’s economic empowerment'
            left_action_items: [["alert-circle-outline", lambda x: app.info2()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H6"
            halign: "center"
        MDLabel:
            text: "Chief executives of 110 companies in Thailand on Wednesday, have signed up to a new set of UN principles on women’s economic empowerment, pledging to improve gender equality in the boardroom, equal pay for equal work, and safer and more inclusive workplaces."
            halign: "center"
            font_style: "H6"
            theme_text_color: "Custom"
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'news_home'
"""

# STATS 3
screen_helper6 = """
Screen:
    id: news_3
    name: 'news_3'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Most countries failing to protect women from COVID-19 economic and social fallout'
            left_action_items: [["alert-circle-outline", lambda x: app.info3()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H6"
            halign: "center"
        MDLabel:       
	        text: "The COVID-19 pandemic is “hitting women hard”, but most nations are failing to provide sufficient social and economic protection for them, the head of the UN gender empowerment agency said on Monday."
            halign: "center"
            font_style: "H6"
            theme_text_color: "Custom"
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'news_home'
"""

# ANALYSER MAIN SCREEN
conv_anal = """
Screen:
    id: conv_home
    name: 'conv_home'
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    id:box
                    orientation: 'vertical'
                    MDToolbar:
                        title: 'CONVO-LYSER'
                        left_action_items: [['alert-circle-outline', lambda x: app.info4()]]
                        elevation:2
                    MDLabel:
                        text: ""
                        font_style:"H6"
                        halign: "center"
                    MDLabel:
                        text: "FEATURES"
                        halign: "center"
                        font_style: "H5"
                    BoxLayout:
                        orientation: 'horizontal'
                        MDFloatingActionButton:
                            id: button
                            icon: "plus"
                            pos: 10, 10
                            on_release: app.tap_target_start1()
                    DrawerList:
                        id: features
                        MDList:
                            OneLineIconListItem:
                                text: "SENTIMENT ANALYSIS"
                                on_release: root.manager.current = 'senti'
                                on_release: app.emo_fn()
                                IconLeftWidget:
                                    icon: "chart-pie"
                                    on_release: root.manager.current = 'senti'

                            OneLineIconListItem:
                                text: "EMOTIONAL ANALYSIS"
                                on_release: root.manager.current = 'emo'
                                on_release: app.emo_fn()
                                IconLeftWidget:
                                    icon: "chart-line"
                                    on_release: root.manager.current = 'emo'
                            OneLineIconListItem:
                                text: "ASPECT BASED ANALYSIS"
                                on_release: root.manager.current = 'aspect'
                                on_release: app.aspect_fn()
                                IconLeftWidget:
                                    icon: "chart-bar"
                                    on_release: root.manager.current = 'aspect'
                            OneLineIconListItem:
                                text: "SEMANTIC ANALYSIS"
                                on_release: root.manager.current = 'lda'
                                on_release: app.lda_fn()
                                IconLeftWidget:
                                    icon: "group"
                                    on_release: root.manager.current = 'lda'
                    ScrollView:
                    MDBottomNavigation:
                        MDBottomNavigationItem:
                            name: 'query'
                            icon: 'comment-question'
                        MDBottomNavigationItem:
                            name: 'home'
                            icon: 'home'
                            on_tab_release: root.manager.current = 'home'
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"
                MDLabel:
                    text: "CONVO-LYSER"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
"""

# SENT ANALYSER
screen_helper1 = """
Screen:
    id: senti
    name: 'senti'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'SENTIMENTAL ANALYSIS'
            left_action_items: [["alert-circle-outline", lambda x: app.info1()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H3"
            halign: "center"
        MDList:
            id: sentimentlist
            name: 'sentimentlist'
        ScrollView:
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'conv_home'
"""

# EMOTION ANALYSER
screen_helper2 = """
Screen:
    id: emo
    name: 'emo'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'EMOTIONAL ANALYSIS'
            left_action_items: [["alert-circle-outline", lambda x: app.info2()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H3"
            halign: "center"
        MDList:
            id: emotionallist
            name: 'emotionallist'
        ScrollView:
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'conv_home'
"""

# ASPECT ANALYSER
screen_helper3 = """
Screen:
    id: aspect
    name: 'aspect'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'ASPECT BASED ANALYSIS'
            left_action_items: [["alert-circle-outline", lambda x: app.info3()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H3"
            halign: "center"
        MDList:
            id: aspectlist
            name: 'aspectlist'
        ScrollView:
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'conv_home'
"""

# SEMANTIC ANALYSER
screen_helperlda = """
Screen:
    id: lda
    name: 'lda'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'SEMANTIC ANALYSIS'
            left_action_items: [["alert-circle-outline", lambda x: app.infolda()]]
            elevation:10
        MDLabel:
            text: ""
            font_style:"H3"
            halign: "center"
        MDList:
            id: ldalist
            name: 'ldalist'
        ScrollView:
        Widget:
        MDBottomAppBar:
            MDToolbar:
                icon: 'home'
                type: 'bottom'
                on_action_button: root.manager.current = 'conv_home'
"""


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    pass


sm = ScreenManager()


class DemoApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Blue"  # "BlueGray"
        self.theme_cls.primary_hue = "500"  # "700"
        self.theme_cls.theme_style = "Light"

        screen = Builder.load_string(login_helper)
        self.lusername = Builder.load_string(helpers.lusername_input)
        self.lpassword = Builder.load_string(helpers.lpassword_input)
        button = MDRectangleFlatButton(text='Submit',
                                       pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                       on_release=self.log_show_data
                                       )
        screen.add_widget(self.lusername)
        screen.add_widget(self.lpassword)
        screen.add_widget(button)
        sm.add_widget(screen)

        screen = Builder.load_string(signup_helper)
        self.username = Builder.load_string(helpers.username_input)
        self.mycontact = Builder.load_string(helpers.mycontact_input)
        self.email = Builder.load_string(helpers.email_input)
        self.password = Builder.load_string(helpers.password_input)
        self.age = Builder.load_string(helpers.age_input)
        button = MDRectangleFlatButton(text='Submit',
                                       pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                       on_release=self.sign_show_data
                                       )

        screen.add_widget(self.username)
        screen.add_widget(self.mycontact)
        screen.add_widget(self.email)
        screen.add_widget(self.password)
        screen.add_widget(self.age)
        screen.add_widget(button)
        sm.add_widget(screen)

        screen = Builder.load_string(navigation_helper)
        sm.add_widget(screen)

        screen = Builder.load_string(screen_helper)
        self.abusername = Builder.load_string(helpers.abusername_input)
        self.contact = Builder.load_string(helpers.contact_input)
        self.reason = Builder.load_string(helpers.reason_input)
        button = MDRectangleFlatButton(text='Submit',
                                       pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                       on_release=self.show_data)
        screen.add_widget(self.abusername)
        screen.add_widget(self.contact)
        screen.add_widget(self.reason)
        screen.add_widget(button)
        sm.add_widget(screen)
        screen = Builder.load_string(newsscraping)
        self.tap_target_view = MDTapTargetView(widget=screen.ids.button1,
                                               title_text="Teens having \nat least 1 social \nmedia profile",
                                               description_text="   75%                  ",

                                               widget_position="center", title_position="right_top",
                                               title_text_size="20sp", outer_radius=250, )

        sm.add_widget(screen)
        screen = Builder.load_string(conv_upload)
        sm.add_widget(screen)

        screen = Builder.load_string(screen_helper4)
        sm.add_widget(screen)
        screen = Builder.load_string(screen_helper5)
        sm.add_widget(screen)
        screen = Builder.load_string(screen_helper6)
        sm.add_widget(screen)

        return sm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".txt", ".py", "kv"],
        )

    # Sign up validation
    def sign_show_data(self, obj):

        if self.username.text != "" and self.mycontact.text != "" and self.email.text != "" and self.password.text != "":
            if len(self.mycontact.text) == 10 and self.mycontact.text.isdigit() and self.age.text.isdigit():
                if re.search(regex, self.email.text):
                    if len(self.password.text) >= 8:
                        print("USERNAME- " + self.username.text)

                        print("CONTACT NUMBER- " + self.mycontact.text)

                        print("EMAIL- " + self.email.text)
                        print("PASSWORD- " + self.password.text)
                        print("AGE- " + self.age.text)
                        # self.reason.text, self.contact.text, self.username.text = ""
                        # self.username.text = ""
                        # self.mycontact.text = ""
                        self.email.text = ""
                        # self.age.text = ""
                        user_error = ""
                    else:
                        user_error = "Please enter a valid password"
                else:
                    user_error = "Please enter a valid email id"
            else:
                user_error = "Please enter a valid contact number."


        else:
            user_error = "Please enter the required fields"
        if user_error == "":
            sm.switch_to(Builder.load_string(navigation_helper))
        else:
            self.dialog = MDDialog(
                text=user_error, size_hint=(0.8, 1),
                buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
            )
            self.dialog.open()

    # Report portal validation
    def show_data(self, obj):

        if self.contact.text != "" and self.reason.text != "":
            if len(self.contact.text) == 10 and self.contact.text.isdigit():
                print("ABUSER NAME- " + self.abusername.text)
                print(self.username.text, self.mycontact.text)
                print("CONTACT NUMBER- " + self.contact.text)
                print("REASON- " + self.reason.text)
                mail.main_func(self.username.text, self.mycontact.text, self.abusername.text, self.contact.text,
                               self.reason.text, "message")
                self.abusername.text = ""
                self.contact.text = ""
                self.reason.text = ""
                user_error = "Your response has been noted. The immediate responders will contact you soon."
            else:
                user_error = "Please enter a valid contact number."
        else:
            user_error = "Please enter the required fields"
        self.dialog = MDDialog(
            text=user_error, size_hint=(0.8, 1),
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        # do stuff after closing the dialog

    def info(self):
        self.dialog = MDDialog(
            text='The information entered below will be forwarded to the respective authorities.', size_hint=(0.8, 1),
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    # Login validation
    def log_show_data(self, obj):
        if self.lusername.text != "" and self.lpassword.text != "":
            if len(self.lpassword.text) >= 8:
                sm.switch_to(Builder.load_string(navigation_helper))
            else:
                user_error = "Incorrect password. Please try again"
                self.dialog = MDDialog(
                    text=user_error, size_hint=(0.8, 1),
                    buttons=[MDFlatButton(text='Close', on_release=self.close_dialog), ]
                )

                self.dialog.open()



        else:
            user_error = "Please enter the required details"
            self.dialog = MDDialog(
                text=user_error, size_hint=(0.8, 1),
                buttons=[MDFlatButton(text='Close', on_release=self.close_dialog), ]
            )

            self.dialog.open()

    def close_dialog1(self, obj):
        self.dialog.dismiss()

        # do stuff after closing the dialog

    def tap_target_start1(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()

    def tap_target_start2(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()

    def info1(self):
        self.dialog = MDDialog(
            text='Sentimental Analysis displays the polarity ie. positive, negative and neutral polarity values of the whole conversation',
            size_hint=(0.9, 0.5), radius=[20, 7, 20, 7],
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def info2(self):
        self.dialog = MDDialog(
            text='Emotional Analysis displays the various emotions and their value of the whole conversation',
            size_hint=(0.9, 0.5), radius=[20, 7, 20, 7],
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def info3(self):
        self.dialog = MDDialog(
            text='Aspect Based Analysis displays the most talked category of the whole conversation',
            size_hint=(0.9, 0.5), radius=[20, 7, 20, 7],
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def info4(self):
        self.dialog = MDDialog(
            text='Analysis on emotions and tones of conversations and visualise the results in the form of graphs.',
            size_hint=(1, 0), radius=[20, 7, 20, 7],
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def infolda(self):
        self.dialog = MDDialog(
            text='Semantic analysis groups words which are used together frequently',
            size_hint=(0.9, 0.5), radius=[20, 7, 20, 7],
            buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def callback(self, instance):
        print("Button is pressed")
        print('The button % s state is <%s>' % (instance, instance.state))

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.file_manager.use_access = True
        self.manager_open = True

    # Read the conversation and prepare conv_anal screen. Also check for grooming if applicable
    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.
        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()

        global finalpath
        punc = '''/~$%^'''
        # remove '/' from the path
        for ele in path:
            if ele in punc:
                path1 = path.replace(ele, "")
        # path1 -> '/' symbol removed filepath  /Users\Kripa\Desktop\exconvo.txt to Users\Kripa\Desktop\exconvo.txt

        tmplist = path1.split(os.sep)
        # splits the path and is put in the list tmplist
        # Users\Kripa\Desktop\exconvo.txt to ['Users','Kripa','Desktop','exconvo.txt']

        finalpath = ""
        for wrd in tmplist:
            finalpath = finalpath + r"\\" + wrd
        finalpath = "C:" + finalpath
        # print(finalpath)   #C:\\Users\Kripa\Desktop\exconvo.txt
        with open(finalpath, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)

            with open('C:\\Users\\Kripa\\Desktop\\convo.csv', 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(('name', 'msg'))
                writer.writerows(lines)

        ct = 0
        row_ct1 = 0
        row_ct2 = 0
        strname = ""

        # Get no.of messages for both users
        with open("C:\\Users\\Kripa\Desktop\\convo.csv", 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                # lets tokenise
                if ct == 0 and row[0] != "name":
                    strname = row[0]
                    ct = ct + 1
                if row[0] == strname:
                    row_ct1 = row_ct1 + 1

                else:
                    row_ct2 = row_ct2 + 1

        screen = Builder.load_string(conv_anal)

        self.tap_target_view = MDTapTargetView(widget=screen.ids.button, title_text="USER 1      USER 2",
                                               description_text="   " + str(row_ct1) + "                  " + str(
                                                   row_ct2) + " \nMESSAGES    MESSAGES",
                                               widget_position="center", title_position="right_top",
                                               title_text_size="20sp", outer_radius=250, )

        sm.add_widget(screen)

        # GROOMING
        if int(self.age.text) < 18:
            with open("C:\\Users\\Kripa\Desktop\\convo.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                pred_name = ""
                p_ct = 0
                for row in csv_reader:
                    if p_ct == 0 and row[0] != "name" and row[0] != self.username.text:
                        pred_name = row[0]
                        p_ct = p_ct + 1
                    row[1] = row[1].lower()  # convert to lowercase

                    lemr = ""
                    for word in row[1].split():  # Lemmatisation
                        lem = (lemmatizer.lemmatize(word, pos="v"))
                        lem = (lemmatizer.lemmatize(lem))
                        lemr = lemr + lem + " "

                    no_punct = ""
                    for char in lemr:  # Remove punctuation
                        if char not in punctuations:
                            no_punct = no_punct + char

                    data = word_tokenize(no_punct)
                    stopWords = set(stopwords.words('english'))
                    wordsFiltered = []

                    for w in data:  # Remove stopwords
                        if w not in stopWords:
                            wordsFiltered.append(w)
                    fp = "C:\\Users\\Kripa\\Desktop\\exconvo2.csv"
                    with open(fp, 'a+', newline='') as out_file:
                        writer = csv.writer(out_file, delimiter=' ')
                        writer.writerow(wordsFiltered[:20])

            # liwc
            def tokenize(text):
                for match in re.finditer(r'\w+', text, re.UNICODE):
                    yield match.group(0)

            parse, category_names = liwc.load_token_parser("C:\\Users\\Kripa\\Desktop\\bigdic.dic")
            cntt = array('i', [0, 0, 0, 0, 0, 0])  # Stages
            predator = "C:\\Users\\Kripa\\Desktop\\exconvo2.csv"
            with open(predator) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                ct = 0
                i = 1
                j = 0
                for row in csv_reader:

                    p = row.copy()
                    p1 = listtostring(p).lower()
                    p_token = tokenize(p1)
                    from collections import Counter
                    op1 = Counter(category for token in p_token for category in parse(token))
                    op = dict(op1)
                    l = list(op.keys())
                    l.sort(reverse=True)
                    if l:
                        j = l[0]
                    if j == "S1":
                        cntt[0] = cntt[0] + 1
                    if j == "S2":
                        cntt[1] = cntt[1] + 1
                    if j == "S3":
                        cntt[2] = cntt[2] + 1
                    if j == "S4":
                        cntt[3] = cntt[3] + 1
                    if j == "S5":
                        cntt[4] = cntt[4] + 1
                    if j == "S6":
                        cntt[5] = cntt[5] + 1
            '''
            cntt[0]=807
            cntt[1]=396
            cntt[2] =87
            cntt[3] =79
            cntt[4] =38
            cntt[5] =226
            '''
            clf = joblib.load('svm.pkl')
            op = clf.predict([cntt])
            if op == [1]:
                mail.main_func(self.username.text, self.mycontact.text, pred_name, "", "", "message1")
                self.dialog = MDDialog(
                    text="Grooming characteristics detected. Immediate responders have been informed.",
                    size_hint=(0.8, 1),
                    buttons=[MDFlatButton(text='Close', on_release=self.close_dialog), ]
                )

                self.dialog.open()

        toast(finalpath)
        # return sm
        os.remove("C:\\Users\\Kripa\\Desktop\\exconvo2.csv")

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    # Aspect analysis
    def aspect_fn(self):
        with open("C:\\Users\\Kripa\\Desktop\\convo.csv") as file:
            data = list(csv.reader(file))

        strin = " ".join(str(x) for x in data)

        natural_language_understanding.set_service_url(
            'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c70c1850-5873-495c-b449-d84d30415f06')
        natural_language_understanding.set_disable_ssl_verification(True)
        response = natural_language_understanding.analyze(
            text=strin,
            features=Features(
                categories=CategoriesOptions(limit=3),
            )).get_result()

        cat1 = response['categories']

        di1 = cat1[0]
        di2 = cat1[1]
        di3 = cat1[2]

        str1 = di1['label']
        str11 = str(di1['score'])
        str2 = di2['label']
        str21 = str(di2['score'])
        str3 = di3['label']
        str31 = str(di3['score'])

        screen = Builder.load_string(screen_helper3)
        screen.ids.aspectlist.add_widget(
            TwoLineListItem(
                text=str1,
                secondary_text=str11

            )
        )
        screen.ids.aspectlist.add_widget(
            TwoLineListItem(
                text=str2,
                secondary_text=str21

            )
        )
        screen.ids.aspectlist.add_widget(
            TwoLineListItem(
                text=str3,
                secondary_text=str31

            )
        )

        sm.add_widget(screen)

    # Sentiment and emotiona enalysis
    def emo_fn(self):
        cn = cp = cng = e1 = e2 = e3 = e4 = e5 = 0
        with open("C:\\Users\\Kripa\\Desktop\\convo.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                j = 0
                row = listtostring(row)
                response = natural_language_understanding.analyze(
                    text=row,
                    language='en',
                    features=Features(
                        sentiment=SentimentOptions(),
                        emotion=EmotionOptions(),
                    )).get_result()

                sen1 = response.get('sentiment').get('document').get('score')
                sen2 = response.get('sentiment').get('document').get('label')
                if sen1 == 0:
                    cn += 1

                elif sen1 > 0:
                    cp += 1

                else:
                    cng += 1
                op = response.get('emotion').get('document').get('emotion')

                # Create a list of tuples sorted by index 1 i.e. value field
                listofTuples = sorted(op.items(), reverse=True, key=lambda x: x[1])
                ll = listofTuples[0]
                d = dict(listofTuples)
                for k, v in d.items():
                    d1 = k
                    d2 = v
                    j += 1
                    if j > 0:
                        break
                if d1 == 'sadness':
                    e1 += 1
                elif d1 == 'joy':
                    e2 += 1
                elif d1 == 'fear':
                    e3 += 1
                elif d1 == 'disgust':
                    e4 += 1
                else:
                    e5 += 1

        s = s1 = 0
        s = cn + cng + cp
        pp = (cp * 100) / s
        ngp = (cng * 100) / s
        np = (cn * 100) / s
        s1 = e1 + e2 + e3 + e4 + e5
        e1p = (e1 * 100) / s1
        e2p = (e2 * 100) / s1
        e3p = (e3 * 100) / s1
        e4p = (e4 * 100) / s1
        e5p = (e5 * 100) / s1

        screen = Builder.load_string(screen_helper1)

        neutral = "Neutral: " + str(round(np, 2))
        pos = "Positive: " + str(round(pp, 2))
        neg = "Negative: " + str(round(ngp, 2))

        screen.ids.sentimentlist.add_widget(
            OneLineListItem(
                text=neutral,

            )
        )
        screen.ids.sentimentlist.add_widget(
            OneLineListItem(
                text=pos,

            )
        )
        screen.ids.sentimentlist.add_widget(
            OneLineListItem(
                text=neg,

            )
        )

        sm.add_widget(screen)

        screen = Builder.load_string(screen_helper2)

        sad = "Sad: " + str(round(e1p, 2))
        joy = "Joy: " + str(round(e2p, 2))
        fear = "Fear: " + str(round(e3p, 2))
        disgust = "Disgust: " + str(round(e4p, 2))
        angry = "Angry: " + str(round(e5p, 2))

        screen.ids.emotionallist.add_widget(
            OneLineListItem(
                text=sad,

            )
        )
        screen.ids.emotionallist.add_widget(
            OneLineListItem(
                text=joy,

            )
        )
        screen.ids.emotionallist.add_widget(
            OneLineListItem(
                text=fear,

            )
        )
        screen.ids.emotionallist.add_widget(
            OneLineListItem(
                text=disgust,

            )
        )
        screen.ids.emotionallist.add_widget(
            OneLineListItem(
                text=angry,

            )
        )

        sm.add_widget(screen)

    # Semantic analysis
    def lda_fn(self):
        screen = Builder.load_string(screen_helperlda)

        with open("C:\\Users\\Kripa\Desktop\\convo.csv", 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                # lets tokenise

                raw = row[1]
                tokens = tokenizer.tokenize(raw)

                # remove stopwords
                stopped_tokens = [i for i in tokens if not i in en_stop]

                tagged = nltk.pos_tag(stopped_tokens)

                for word, tag in tagged:
                    w_tag = get_wordnet_pos(tag)
                    if w_tag is None:
                        lemmatized_tokens = [lemmatizer.lemmatize(word)]
                    else:
                        lemmatized_tokens = [lemmatizer.lemmatize(word, pos=w_tag)]

                    texts.append(lemmatized_tokens)

        # create_dict
        id2word = corpora.Dictionary(texts)

        # convert to document-term matrix
        corpus = [id2word.doc2bow(text) for text in texts]

        # generate lda
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=5,
                                                    passes=20)
        # print(lda_model.print_topics(num_topics=5))

        top_words_per_topic = []

        # puting ouput to a csv file!
        for t in range(lda_model.num_topics):
            top_words_per_topic.extend([(t,) + x for x in lda_model.show_topic(t)])

        x = pd.DataFrame(top_words_per_topic, columns=['Tno', 'Word', 'P'])
        # .to_csv('C:\\Users\\Kripa\Desktop\\top_words.csv')
        y = x['Word']

        name1 = []
        for ele in y:
            name1.append(ele)

        screen.ids.ldalist.add_widget(
            ThreeLineListItem(
                text="Group 1",
                secondary_text=name1[0] + "," + name1[1] + "," + name1[2] + "," + name1[3] + "," + name1[4] + ",",
                tertiary_text=name1[5] + "," + name1[6] + "," + name1[7] + "," + name1[8] + "," + name1[9]

            )
        )
        screen.ids.ldalist.add_widget(
            ThreeLineListItem(
                text="Group 2",
                secondary_text=name1[10] + "," + name1[11] + "," + name1[12] + "," + name1[13] + "," + name1[14] + ",",
                tertiary_text=name1[15] + "," + name1[16] + "," + name1[17] + "," + name1[18] + "," + name1[19]

            )
        )
        screen.ids.ldalist.add_widget(
            ThreeLineListItem(
                text="Group 3",
                secondary_text=name1[20] + "," + name1[21] + "," + name1[22] + "," + name1[23] + "," + name1[24] + ",",
                tertiary_text=name1[25] + "," + name1[26] + "," + name1[27] + "," + name1[28] + "," + name1[29]

            )
        )

        sm.add_widget(screen)


DemoApp().run()