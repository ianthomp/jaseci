from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph

import jaseci.jac.tests.book_code as jtc
import sys
import io
from unittest import TestCase
from jaseci.utils.utils import TestCaseHelper


class jac_book_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.gph = graph(h=mem_hook())
        self.sent = sentinel(h=self.gph._h)
        self.old_stdout = sys.stdout
        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self):
        sys.stdout = self.old_stdout
        super().tearDown()

    def to_screen(self):
        sys.stdout = self.old_stdout
        print("output: ", self.new_stdout.getvalue())
        sys.stdout = self.new_stdout

    def test_basic_arith(self):
        self.sent.register_code(jtc.basic_arith)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "8 -20 1.0 -2 -13.0\n")

    def test_additional_arith(self):
        self.sent.register_code(jtc.more_arith)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "256 4\n")

    def test_compare(self):
        self.sent.register_code(jtc.compare)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "false true true false true false true\n")

    def test_logical(self):
        self.sent.register_code(jtc.logical)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "true false false true false true false true\n")

    def test_assignments(self):
        self.sent.register_code(jtc.assignments)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "8\n16\n36\n36.0\n-18.0\n")

    def test_if_stmt(self):
        self.sent.register_code(jtc.if_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "Hello!\n")

    def test_else_stmt(self):
        self.sent.register_code(jtc.else_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "A is not equal to B\n")

    def test_elif_stmt(self):
        self.sent.register_code(jtc.elif_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "A is one less than B\n")

    def test_for_stmt(self):
        self.sent.register_code(jtc.for_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "Hello 0 times!\nHello 1 times!\nHello 2 times!\n"
                         "Hello 3 times!\nHello 4 times!\nHello 5 times!\n"
                         "Hello 6 times!\nHello 7 times!\nHello 8 times!\n"
                         "Hello 9 times!\n")

    def test_while_stmt(self):
        self.sent.register_code(jtc.while_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "Hello 5 times!\nHello 4 times!\nHello 3 times!\n"
                         "Hello 2 times!\nHello 1 times!\n")

    def test_break_stmt(self):
        self.sent.register_code(jtc.break_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "Hello 0 times!\nHello 1 times!\nHello 2 times!\n"
                         "Hello 3 times!\nHello 4 times!\nHello 5 times!\n"
                         "Hello 6 times!\n")

    def test_continue_stmt(self):
        self.sent.register_code(jtc.continue_stmt)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "Hello 5 times!\nHello 4 times!\n"
                         "Hello 2 times!\nHello 1 times!\n")

    def test_destroy_disconnect(self):
        self.sent.register_code(jtc.destroy_disconn)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        # self.assertEqual(self.new_stdout.getvalue(),
        #                  "Hello 5 times!\nHello 4 times!\n"
        #                  "Hello 2 times!\nHello 1 times!\n")

    def test_array_assign(self):
        self.sent.register_code(jtc.array_assign)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "[[0, 0], [0, 0]]\n"
                         "[[1, 1], [0, 0]]\n"
                         "[[1, 2], [3, 4]]\n"
                         "[[1, 2], [1, 2]]\n")

    def test_md_array_assign(self):
        self.sent.register_code(jtc.array_md_assign)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "[[1, 2], [3, 4]]\n"
                         "[[1, 1], [3, 4]]\n")

    def test_dereference(self):
        self.sent.register_code(jtc.dereference)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue()[:9],
                         "urn:uuid:")

    def test_pre_post_walk(self):
        self.sent.register_code(jtc.pre_post_walking)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "count: 8\n")

    def test_pre_post_walk_disengage(self):
        self.sent.register_code(jtc.pre_post_walking_dis)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "count: 6\n")

    def test_length(self):
        self.sent.register_code(jtc.length)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "3\n3\n")

    def test_sort_by_col(self):
        self.sent.register_code(jtc.sort_by_col)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "[['b', 333], ['c', 245], ['a', 56]]\n"
                         "[['a', 56], ['b', 333], ['c', 245]]\n"
                         "[['c', 245], ['b', 333], ['a', 56]]\n"
                         "[['a', 56], ['c', 245], ['b', 333]]\n"
                         "[['b', 333], ['c', 245], ['a', 56]]\n")

    def test_list_remove_element(self):
        self.sent.register_code(jtc.list_remove)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "[['b', 333], ['c', 245], ['a', 56]]\n"
                         "[['b', 333], ['a', 56]]\n"
                         "[['b', 333]]\n")

    def test_can_action(self):
        self.sent.register_code(jtc.can_action)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "56 7\n"
                         "56 8\n")

    def test_cross_scope_report(self):
        self.sent.register_code(jtc.cross_scope_report)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertIn(56, gen_walker.report)
        self.assertIn(8, gen_walker.report)
        self.assertEqual(self.new_stdout.getvalue(),
                         "56 7\n"
                         "56 8\n")

    def test_has_private(self):
        self.sent.register_code(jtc.has_private)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        print(gen_walker.report)
        self.assertTrue(self.new_stdout.getvalue().startswith(
            "[{'context': {'apple': 12,"))

    def test_array_idx_of_expr(self):
        self.sent.register_code(jtc.array_idx_of_expr)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "3\n1\n")

    def test_dict_assign(self):
        self.sent.register_code(jtc.dict_assign)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "{'three': 3, 'four': 4}\n"
                         "{'three': 3, 'four': 55}\n"
                         "{'one': 1, 'two': 2}\n"
                         "2\n")

    def test_dict_md_assign(self):
        self.sent.register_code(jtc.dict_md_assign)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "{'one': {'inner': 44}, 'two': 2}\n"
                         "{'inner': 2}\n"
                         "2\n")

    def test_dict_keys(self):
        self.sent.register_code(jtc.dict_keys)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "{'one': {'inner': 44}, 'two': 2}\n"
                         "{'inner': 2}\n"
                         "2\n")

    def test_vector_softmax(self):
        self.sent.register_code(jtc.soft_max)
        gen_walker = self.sent.walker_ids.get_obj_by_name('init')
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(),
                         "[0.8360188  0.11314284 0.05083836]\n")