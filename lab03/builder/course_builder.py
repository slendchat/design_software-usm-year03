from models_immutable import *
from models_mutable import *

class Course_builder:
    """Собирает курс по шагам, валидирует и возвращает immutable снапшот."""
    def __init__(self) -> None:
        # draft (mutable)
        self.title: str | None = None
        self.description: str | None = None
        # subjects: list[{"name": str, "teacher": str}]
        self._subjects: list[dict] = []
        # groups: list[{"name": str, "students": list[dict]}]
        self._groups: list[dict] = []

    # --- fluent setters ---
    def set_title(self, title: str) -> "Course_builder":
        self.title = title
        return self

    def set_description(self, description: str) -> "Course_builder":
        self.description = description
        return self

    def add_subject(self, subject_name: str, teacher_name: str) -> "Course_builder":
        self._subjects.append({"name": subject_name, "teacher": teacher_name})
        return self

    def add_group(self, group_name: str) -> "Course_builder":
        # одна группа – один раз
        if any(g["name"] == group_name for g in self._groups):
            raise ValueError(f"Group '{group_name}' already exists")
        self._groups.append({"name": group_name, "students": []})
        return self

    def add_student(self, group_name: str, *, name: str, age: int, grade: int) -> "Course_builder":
        # один студент -> одна группа (твоя логика)
        group = next((g for g in self._groups if g["name"] == group_name), None)
        if group is None:
            raise ValueError(f"Group '{group_name}' not found")
        group["students"].append({"name": name, "age": age, "grade": grade})
        return self

    # --- validation ---
    def _validate(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Course.title is required")
        if not self.description or not self.description.strip():
            raise ValueError("Course.description is required")
        if not self._subjects:
            raise ValueError("At least one subject is required")
        if not self._groups:
            raise ValueError("At least one group is required")

        # уникальность имён
        subj_names = [s["name"] for s in self._subjects]
        if len(subj_names) != len(set(subj_names)):
            raise ValueError("Subject names must be unique within a course")

        group_names = [g["name"] for g in self._groups]
        if len(group_names) != len(set(group_names)):
            raise ValueError("Group names must be unique within a course")

        # в каждой группе должен быть хотя бы один студент
        for g in self._groups:
            if not g["students"]:
                raise ValueError(f"Group '{g['name']}' must have at least one student")

        # базовая проверка студентов
        for g in self._groups:
            for st in g["students"]:
                if not st["name"] or st["age"] < 0 or st["grade"] < 0:
                    raise ValueError(f"Invalid student in group '{g['name']}'")

    # --- build (mutable -> immutable) ---
    def build(self) -> Course_immutable:
        self._validate()

        subjects_imm = tuple(
            Subject_immutable(
                name=s["name"],
                teacher=Teacher_immutable(name=s["teacher"])
            )
            for s in self._subjects
        )

        groups_imm = tuple(
            Group_immutable(
                name=g["name"],
                students=tuple(
                    Student_immutable(**st) for st in g["students"]
                )
            )
            for g in self._groups
        )

        return Course_immutable(
            title=self.title,  # type: ignore[arg-type]
            description=self.description,  # type: ignore[arg-type]
            subjects=subjects_imm,
            groups=groups_imm,
        )


    