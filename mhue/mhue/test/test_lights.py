import unittest

from mhue.mhue.common import HueConnection
from mhue.mhue.hue_objects.lights import Lights


class TestLights(unittest.TestCase):

    def test_get_lights(self):
        lights = Lights(HueConnection('../private.json'))
        self.assertTrue(isinstance(lights, Lights))

    def test_set_lights(self):
        lights = Lights(HueConnection('../private.json'))
        # TODO: actually test that lights can be set. Have to handle the response.
        state = {'on': True}
        self.assertTrue(True)
        state = {'on': True, 'bri': 255}
