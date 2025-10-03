# House owners area, change something calculate pipeline
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

TContext = TypeVar("TContext")

class Pipeline_step(ABC, Generic[TContext]):
  @abstractmethod
  def execute(context:TContext): pass
  
  @abstractmethod
  def introspect(): pass


class Pipeline(Generic[TContext]):

  def __init__(self,steps:list[Pipeline_step[TContext]] | None = None):
    self.steps = steps if steps is not None else []

  def add_step(self,step: Pipeline_step[TContext]):
    self.steps.append(step)

  def run(self,context:TContext):
    for step in self.steps:
      if getattr(context, "is_done", True):
        print("DONE")
        break
      step.execute(context)

