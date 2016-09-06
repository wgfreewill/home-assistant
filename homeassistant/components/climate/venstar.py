"""
Venstar Colortouch thermostat.

William Groh william@miamiconsultant.com

Usage in configuration.yaml

thermostat:
  platform: venstar
  ipaddress: YOUR.VENSTAR.IP.ADDR

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

    def __init__(self, name, ip, operation, target_temperature, unit_of_measurement,
                 away, current_temperature, is_fan_on):
        """Initialize the thermostat."""
        self._name = name
        self._ip = ip
        self._operation = operation
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
        url = 'http://%s/query/info' % self._ip
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
        url = 'http://%s/query/info' % self._ip
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._current_temperature = data['spacetemp']
        return self._current_temperature


    @property
    def operation(self):
        url = 'http://%s/query/info' % self._ip
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._mode = data['mode']
        return self._operation

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        url = 'http://%s/query/info' % self._ip
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._target_temperature = data['cooltemp']
        return self._target_temperature

    @property
    def is_away_mode_on(self):
        """Return if away mode is on."""
        url = 'http://%s/query/info' % self._ip
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._away = data['away']
        return self._away

    @property
    def is_fan_on(self):
        """Return true if the fan is on."""
        url = 'http://%s/query/info' % self._ip
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        self._is_fan_on = data['fanstate']
        return self._is_fan_on

    def set_temperature(self, temperature):
        """Set new target temperature."""
        heattemp = temperature - 3
        cooltemp = temperature
        url = 'http://%s/control' % self._ip
        params = {
          'cooltemp': cooltemp,
          'heattemp': heattemp
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)
        """output = resp.read()
        print(output)"""
        self._target_temperature = temperature

    def turn_away_mode_on(self):
        """Turn away mode on."""
        url = 'http://%s/control' % self._ip
        params = {
          'away': 1
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)
        output = resp.read()
        print(output)
        self._away = True

    def turn_away_mode_off(self):
        """Turn away mode off."""
        url = 'http://%s/control' % self._ip
        params = {
          'away': 0
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)
        output = resp.read()
        print(output)
        self._away = False

    def turn_fan_on(self):
        """Turn fan on."""
        url = 'http://%s/control' % self._ip
        params = {
          'fan': 1
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)
        output = resp.read()
        print(output)
        self._is_fan_on = True

    def turn_fan_off(self):
        """Turn fan off."""
        url = 'http://%s/control' % self._ip
        params = {
          'fan': 0
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data)
        resp = urllib.request.urlopen(req)
        output = resp.read()
        print(output)
        self._is_fan_on = False
