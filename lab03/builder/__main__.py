from course_builder import Course_builder

def main():
  course = (
        Course_builder()
        .set_title("Software Engineering")
        .set_description("Design patterns & team projects")
        .add_subject("OOP", "Dina")
        .add_subject("Databases", "Andrei")
        .add_group("SE-31")
        .add_student("SE-31", name="Artur", age=21, grade=3)
        .add_student("SE-31", name="Grisha", age=22, grade=3)
        .build()
    )
  print(course)

if __name__ == "__main__":
  main()