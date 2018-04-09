import json
import requests

from helpers import *


class RequestHandler:
  def __init__(self, parent):
    self.parent = parent
    self.last_r = None
    self.html_parser = HTMLParser()

    self.sess = requests.session()
    self.sess.headers.update = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    self.load_cookies()

  def __getattr__(self, attr):
    return getattr(self.parent, attr)

  def req(self, url_path, data={}, headers=None):
    url = 'https://%s/%s' % (self.domain, url_path)
    
    if data:
      log('POST to %s' % url_path)
      r = self.sess.post(url, data=data, headers=headers)
      self.last_r = r
      return r
    
    log('GET to %s' % url_path)
    r = self.sess.get(url)
    self.last_r = r
    return r

  def load_cookies(self):
    try:
      with open('cookies.cj', 'r') as f:
        cookies = requests.utils.cookiejar_from_dict(json.load(f))
        self.parent.sess.cookies = cookies
    except IOError:
      log('Cookiejar doesn\'t exist')
      return

    log('Loaded cookies from cookiejar')

  def save_cookies(self):
    with open('cookies.cj', 'w') as f:
      json.dump(requests.utils.dict_from_cookiejar(self.parent.sess.cookies), f)

    log('Saved cookies to cookiejar')