from typing import Union

from mhue.mhue.common import HueConnection


class Light:
    STATE_KEYS = ['on', 'bri', 'hue', 'sat', 'effect', 'xy', 'ct', 'alert']

    def __init__(self, light_data: dict, light_id: str):
        self.id = light_id
        self.data = {}
        self.name = None
        self._bri = None
        self._hue = None
        self._on = None
        self._sat = None

        self._set_up_light(light_data)

    def _set_up_light(self, light_data: dict) -> None:
        """
        Intended for the initial set up of a light.

        :param light_data: Dictionary containing values for the light

        """
        updated_light_state = {}
        for k, v in light_data.items():
            # Handle values in state that cannot be set
            if k == 'state':
                for key, val in v.items():
                    if key != 'colormode' and key != 'reachable':
                        updated_light_state[key] = val
                light_data[k] = updated_light_state
        self.data.update(light_data)
        self.name = self.data.get('name') if not None else self.name
        self.bri = self.data.get('state').get('bri')
        self.hue = self.data.get('state').get('hue')
        self.on = self.data.get('state').get('on')
        self.sat = self.data.get('state').get('sat')

    def update_light_state(self, light_state: dict) -> None:
        """
        This method exists to keep the light state data up to date as changes are made.

        :param light_state: Dictionary of state attributes

        """
        self.bri = light_state.get('bri') if light_state.get('bri') is not None else self.bri
        self.hue = light_state.get('hue') if light_state.get('hue') is not None else self.hue
        self.on = light_state.get('on') if light_state.get('on') is not None else self.on
        self.sat = light_state.get('sat') if light_state.get('sat') is not None else self.sat

    @staticmethod
    def valid_state(state: dict) -> bool:
        """
        Checks that each entry in the state dictionary is valid

        :param state: Dictionary of state data
        :return: True if the state dictionary is valid
        """
        for k, v in state.items():
            if k not in Light.STATE_KEYS:
                return False
            if (k == 'bri' or k == 'sat') and (not 0 <= v <= 255):
                return False
            elif k == 'hue' and not (0 <= v <= 65535):
                return False
            elif k == 'on' and not isinstance(v, bool):
                return False
            # Not sure what to check for regarding other fields

        return True

    @property
    def bri(self):
        return self._bri

    @bri.setter
    def bri(self, value: Union[dict, int]) -> None:
        if isinstance(value, dict):
            self._bri = max(min(255, value['state']['bri']), 0)
        else:
            self._bri = max(min(255, value), 0)
        self.data['state']['bri'] = self._bri

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, value: Union[dict, int]) -> None:
        if isinstance(value, dict):
            self._hue = max(min(65535, value['state']['hue']), 0)
        else:
            self._hue = max(min(255, value), 0)
        self.data['state']['hue'] = self._hue

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, value: Union[dict, bool]) -> None:
        if isinstance(value, dict):
            self._on = value['state']['on'] or False
        else:
            self._on = value or False
        self.data['state']['on'] = self._on

    @property
    def sat(self):
        return self._sat

    @sat.setter
    def sat(self, value: Union[dict, int]) -> None:
        if isinstance(value, dict):
            self._sat = max(min(255, value['state']['sat']), 0)
        else:
            self._sat = max(min(255, value), 0)
        self.data['state']['sat'] = self._sat

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplementedError(f'Unable to check equality between: {type(self)} and {type(other)}')
        return self.id == other.id and self.name == other.name


class Lights:
    REQUEST_TYPE = 'lights'

    def __init__(self, bridge: HueConnection):
        self.bridge = None
        self.lights = None

        self.reset(bridge)

    def reset(self, bridge) -> None:
        """
        Resets the Lights class by clearing the lights set and re-initializing it.

        """
        self.bridge = bridge
        self.lights = set({})
        self._setup_lights()

    def _setup_lights(self) -> None:
        """
        Sets up the lights.

        :return: list of Light objects
        """
        lights = self.bridge.get_request(Lights.REQUEST_TYPE)

        for light_id, values in lights.items():
            self.lights.add(Light(values, light_id))

    def set_light_state(self, settings: dict, light_list: list = None) -> None:
        """
        Uses the list of Light objects to set each Light to whatever settings are specified.

        :param settings: Dictionary of settings to be changed
        :param light_list: List of Light objects

        """
        if not Light.valid_state(settings):
            return
        state_success = []
        for light in light_list:
            light.update_light_state(settings)
            state_success.append(self.bridge.put_request(f'{Lights.REQUEST_TYPE}/{light.id}/state', settings))
