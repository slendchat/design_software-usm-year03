from typing import TypeVar, Generic

T = TypeVar('T')

class Key(Generic[T]):
  def __init__(self,name, expected_type):
    self.name = name
    self.type = expected_type

class Keyregistry:
  registry = {}
       
  @classmethod
  def register(cls, name, type):
    if name in cls.registry:
      raise ValueError("key already exists")
    key = Key(name, type)
    cls.registry[name]=key
    return key
  
class Context:
  def __init__(self):
    self.data = {}

  def set(self, key:Key, value):
    if type(value) != key.type:
      raise TypeError("Types do not match")
    self.data[key.name] = value
  
  def get(self,key:Key):
    return self.data[key.name]