 """
Venstar Colortouch thermostat.

William Groh william@miamiconsultant.com
"""
from homeassistant.components.thermostat import ThermostatDevice
from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT
import json,urllib.request,urllib.parse

CONF_IPADDRESS = 'ipaddress'


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the ColorTouch thermostat."""
    ip = str(config[CONF_IPADDRESS])
    print (ip)
    add_devices([
        ColorTouchThermostat("Venstar", ip, "COOL", 70, TEMP_FAHRENHEIT, False, 70, True),
    ])


# pylint: disable=too-many-arguments, abstract-method
class ColorTouchThermostat(ThermostatDevice):
    """Representation of a ColorTouch thermostat."""

    def __init__(self, name, ip, mode, target_temperature, unit_of_measurement,
                 away, current_temperature, is_fan_on):
        """Initialize the thermostat."""
        self._name = name
        self._ip = ip
        self._mode = mode
        self._target_temperature = target_temperature
        self._unit_of_measurement = unit_of_measurement
        self._away = away
        self._current_temperature = current_temperature
        self._is_fan_on = is_fan_on

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        url = 'http://192.168.187.149/query/info'
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._name = data['name']
        return self._name

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        url = 'http://192.168.187.149/query/info'
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._name = data['spacetemp']
        return self._current_temperature


    @property
    def mode(self):
        url = 'http://192.168.187.149/query/info'
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._name = data['mode']
        return self._mode

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        url = 'http://192.168.187.149/query/info'
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._name = data['cooltemp']
        return self._target_temperature

    @property
    def is_away_mode_on(self):
        """Return if away mode is on."""
        url = 'http://192.168.187.149/query/info'
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._name = data['away']
        return self._away

    @property
    def is_fan_on(self):
        """Return true if the fan is on."""
        url = 'http://192.168.187.149/query/info'
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._name = data['fanstate']
        return self._is_fan_on

    def set_temperature(self, temperature):
        """Set new target temperature."""
        self._target_temperature = temperature

    def turn_away_mode_on(self):
        """Turn away mode on."""
        self._away = True

    def turn_away_mode_off(self):
        """Turn away mode off."""
        self._away = False

    def turn_fan_on(self):
        """Turn fan on."""
        url = 'http://192.168.187.149/control'
        params = urllib.urlencode({
          'fan': 1
        })
        data = parse.urlencode(<your data dict>).encode()
        req =  request.Request(<your url>, data=data) # this will make the method "POST"
        resp = request.urlopen(req)


        self._is_fan_on = True

    def turn_fan_off(self):
        """Turn fan off."""
        self._is_fan_on = False
                                                                                                   
