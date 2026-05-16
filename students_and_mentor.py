class GradesFeature:
    """Класс, расширяющий возможности работы с оценками."""
    def __init__(self):
        self.grades = {}

    def avg_grade(self) -> float:
        """Вычисление среднего значения среди всех оценок."""
        grades_all = []
        for grade in self.grades.values():
            grades_all += grade
        return 0 if len(grades_all) == 0 else sum(grades_all) / len(grades_all)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.avg_grade() == other.avg_grade()

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.avg_grade() > other.avg_grade()

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.avg_grade() < other.avg_grade()

    def __ge__(self, other):
        if isinstance(other, type(self)):
            return self.avg_grade() >= other.avg_grade()

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.avg_grade() <= other.avg_grade()


class Student(GradesFeature):
    """Студент."""
    def __init__(self, name, surname, gender):
        super().__init__()
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []

    def rate_lecture(self, mentor, course, grade):
        """Оценка лекции студентом."""
        if (isinstance(mentor, Lecturer)
                and course in self.courses_in_progress
                and course in mentor.courses_attached
                and 0 < grade < 11):
            if course in mentor.grades:
                mentor.grades[course] += [grade]
            else:
                mentor.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return '\n'.join([
            f'Имя: {self.name}',
            f'Фамилия: {self.surname}',
            f'Средняя оценка за домащние задания: {self.avg_grade():.1f}',
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}',
            f'Завершенные курсы: {", ".join(self.finished_courses)}',
        ])


class Mentor:
    """Эксперт (Абстрактный класс)."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


class Lecturer(Mentor, GradesFeature):
    """Эксперт, ведущий лекции"""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        GradesFeature.__init__(self)

    def __str__(self):
        return f'{super().__str__()}\nСредняя оценка за лекции: {self.avg_grade():.1f}'


class Reviewer(Mentor):
    """Эксперт, проверяющий домашние задания."""
    def rate_hw(self, student, course, grade):
        """Оценка работы студента."""
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Пётр', 'Петров')
reviewer1 = Reviewer('Антон', 'Антонов')
reviewer2 = Reviewer('Андрей', 'Андреев')
student1 = Student('Ольга', 'Ольгина', 'Ж')
student2 = Student('Олег', 'Олеев', 'М')

student1.courses_in_progress += ['Python', 'C++']
student2.courses_in_progress += ['Python', 'Java']
lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Java']
reviewer1.courses_attached += ['Python', 'C++']
reviewer2.courses_attached += ['Java']

reviewer1.rate_hw(student1, 'Python', 2)
reviewer2.rate_hw(student1, 'Java', 7)
reviewer1.rate_hw(student1, 'C++', 1)
reviewer1.rate_hw(student1, 'C++', 7)

reviewer1.rate_hw(student2, 'Python', 5)
reviewer1.rate_hw(student2, 'Java', 7)
reviewer1.rate_hw(student2, 'Python', 1)
reviewer2.rate_hw(student2, 'Java', 7)

student1.rate_lecture(lecturer1, 'Python', 2)
student1.rate_lecture(lecturer1, 'Python', 1)
student1.rate_lecture(lecturer1, 'C++', 10)
student1.rate_lecture(lecturer2, 'Python', 7)
student2.rate_lecture(lecturer2, 'Java', 7)

print(f'{student1}\n')
print(f'{student2}\n')
print(f'{lecturer1}\n')
print(f'{lecturer2}\n')
print(f'{reviewer1}\n')
print(f'{reviewer2}\n')

print(student1 == student2)
print(student1 > student2)
print(student1 < student2)
print(student1 >= student2)
print(student1 <= student2)

print(lecturer1 == lecturer2)
print(lecturer1 > lecturer2)
print(lecturer1 < lecturer2)
print(lecturer1 >= lecturer2)
print(lecturer1 <= lecturer2)


def avg_grade_all(peoples, course) -> float:
    """Подсчет средней оценки по курсу\n
    Args:
        peoples (list): список студентов или лекторов
        course (str): название курса
    """
    grades_all = []

    # список только из студентов или только из лекторов
    if (all(isinstance(value, Student) for value in peoples) or
            all(isinstance(value, Lecturer) for value in peoples)):
        for people in peoples:
            if course in people.grades:
                grades_all += people.grades[course]
        return 0 if len(grades_all) == 0 else sum(grades_all) / len(grades_all)


print(avg_grade_all([lecturer1, lecturer2], 'Java'))
print(avg_grade_all([student1, student2], 'Python'))


# Ниже представлена реализация отдельными функциями
# Вдруг с одной общей задание не засчитают :)


def avg_grade_all_students(students, course) -> float:
    """Подсчет средней оценки по курсу\n
    Args:
        students (list): список студентов
        course (str): название курса
    """
    grades_all = []

    # список только из студентов
    if all(isinstance(value, Student) for value in students):
        for people in students:
            if course in people.grades:
                grades_all += people.grades[course]
        return 0 if len(grades_all) == 0 else sum(grades_all) / len(grades_all)


def avg_grade_all_lectors(lectors, course) -> float:
    """Подсчет средней оценки по курсу\n
    Args:
        lectors (list): список лекторов
        course (str): название курса
    """
    grades_all = []

    # список только из лекторов
    if all(isinstance(value, Lecturer) for value in lectors):
        for people in lectors:
            if course in people.grades:
                grades_all += people.grades[course]
        return 0 if len(grades_all) == 0 else sum(grades_all) / len(grades_all)
