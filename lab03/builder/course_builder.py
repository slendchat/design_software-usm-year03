from models_immutable import *
from models_mutable import *

class Course_builder:
  def add_student(self, student:Student):
    self.student = student