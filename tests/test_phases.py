from datetime import datetime as dt
import unittest

from moon import phasecalc as pc

class PhaseTest(unittest.TestCase):

    def test_phases(self):
        self.assertEqual(pc.get_phase(_dt('2025-04-11 13:19:00')), 'waxing gibbous')
        self.assertEqual(pc.get_phase(_dt('2025-04-12 13:19:00')), 'full moon')
        self.assertEqual(pc.get_phase(_dt('2025-04-27 13:19:00')), 'new moon')

    def test_illumination(self):
        self.assertAlmostEqual(pc.get_illumination(_dt('2025-04-12 09:40:00')), 99.6, 1)
        self.assertAlmostEqual(pc.get_illumination(_dt('2025-04-20 12:30:30')), 55.9, 1)
        self.assertAlmostEqual(pc.get_illumination(_dt('2025-04-27 13:19:00')), 0.2, 1)

    def test_up_down(self):
        data = pc.get_rise_set(_dt('2025-04-12 10:15:00'))
        self.assertFalse(data[0])

        data = pc.get_rise_set(_dt('2025-04-12 23:37:00'))
        self.assertTrue(data[0])

        data = pc.get_rise_set(_dt('2025-04-14 04:30:00'))
        self.assertTrue(data[0])

    # We're basically just testing the library here, but it'll prove the code runs
    def test_constellation(self):
        self.assertEqual(pc.get_constellation(_dt('2025-04-12 13:19:00'))[0], 'Virgo')
        self.assertEqual(pc.get_constellation(_dt('2025-04-15 13:19:00'))[0], 'Libra')
        self.assertEqual(pc.get_constellation(_dt('2025-04-17 13:19:00'))[0], 'Ophiuchus')

def _dt(dtstr: str) -> dt:
    return dt.strptime(dtstr, '%Y-%m-%d %H:%M:%S')

    