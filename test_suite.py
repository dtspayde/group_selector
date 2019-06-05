import unittest

import group_selector


class TestClassStudent(unittest.TestCase):

    def test_no_id_number(self):
        self.assertRaises(TypeError, group_selector.Student,
                          last_name="Smith", first_name="John")

    def test_no_last_name(self):
        self.assertRaises(TypeError, group_selector.Student, id_number=1,
                          first_name="John")

    def test_no_first_name(self):
        self.assertRaises(TypeError, group_selector.Student, id_number=1,
                          last_name="Smith")

    def test_wrong_gender(self):
        self.assertRaises(ValueError, group_selector.Student, id_number=1,
                          last_name="Smith", first_name="John", gender="c")


class TestClassGroup(unittest.TestCase):

    def test_bad_group_composition(self):
        student1 = group_selector.Student(id_number=1, last_name="Smith",
                                          first_name="John", gender="m")
        student2 = group_selector.Student(id_number=2, last_name="Doe",
                                          first_name="Jim", gender="m")
        student3 = group_selector.Student(id_number=3, last_name="Mills",
                                          first_name="Jane", gender="f")
        group = group_selector.Group()
        group.add_student(student1)
        group.add_student(student2)
        group.add_student(student3)

        self.assertFalse(group.check_composition())

    def test_good_mixed_group_composition(self):
        student1 = group_selector.Student(id_number=1, last_name="Smith",
                                          first_name="John", gender="m")
        student2 = group_selector.Student(id_number=2, last_name="Doe",
                                          first_name="Jill", gender="f")
        student3 = group_selector.Student(id_number=3, last_name="Mills",
                                          first_name="Jane", gender="f")
        group = group_selector.Group()
        group.add_student(student1)
        group.add_student(student2)
        group.add_student(student3)

        self.assertTrue(group.check_composition())

    def test_good_equal_group_composition(self):
        student1 = group_selector.Student(id_number=1, last_name="Smith",
                                          first_name="John", gender="m")
        student2 = group_selector.Student(id_number=2, last_name="Doe",
                                          first_name="Jim", gender="m")
        student3 = group_selector.Student(id_number=3, last_name="Mills",
                                          first_name="Jane", gender="f")
        student4 = group_selector.Student(id_number=3, last_name="Cook",
                                          first_name="Jill", gender="f")
        group = group_selector.Group()
        group.add_student(student1)
        group.add_student(student2)
        group.add_student(student3)
        group.add_student(student4)

        self.assertTrue(group.check_composition())

    def test_good_female_group_composition(self):
        student3 = group_selector.Student(id_number=3, last_name="Mills",
                                          first_name="Jane", gender="f")
        student4 = group_selector.Student(id_number=3, last_name="Cook",
                                          first_name="Jill", gender="f")
        group = group_selector.Group()
        group.add_student(student3)
        group.add_student(student4)

        self.assertTrue(group.check_composition())

    def test_good_male_group_composition(self):
        student1 = group_selector.Student(id_number=1, last_name="Smith",
                                          first_name="John", gender="m")
        student2 = group_selector.Student(id_number=2, last_name="Doe",
                                          first_name="Jim", gender="m")
        group = group_selector.Group()
        group.add_student(student1)
        group.add_student(student2)

        self.assertTrue(group.check_composition())
