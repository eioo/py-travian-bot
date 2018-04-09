import json
import os
import pdb
import time
import sys
from html.parser import HTMLParser

debug_folder = './debug'
config_file = './config.json'
html_parser = HTMLParser()

def read_config():
  if os.path.exists(config_file):
    with open(config_file) as f:
      return json.loads(f.read())

def timestamp():
  return time.localtime()

def epoch():
  return time.mktime(timestamp())

def log(text):
  sys.stdout.write('[%s] %s\n' % (time.strftime("%H:%M:%S", timestamp()), text))

def unescape(html):
  return html_parser.unescape(html)

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0))
        return ret
    return wrap

def saveDebugFile(html, remove_files=False):
  filename = 'debug/{}.html'.format(int(epoch()))

  if not os.path.exists(debug_folder):
    os.mkdir(debug_folder)

  if remove_files:
    for the_file in os.listdir(debug_folder):
        file_path = os.path.join(debug_folder, the_file)
        try:
            if os.path.isfile(file_path):
              os.unlink(file_path)
        except Exception as e:
            print(e)

  open(filename, 'w').write(html.encode('utf-8'))