import unittest
from app.server import add_task, completed_task_count, set_task_completed

class TaskTests(unittest.TestCase):
    def test_add_task(self):
        result = add_task([], 'Write CI')
        self.assertEqual(result, [{'id': 1, 'title': 'Write CI', 'completed': False}])
    def test_second_task(self):
        result = add_task([{'id':1,'title':'First'}], 'Second')
        self.assertEqual(result[1]['id'], 2)
    def test_empty_task_rejected(self):
        with self.assertRaises(ValueError):
            add_task([], '  ')

    def test_completed_task_count(self):
        tasks = [
            {'id': 1, 'title': 'First', 'completed': True},
            {'id': 2, 'title': 'Second', 'completed': False},
            {'id': 3, 'title': 'Legacy task'},
        ]
        self.assertEqual(completed_task_count(tasks), 1)

    def test_set_task_completed(self):
        tasks = [{'id': 1, 'title': 'First', 'completed': False}]
        result = set_task_completed(tasks, 1, True)
        self.assertTrue(result[0]['completed'])
        self.assertFalse(tasks[0]['completed'])

    def test_set_task_completed_rejects_unknown_task(self):
        with self.assertRaisesRegex(ValueError, 'Task not found'):
            set_task_completed([], 99, True)

if __name__ == '__main__': unittest.main()
