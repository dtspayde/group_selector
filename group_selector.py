#!/usr/bin/env python3
# coding: utf-8

import random
import numpy as np
from pathlib import Path
import itertools
import json
import operator

class Student(object):
    """ The Student class describes a student in the classroom
    
    Attributes
    ----------
    id_number  : student's ID number
    last_name  : student's last name
    first_name : student's first name
    gender     : student's gender
    """
    
    def __init__(self, id_number, last_name, first_name, gender = None):
        """ Initializes Student with appropriate default values """

        self.gender = gender
        if self.gender is not None:
            self.gender = self.gender[0].lower()
            if self.gender != 'm' and self.gender != 'f':
                raise ValueError("Please provide gender as 'm' or 'f'.")

        self.last_name = last_name
        self.first_name = first_name
        self.id_number = id_number

    def __repr__(self):

        return (f'{self.__class__.__name__}('
                f'{self.id_number}, {self.first_name!r}, {self.last_name!r}, {self.gender!r})'
                )

class Group(object):
    """ The group class contains a collection of students to work together

    """

    def __init__(self):
        self.students = []

    def __iter__(self):
        return iter(self.students)

    def __len__(self):
        return len(self.students)

    def add_student(self, student):

        print("Adding student", student)
        self.students.append(student)

    def print_students(self):
        
        print(self.students)
        # (print(student) for student in self.students)

    def check_composition(self):
        n_m = 0
        n_f = 0

        for student in self.students:
            if student.gender == 'm':
                n_m += 1
            if student.gender == 'f':
                n_f += 1

        # print(n_m, n_f)

        if 0 < n_f < n_m:
            return False
        else:
            return True

class Classroom(object):
    """ Classroom is a collection of all Students that compose the class
    """

    def __init__(self):

        self.students = []
        self.n_students = 0
        self.student_ids = []
        self.dict_history = {}

    def add_student(self, student):
        print(f"Adding student {student} to class.")
        # student.id_number = self.n_students
        self.students.append(student)
        self.student_ids.append(student.id_number)
        self.n_students += 1

    def load_students(self, filename = 'student_list.txt'):
        file = Path(filename)

        if not file.exists():
            raise Exception(f'Student list file does not exist.')

        for line in file.read_text().splitlines():
            (student_id, first_name, last_name, gender) = (item.strip() for item in line.split(','))
            self.add_student(Student(id_number = student_id, first_name = first_name, 
                last_name = last_name, gender = gender))

    def load_student_history(self, filename = 'students_history.txt'):
        file = Path(filename)

        if file.exists():
            with file.open(mode='r') as f:
                self.dict_history = json.load(f)
        else:
            for id in self.student_ids:
                dict_line = {}
                for partner_id in self.student_ids:
                    if partner_id == id:
                        continue
                    dict_line[partner_id] = 0
                self.dict_history[id] = dict_line

    def store_student_history(self, filename = 'students_history.txt'):
        file = Path(filename)
        
        with file.open(mode='w') as f:
            json.dump(self.dict_history, f)

    def __iter__(self):
        return iter(self.students)

    def print_students(self):
        print(self.students)
        
    def calculate_n_groups(self, n_members, n_students = None, groups = None):

        if groups is None:
            groups = {}

        if n_students is None:
            n_students = self.n_students

        if n_students == 0:
            pass
        elif n_students == 1:
            groups[n_members + 1] -= 1
            n_students += n_members + 1

            if n_members == 1:
                if n_students in groups.keys():
                    groups[n_students] += 1
                else:
                    groups[n_students] = 1

                n_students = 0

            self.calculate_n_groups(n_members, n_students, groups)

        elif n_students <= n_members:
            n_groups = 1
            groups[n_students] = n_groups
        else:
            n_groups = n_students // n_members
            n_students = n_students % n_members
            groups[n_members] = n_groups

            self.calculate_n_groups(n_members - 1, n_students, groups)

        return groups

def main():

    classroom = Classroom()

    classroom.load_students()
    classroom.load_student_history()

    d_groups = classroom.calculate_n_groups(3)
    print(d_groups, sum(s*g for s, g in d_groups.items()))

    success = False
    session = []

    while not success:

        session.clear()
        student_list = classroom.students.copy()
        random.shuffle(student_list)
        n_group = 0

        for size, number in d_groups.items():
            for i in range(number):
                group = Group()
                print(f'Creating group number {n_group} with {size} members...')
                n_group += 1

                student = student_list.pop()
                group.add_student(student)
                student_history = classroom.dict_history[student.id_number]

                possible_partners = sorted(student_history.items(), key=operator.itemgetter(1), 
                        reverse=True)
                possible_ids = []
                for partner in possible_partners:
                    for student in student_list:
                        if partner[0] == student.id_number:
                            possible_ids.append(partner[0])

                student_ids = [student.id_number for student in student_list]

                # print(f"student_list = {student_list}")
                # print(f"possible_partners = {possible_partners}")

                # print(f"student_ids = {student_ids}")
                # print(f"possible_ids = {possible_ids}")

                # print(f"{i} {number} {size} : {student.id_number} : {possible_partners}")
                # print(f"{len(student_list)} : {student_list}")

                for j in range(size-1):
                    partner_id = possible_ids.pop()
                    for student in student_list:
                        if student.id_number == partner_id:
                            group.add_student(student)
                            break

                if group.check_composition():
                    session.append(group)
                    for student in group:
                        if student in student_list:
                            student_list.remove(student)
                    success = True
                else:
                    print(f'Failed composition check')
                    group.print_students()
                    success = False
                    break
            if not success:
                break

                    
    for i, group in enumerate(session):
        print(f'Group {i}: {len(group)} ')
        group.print_students()
        for student in group:
            for partner in group:
                if partner != student:
                    classroom.dict_history[student.id_number][partner.id_number] += 1

    classroom.store_student_history()
    return

if __name__ == "__main__":
    main()

