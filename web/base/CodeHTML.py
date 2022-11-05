from email import header
from html.parser import HTMLParser
import re
from urllib import response
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
import requests
from lxml import html
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CodeHTML:
    link = None
    page = None

    def __init__(self, link):
        self.link = link
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [
            OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100)
        self.user_agent = user_agent_rotator.get_random_user_agent()

    def getPage(self):
        if self.page == None:
            s = requests.session()
            response = s.get(self.link  , headers={'User-agent': 'Mozilla/5.0'})
            self.page = response.text
        return self.page

    def beautifulSoup(self):
        page = self.getPage()
        if page != None:
            return BeautifulSoup( page , "html.parser")
        else:
            return None
    
    def tree(self):
        self.page()
        if self.page != None:
            myparser = html,HTMLParser( encoding = "utf-8")
            return html.fromstring(self.page , parser = myparser)
        else:
            return None
    