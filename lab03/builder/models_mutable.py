
class Student:
  def __init__(self, name: str, age: int, grade: int):
    self.name = name
    self.age = age
    self.grade = grade
    self.group = None
    self.subjects = []
    self.teachers = []

class Course:
  def __init__(self, title:str, description:str):
    self.title = title
    self.description = description

class Group:
  def __init__(self, name:str):
    self.name = name
    self.students = []
    self.course = None

class Subject:
  def __init__(self, name:str):
    self.name = name
    self.course = None
    self.teacher = None
    self.groups = []

class Teacher:
  def __init__(self, name:str, subject:Subject):
    self.name = name
    self.subject = subject

