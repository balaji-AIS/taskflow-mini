import unittest
from app.server import add_task

class TaskTests(unittest.TestCase):
    def test_add_task(self):
        result = add_task([], 'Write CI')
        self.assertEqual(result, [{'id': 1, 'title': 'Write CI'}])
    def test_second_task(self):
        result = add_task([{'id':1,'title':'First'}], 'Second')
        self.assertEqual(result[1]['id'], 2)
    def test_empty_task_rejected(self):
        with self.assertRaises(ValueError):
            add_task([], '  ')

if __name__ == '__main__': unittest.main()
