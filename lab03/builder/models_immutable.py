from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Course_immutable:
  title: str
  description: str
  groups: tuple[Group_immutable, ...]
  subjects: tuple[Subject_immutable, ...]

@dataclass(frozen=True)
class Group_immutable:
  name: str
  students: tuple[Student_immutable, ...]
  course: Course_immutable

@dataclass(frozen=True)
class Subject_immutable:
  name: str
  course: Course_immutable
  teacher: Teacher_immutable
  groups: tuple[Group_immutable, ...]

@dataclass(frozen=True)
class Teacher_immutable:
  name: str
  subject: Subject_immutable

@dataclass(frozen=True)
class Student_immutable:
  name: str
  age: int
  grade: int
  group: tuple[Group_immutable, ...]
  subjects: tuple[Subject_immutable, ...]
  teachers: tuple[Teacher_immutable, ...]