import unittest
from metrics import get_system_metrics, load_config

class TestCollector(unittest.TestCase):
    def test_collect_metrics(self):
        config = load_config()
        metrics = get_system_metrics(config)
        self.assertIn('cpu', metrics)
        self.assertIn('memory', metrics)
        self.assertIn('disk', metrics)

if __name__ == '__main__':
    unittest.main()