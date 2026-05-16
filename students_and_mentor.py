class GradesFeature:
    def __init__(self):
        self.grades = {}

    def avg_grade(self) -> float:
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
    def __init__(self, name, surname, gender):
        super().__init__()
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []

    def rate_lecture(self, mentor, course, grade):
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
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


class Lecturer(Mentor, GradesFeature):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        GradesFeature.__init__(self)

    def __str__(self):
        return f'{super().__str__()}\nСредняя оценка за лекции: {self.avg_grade():.1f}'


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Алёха', 'Ольгина', 'Ж')

student.courses_in_progress += ['Python', 'Java']
student2.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

reviewer.rate_hw(student, 'Python', 2)
reviewer.rate_hw(student, 'Python', 7)
reviewer.rate_hw(student, 'Python', 1)

reviewer.rate_hw(student2, 'Python', 2)
reviewer.rate_hw(student2, 'Python', 7)
reviewer.rate_hw(student2, 'Python', 1)

student.rate_lecture(lecturer, 'Python', 2)
student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Python', 7)

print(student)
print(lecturer)
print(reviewer)

print(student == student2)
print(student > student2)
print(student < student2)
print(student >= student2)
print(student <= student2)
