class ResourceList:
  def __init__(self, wood, clay, iron, grain, free_crop=None):
    self.wood = float(wood)
    self.clay = float(clay)
    self.iron = float(iron)
    self.grain = float(grain)

    if free_crop:
      self.free_crop = float(free_crop)
    
  def __repr__(self):
    text = 'Wood: %s\nClay: %s\nIron: %s\nGrain: %s' % \
            (self.wood, self.clay, self.iron, self.grain)

    if hasattr(self, 'free_crop'):
      text += '\nFree Crop: %s' % (self.free_crop)

    return text

  def __gt__(self, res2):
    return  self.wood > res2.wood and \
            self.clay > res2.clay and \
            self.iron > res2.iron and \
            self.grain > res2.grain
  
  def __lt__(self, res2):
    return  self.wood < res2.wood and \
            self.clay < res2.clay and \
            self.iron < res2.iron and \
            self.grain < res2.grain

  def __ge__(self, res2):
    return  self.wood >= res2.wood and \
            self.clay >= res2.clay and \
            self.iron >= res2.iron and \
            self.grain >= res2.grain
  
  def __le__(self, res2):
    return  self.wood <= res2.wood and \
            self.clay <= res2.clay and \
            self.iron <= res2.iron and \
            self.grain <= res2.grain

  def __eq__(self, res2):
    return  self.wood == res2.wood and \
            self.clay == res2.clay and \
            self.iron == res2.iron and \
            self.grain == res2.grain

class Resources:
  def __init__(self, production, storage, max_storage):
    self.production = production
    self.storage = storage
    self.max_storage = max_storage
    
  def __repr__(self):
    return 'Production\n%s\n%s\n\nStorage\n%s\n%s\n\nMax Storage\n%s\n%s' % \
           ("-" * 20, self.production, 
            "-" * 20, self.storage,
            "-" * 20, self.max_storage)