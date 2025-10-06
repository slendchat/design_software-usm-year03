from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class Course_immutable:
  title: str
  description: str
  groups: Optional[tuple[Group_immutable, ...]] = None
  subjects: Optional[tuple[Subject_immutable, ...]] = None

@dataclass(frozen=True)
class Group_immutable:
  name: str
  students: Optional[tuple[Student_immutable, ...]] = None
  course: Optional[Course_immutable] = None

@dataclass(frozen=True)
class Subject_immutable:
  name: str
  course: Optional[Course_immutable] = None
  teacher: Optional[Teacher_immutable] = None
  groups: Optional[tuple[Group_immutable, ...]] = None

@dataclass(frozen=True)
class Teacher_immutable:
  name: str
  subject: Optional[Subject_immutable] = None

@dataclass(frozen=True)
class Student_immutable:
  name: str
  age: int
  grade: int
  group: Optional[tuple[Group_immutable, ...]] = None
  subjects: Optional[tuple[Subject_immutable, ...]] = None
  teachers: Optional[tuple[Teacher_immutable, ...]] = None