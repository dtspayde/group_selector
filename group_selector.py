#!/usr/bin/env python3
# coding: utf-8

import random
from pathlib import Path
import json
import operator
import collections
import datetime
import logging

import click

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-6s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Student(object):
    """ The Student class describes a student in the classroom

    Attributes
    ----------
    id_number  : student's ID number
    last_name  : student's last name
    first_name : student's first name
    gender     : student's gender
    """

    def __init__(self, id_number, last_name, first_name, gender=None):

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
                f'{self.id_number}, {self.first_name!r},'
                f'{self.last_name!r}, {self.gender!r})'
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

        logger.debug("Adding student %s", student)
        self.students.append(student)

    def print_students(self):

        print(self.students)

    def check_composition(self):
        """ This function checks to make sure that the group does not contain
        more male than female students.
        """

        n_m = 0
        n_f = 0

        for student in self.students:
            if student.gender == 'm':
                n_m += 1
            if student.gender == 'f':
                n_f += 1

        return not (0 < n_f < n_m)


class Classroom(object):
    """ Classroom is a collection of all Students that compose the class
    """

    def __init__(self):

        self.students = []
        self.n_students = 0
        self.student_ids = []
        self.dict_history = {}
        self.groups = []
        self.shape_groups = {}

    def str_groups(self, groups=None):
        """ This function returns a string with the groups in Markdown
        format.
        """

        if groups is None:
            groups = self.groups

        str_title = f'# Groups created on {datetime.datetime.now()} # \n'
        str_header = f'Group '
        str_dashes = f'----- '
        roles = ('Manager', 'Scribe', 'Reporter', 'Skeptic')
        _ = ''
        for role in roles:
            str_header += f'{role:18s} '
            str_dashes += f'{_:-^18s} '

        str_header += '\n'
        str_dashes += '\n'

        str_final = str_title + '\n' + str_header + str_dashes

        for i, group in enumerate(groups):
            str = f'{i+1:^5d} '
            for student in group:
                str += f'{student.first_name[0]}. {student.last_name:15s} '
            str += '\n'
            str_final += str

        str_final += '\n'

        return str_final

    def add_student(self, student):
        logger.info(f"Adding student {student} to class.")
        self.students.append(student)
        self.student_ids.append(student.id_number)
        self.n_students += 1

    def load_students(self, filename='student_list.txt'):
        file = Path(filename)

        if not file.exists():
            raise Exception(f'Student list file does not exist.')

        for line in file.read_text().splitlines():
            (student_id, first_name, last_name, gender) = (
                item.strip() for item in line.split(','))
            self.add_student(
                Student(id_number=student_id, first_name=first_name,
                        last_name=last_name, gender=gender))

    def load_student_history(self, filename='students_history.txt'):
        """ The student history file records group history information in a
        machine-readable format.  This is used to minimize the number of
        repeat pairings.
        """

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

    def store_student_history(self, filename='students_history.txt'):
        file = Path(filename)

        with file.open(mode='w') as f:
            json.dump(self.dict_history, f)

    def update_student_history(self):
        for i, group in enumerate(self.groups):
            for student in group:
                for partner in group:
                    if partner != student:
                        sid = student.id_number
                        pid = partner.id_number
                        self.dict_history[sid][pid] += 1

    def store_groups(self, filename='groups.txt'):
        file = Path(filename)

        # str = ''
        str = file.read_text() if file.exists() else ''

        str_final = self.str_groups() + str

        file.write_text(str_final)

    def __iter__(self):
        return iter(self.students)

    def print_students(self):
        print(self.students)

    def histogram_partner_data(self):
        histo = collections.Counter()
        for sub_dicts in self.dict_history.values():
            histo.update(sub_dicts.values())

        return histo

    def print_partner_data(self):
        """ This function is used to print the number of repeat pairings and
        the count.
        """

        histo = self.histogram_partner_data()

        for n_times in sorted(histo.keys()):
            logger.debug(f'{n_times} = {int(histo[n_times]/2)}')

    def calculate_n_groups(self, n_members, n_students=None, groups=None):
        """
        Given a number of students in the class and a number of desired
        members, this function determines the number of groups and how many
        members in each group.
        """

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

        self.shape_groups = groups
        return groups

    def form_groups(self):

        success = False
        session = []

        while not success:

            session.clear()
            student_list = self.students.copy()
            random.shuffle(student_list)
            n_group = 0

            for size, number in self.shape_groups.items():
                for i in range(number):
                    group = Group()
                    logger.info(
                            f'Creating group {n_group} with {size} members...')
                    n_group += 1

                    student = student_list.pop()
                    group.add_student(student)
                    student_history = self.dict_history[student.id_number]

                    possible_partners = sorted(student_history.items(),
                                               key=operator.itemgetter(1),
                                               reverse=True)
                    possible_ids = []
                    for partner in possible_partners:
                        for student in student_list:
                            if partner[0] == student.id_number:
                                possible_ids.append(partner[0])

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
                        logger.info(f'Failed composition check')
                        success = False
                        break
                if not success:
                    break

        self.groups = session


@click.command()
@click.option('--n_members', '-n', default=3, show_default=True)
@click.option('--f_group', '-g', default='groups.txt', show_default=True,
              type=click.Path(exists=False, readable=True))
@click.option('--f_history', '-g', default='history.txt', show_default=True,
              type=click.Path(exists=False, readable=True))
@click.argument('f_students', type=click.Path(exists=True, readable=True))
def cli(n_members, f_group, f_history, f_students):
    """ This program will generate a set of groups from a class roster F_STUDENTS.

    The file F_STUDENTS should be comma separated.  Each line is one student
    with the following fields:  student ID number, first name, second name, and
    gender (f or m).  No comments or comment lines are allowed.

    The script will spread partners around before repeating; it is not truly
    random.  It will not allow groups with more male than female members to be
    formed.  This is a brute force process - all groups will be thrown out if
    one gets formed with the wrong balance.
    """

    classroom = Classroom()

    classroom.load_students(filename=f_students)

    classroom.load_student_history(filename=f_history)

    classroom.calculate_n_groups(3)

    classroom.form_groups()

    print("")
    print("Here's the next set of groups")
    print("")
    print(classroom.str_groups())

    classroom.store_groups(filename=f_group)

    classroom.update_student_history()

    classroom.print_partner_data()

    classroom.store_student_history(filename=f_history)

    return


if __name__ == "__main__":
    cli()
