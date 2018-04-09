from lib.travian import Travian

from helpers import *


config = read_config()
bot = Travian(config['username'], config['password'], config['domain'])
village = bot.village

log(village.resources)
## Build until every building is level 2
#for area in bot.village.areas.values():
#  if area.buildable(bot.village.resources.storage) and area.level == 1:
#    bot.village.build(area.id)