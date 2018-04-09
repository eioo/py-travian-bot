import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from lib.loginhandler import LoginHandler
from lib.requesthandler import RequestHandler
from lib.village import Village
from helpers import *


class Travian(RequestHandler, LoginHandler, Village):
  def __init__(self, username, password, domain):
    RequestHandler.__init__(self, self)
    LoginHandler.__init__(self, self, username, password, domain)
    Village.__init__(self, self)
    
    self.check_login()
    
    self.village = Village(self)
    self.village.refresh()