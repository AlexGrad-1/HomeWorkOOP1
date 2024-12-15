class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.lecturer_grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: Объект не является лектором'
        if course not in lecturer.courses_attached:
            return 'Ошибка: Лектор не ведет этот курс'
        if course not in self.courses_in_progress:
            return 'Ошибка: Студент не изучает данный курс'
        if course in self.lecturer_grades:
            self.lecturer_grades[course] += [grade]
        else:
            self.lecturer_grades[course] = [grade]
        return "Оценка успешно добавлена"  # Уведомление об успехе

    def __str__(self):
        average_grade = self.average_grade(self.grades) if self.grades else 0
        average_lecturer_grade = self.average_grade(self.lecturer_grades) if self.lecturer_grades else 0
        courses_in_progress_str = ", ".join(self.courses_in_progress) if self.courses_in_progress else "Нет"
        finished_courses_str = ", ".join(self.finished_courses) if self.finished_courses else "Нет"
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {average_grade:.1f}\nСредняя оценка за лекции: {average_lecturer_grade:.1f}\nКурсы в процессе изучения: {courses_in_progress_str}\nЗавершенные курсы: {finished_courses_str}"

    def average_grade(self, grades_dict):
        all_grades = [grade for course_grades in grades_dict.values() for grade in course_grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __gt__(self, other):
        if not isinstance(other, Student):
            raise TypeError("Сравнивать можно только объекты класса Student")
        return self.average_grade(self.grades) > other.average_grade(other.grades)

    def __lt__(self, other):
        if not isinstance(other, Student):
            raise TypeError("Сравнивать можно только объекты класса Student")
        return self.average_grade(self.grades) < other.average_grade(other.grades)

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False  # сравниваем только с студентами
        return self.average_grade(self.grades) == other.average_grade(other.grades)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def rate_lectures(self, student, course, grade):
        if not isinstance(student, Student):
            return "Ошибка: Объект не является студентом"
        if course not in self.courses_attached:
            return 'Ошибка: Лектор не ведет этот курс'
        if course not in student.courses_in_progress:
            return 'Ошибка: Студент не изучает данный курс'
        if course in self.grades:
            self.grades[course] += [grade]
        else:
            self.grades[course] = [grade]

    def __str__(self):
        average_grade = self.average_grade(self.grades) if self.grades else 0
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {average_grade:.1f}"

    def average_grade(self, grades_dict):
        all_grades = [grade for course_grades in grades_dict.values() for grade in course_grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError("Сравнивать можно только объекты класса Lecturer")
        return self.average_grade(self.grades) > other.average_grade(other.grades)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            raise TypeError("Сравнивать можно только объекты класса Lecturer")
        return self.average_grade(self.grades) < other.average_grade(other.grades)

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return False  # сравниваем только с лекторами
        return self.average_grade(self.grades) == other.average_grade(other.grades)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            return "Ошибка: Объект не является студентом"
        if course not in self.courses_attached:
            return 'Ошибка: Рецензент не ведет этот курс'
        if course not in student.courses_in_progress:
            return 'Ошибка: Студент не изучает данный курс'
        if course in student.grades:
            student.grades[course] += [grade]
        else:
            student.grades[course] = [grade]

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Функции для подсчета средних оценок
def average_hw_grade_for_course(students, course):
    """Вычисляет среднюю оценку за домашние задания по всем студентам для заданного курса."""
    total_grades = 0
    student_count = 0
    for student in students:
        if course in student.grades:
            total_grades += sum(student.grades[course])
            student_count += len(student.grades[course])
    return total_grades / student_count if student_count > 0 else 0


def average_lecture_grade_for_course(lecturers, course):
    """Вычисляет среднюю оценку за лекции по всем лекторам для заданного курса."""
    total_grades = 0
    lecturer_count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades += sum(lecturer.grades[course])
            lecturer_count += len(lecturer.grades[course])
    return total_grades / lecturer_count if lecturer_count > 0 else 0


# Создание экземпляров классов
student1 = Student('Ruoy', 'Eman', 'your_gender')
student2 = Student('Alice', 'Smith', 'female')
student1.courses_in_progress += ['Python', 'Git']
student2.courses_in_progress += ['Python']
student1.finished_courses += ['Введение в программирование']

reviewer1 = Reviewer('Some', 'Buddy')
reviewer2 = Reviewer('Jane', 'Doe')
reviewer1.courses_attached += ['Python', 'Git']
reviewer2.courses_attached += ['Python']

lecturer1 = Lecturer('John', 'Doe')
lecturer2 = Lecturer('Mike', 'Smith')
lecturer1.courses_attached += ['Python', 'Git']
lecturer2.courses_attached += ['Python']

# Вызовы методов и выставление оценок
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Git', 10)

reviewer2.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student2, 'Python', 7)

lecturer1.rate_lectures(student1, 'Python', 9)
lecturer1.rate_lectures(student1, 'Python', 10)
lecturer1.rate_lectures(student1, 'Git', 10)
lecturer2.rate_lectures(student2, 'Python', 7)
lecturer2.rate_lectures(student2, 'Python', 6)

student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer1, 'Git', 10)

student2.rate_lecturer(lecturer2, 'Python', 8)
student2.rate_lecturer(lecturer2, 'Python', 7)

# Вывод информации об объектах
print("\nИнформация о студентах:")
print(student1)
print(student2)

print("\nИнформация о лекторах:")
print(lecturer1)
print(lecturer2)

print("\nИнформация о рецензентах:")
print(reviewer1)
print(reviewer2)

# Сравнение лекторов
print(f"\nЛектор {lecturer1.name} > Лектор {lecturer2.name}: {lecturer1 > lecturer2}")  # True or False
print(f"Лектор {lecturer1.name} < Лектор {lecturer2.name}: {lecturer1 < lecturer2}")  # True or False
print(f"Лектор {lecturer1.name} == Лектор {lecturer2.name}: {lecturer1 == lecturer2}")  # True or False

# Сравнение студентов
print(f"\nСтудент {student1.name} > Студент {student2.name}: {student1 > student2}")  # True or False
print(f"Студент {student1.name} < Студент {student2.name}: {student1 < student2}")  # True or False
print(f"Студент {student1.name} == Студент {student2.name}: {student1 == student2}")  # True or False

# Вызов функций для подсчета средних оценок
students = [student1, student2]
lecturers = [lecturer1, lecturer2]
course_name = 'Python'

average_hw = average_hw_grade_for_course(students, course_name)
average_lecture = average_lecture_grade_for_course(lecturers, course_name)

print(f"\nСредняя оценка за домашние задания по курсу '{course_name}': {average_hw:.1f}")
print(f"Средняя оценка за лекции по курсу '{course_name}': {average_lecture:.1f}")

course_name = 'Git'
average_hw = average_hw_grade_for_course(students, course_name)
average_lecture = average_lecture_grade_for_course(lecturers, course_name)

print(f"\nСредняя оценка за домашние задания по курсу '{course_name}': {average_hw:.1f}")
print(f"Средняя оценка за лекции по курсу '{course_name}': {average_lecture:.1f}")
