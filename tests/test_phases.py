from datetime import datetime as dt
import time
import unittest

from moon import phasecalc as pc

class PhaseTest(unittest.TestCase):

    def test_phases(self):
        self.assertEqual(pc.get_phase(_ts('2025-04-11 13:19:00')), 'waxing gibbous')
        self.assertEqual(pc.get_phase(_ts('2025-04-12 13:19:00')), 'full moon')
        self.assertEqual(pc.get_phase(_ts('2025-04-27 13:19:00')), 'new moon')

    def test_illumination(self):
        self.assertAlmostEqual(pc.get_illumination(_ts('2025-04-11 13:19:00')), 98.8, 1)
        self.assertAlmostEqual(pc.get_illumination(_ts('2025-04-20 13:19:00')), 9.8, 1)


def _ts(dtstr: str) ->int:
    mydt = dt.strptime(dtstr, '%Y-%m-%d %H:%M:%S')
    return int(mydt.timestamp())
    