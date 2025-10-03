# House owners area, change something calculate pipeline
from abc import ABC, abstractmethod
from context import Context

class Pipeline_step(ABC):
  @abstractmethod
  def execute(context:"Context"): pass
  
  @abstractmethod
  def introspect(): pass


class Pipeline:

  def __init__(self,steps:list=list()):
    self.steps = steps

  def add_step(self,step: Pipeline_step):
    self.steps.append(step)

  def run(self,context:"Context"):
    for step in self.steps:
      step.execute(context)



