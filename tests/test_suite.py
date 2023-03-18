from __future__ import annotations

import unittest

import group_selector.group_selector as m


class TestClassStudent(unittest.TestCase):
    def test_no_id_number(self):
        self.assertRaises(TypeError, m.Student, last_name="Smith", first_name="John")

    def test_no_last_name(self):
        self.assertRaises(TypeError, m.Student, id_number=1, first_name="John")

    def test_no_first_name(self):
        self.assertRaises(TypeError, m.Student, id_number=1, last_name="Smith")

    def test_wrong_gender(self):
        self.assertRaises(
            ValueError,
            m.Student,
            id_number=1,
            last_name="Smith",
            first_name="John",
            gender="c",
        )


class TestClassGroup(unittest.TestCase):
    def setUp(self):
        self.student = []
        self.student.append(
            m.Student(id_number=1, last_name="Smith", first_name="John", gender="m")
        )
        self.student.append(
            m.Student(id_number=2, last_name="Doe", first_name="Jim", gender="m")
        )
        self.student.append(
            m.Student(id_number=3, last_name="Mills", first_name="Jane", gender="f")
        )
        self.student.append(
            m.Student(id_number=3, last_name="Cook", first_name="Jill", gender="f")
        )

        self.bad_group = [0, 1, 2]
        self.good_mixed_group = [0, 2, 3]
        self.good_equal_group = [0, 1, 2, 3]
        self.good_female_group = [2, 3]
        self.good_male_group = [0, 1]

    def test_bad_group_composition(self):
        group = m.Group()

        for i in self.bad_group:
            group.add_student(self.student[i])

        assert not group.check_composition()

    def test_good_mixed_group_composition(self):
        group = m.Group()

        for i in self.good_mixed_group:
            group.add_student(self.student[i])

        assert group.check_composition()

    def test_good_equal_group_composition(self):
        group = m.Group()

        for i in self.good_equal_group:
            group.add_student(self.student[i])

        assert group.check_composition()

    def test_good_female_group_composition(self):
        group = m.Group()

        for i in self.good_female_group:
            group.add_student(self.student[i])

        assert group.check_composition()

    def test_good_male_group_composition(self):
        group = m.Group()

        for i in self.good_male_group:
            group.add_student(self.student[i])

        assert group.check_composition()
        assert group.check_composition()
