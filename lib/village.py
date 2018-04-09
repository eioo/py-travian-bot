import re
from bs4 import BeautifulSoup
from pprint import pformat

from .resources import ResourceList, Resources
from helpers import *

class Village:
  def __init__(self, parent):
    self.parent      = parent
    self.resources   = None
    self.areas       = None
    self.build_queue = []

  def __getattr__(self, attr):
    return getattr(self.parent, attr)

  def __repr__(self):
    return pformat((self.resources, self.areas, ), indent=2)

  def get_resources(self, html=None):
    if not html:
      r = self.parent.req('dorf1.php')
      html = r.text
  
    production = re.findall('l1": ([\d+\.]+),"l2": ([\d+\.]+),"l3": ([\d+\.]+),"l4": ([\d+\.]+),"l5": ([\d+\.]+)', html)[0]
    storages   = re.findall('l1": ([\d+\.]+),"l2": ([\d+\.]+),"l3": ([\d+\.]+),"l4": ([\d+\.]+)\W+}', html)
    
    production  = ResourceList(*production)
    storage     = ResourceList(*storages[0])
    max_storage = ResourceList(*storages[1])

    self.resources = Resources(production, storage, max_storage)
    return self.resources

  def get_area_data(self, html=None):
    if not html:
      r = self.parent.req('dorf1.php')
      html = r.text
  
    soup = BeautifulSoup(html, 'html5lib')

    areas = {}

    for i, element in enumerate(soup.findAll('area')):
      if not 'build.php' in element['href']:
        continue
    
      area_id = i + 1

      unescaped = unescape(element['title'])
      area_soup = BeautifulSoup(unescaped, 'html5lib')

      name  = area_soup.getText().strip().split()[0]

      level = int(area_soup.find('span', {'class': 'level'}) \
                           .getText().strip().split()[-1])

      cost_wood  = int(area_soup.find('span', {'class': 'r1'}).getText())
      cost_clay  = int(area_soup.find('span', {'class': 'r2'}).getText())
      cost_iron  = int(area_soup.find('span', {'class': 'r3'}).getText())
      cost_grain = int(area_soup.find('span', {'class': 'r4'}).getText())

      build_cost = ResourceList(cost_wood, cost_clay, cost_iron, cost_grain)
      area = Area(area_id, name, level, build_cost)

      areas[area_id] = area

    self.areas = areas
    return self.areas

  def get_build_queue(self, html=None):
    if not html:
      r = self.parent.req('dorf1.php')
      html = r.text

    queue = []

    soup = BeautifulSoup(html, 'html5lib')
    building_list = soup.select('.buildingList')

    if not building_list:
      return queue

    building_list = building_list[0]

    names = building_list.select('.name')
    build_times = building_list.select('.buildDuration')

    for i in range(len(names)):
      name, level = re.findall('(\w+).+(\d+)', str(names[i]))[0]
      build_time = build_times[i].select('span')[0]['value']

      queue.append(BuildingQueueItem(name, level, build_time))
    
    self.build_queue = queue
    return self.build_queue
  
  def build_queue_wait(self, html=None):
    if not self.build_queue:
      return
    
    longest = self.build_queue[0]

    for queue_item in self.build_queue:
      if queue_item.build_time > longest.build_time:
        longest = queue_item

    log('Waiting for %s seconds for build queue to empty.' % (longest.build_time + 2))
    time.sleep(longest.build_time + 2)

  def wait_for_resources(self, area):
    """Wait until enough resources to build again"""
    production  = self.resources.production
    storage     = self.resources.storage
    max_storage = self.resources.max_storage

    seconds_list = []

    for resource in ['wood', 'clay', 'iron', 'grain']:
      area_res        = getattr(area.build_cost, resource)
      storage_res     = getattr(storage,         resource)
      production_res  = getattr(production,      resource)

      if area_res > storage_res:
        seconds = int(((area_res - storage_res + 3) / production.wood) * 60 * 60)
        seconds_list.append(seconds)

    if seconds_list:
      longest = max(seconds_list)
      log('Need to wait for resources. (Done: %s)' % time.strftime("%H:%M:%S", time.localtime(epoch() + longest + 3)))
      time.sleep(longest + 3)
    
  def refresh(self):
    log('Refreshing village data')
    r = self.parent.req('dorf1.php')

    self.get_build_queue(r.text)
    self.get_resources(r.text)
    self.get_area_data(r.text)

    self.wait_for_resources(self.areas[1])

    log('Village data refreshed')
    return self

  def build(self, area_id):
    if not self.resources or not self.areas:
      self.refresh()

    area = self.areas[area_id]
    log('Building %s to lvl %s. (id: %s)' % (area.name, (area.level + 1), area.id))
    
    self.build_queue_wait()

    if not area.buildable(self.resources.storage):
      log('Not enough resources to build %s lvl %s. (id: %s)' % (area.name, (area.level + 1), area.id))
      self.wait_for_resources(area)

    r = self.parent.req('build.php?id=%s' % (area.id))
    soup = BeautifulSoup(r.text, 'html5lib')

    url_path = str(soup.find('button', {'class': 'green build'})) \
                .split('window.location.href = \'')[1] \
                .split('\';')[0]
    url_path = unescape(url_path)

    r = self.parent.req(url_path)
    self.get_build_queue(r.text)

    return True

class Area:
  def __init__(self, area_id, name, level, build_cost):
    self.id = area_id
    self.name = name
    self.level = level
    self.build_cost = build_cost
  
  def buildable(self, resources):
    return resources >= self.build_cost

class BuildingQueueItem:
  def __init__(self, name, target_level, build_time):
    self.name         = name
    self.target_level = int(target_level)
    self.build_time   = int(build_time)
  
  def __repr__(self):
    return repr([self.name, self.target_level, self.build_time])