import json
from bs4 import BeautifulSoup

from helpers import *


class LoginHandler:
  def __init__(self, parent, username, password, domain):
    self.parent = parent
    self.username = username
    self.password = password
    self.domain = domain
    self.logged_in = False
    self.travian_plus = None # In seconds
    self.ajax_token = None
  
  def __getattr__(self, attr):
    return getattr(self.parent, attr)
      
  def login(self):
    log('Logging in...')

    r = self.req('dorf1.php', {
      'name':     self.username,
      'password': self.password,
      's1':       'Kirjaudu',              # TO-DO: this needs to be dynamic
      'w':        '1680:1050',             # TO-DO: this needs to be dynamic
      'login':    str(epoch()),            # Current time
      'lowRes':   '0'                      # 0 is for large screens
    })
    
    self.logged_in = 'href="logout.php"' in r.text

    if not self.logged_in:
      log('Login failed. Exiting...')
      sys.exit()

    self.save_cookies()
    log('Login succesful')
    return r

  def check_login(self):
    """Checks if player is logged in. Tries to login if not logged in already."""
    log('Checking if logged in')

    if not self.last_r:
      r = self.req('dorf1.php')

    self.logged_in = 'href="logout.php"' in r.text

    if self.logged_in:
      self.get_plus_time(r.text)
    else:
      log('Not logged in')
      self.login()
      self.get_plus_time()
    
  def get_plus_time(self, html=None):
    log('Getting plus time')

    if not html:
      r = self.req('dorf1.php')
    
    self.ajax_token = self.last_r.text.split('return \'')[1].split('\'')[0]

    payload = {
      'cmd': 'paymentWizard',
      'goldProductId': '',
      'goldProductLocation': '',
      'location': '',
      'activeTab': 'pros',
      'ajaxToken': self.ajax_token
    }

    r = self.req('ajax.php?cmd=paymentWizard', data=payload, headers={
      'X-Request': 'JSON',
      'X-Requested-With': 'XMLHttpRequest'
    })

    html = json.loads(r.text)['response']['data']['html']
    soup = BeautifulSoup(html, 'html5lib')

    seconds = int(soup.select('.featureContent')[1].select('.timer')[0]['value'])
    self.travian_plus = epoch() + seconds
    log('Travian plus ends in %.2f hours' % (float(self.travian_plus - epoch()) / 60 / 60))