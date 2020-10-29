import logging
import requests
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'sonoff'
SONOFF_DEVICES = 'devices'
SONOFF_LIGHT = 'light'
SONOFF_MINI_DEVICE = 'sonoff_mini'


def sonoff_mini_devices_load_platform(hass, config, devices):
    mini_lights = list((({"api_factory": SonoffApiFactory(device_id, SONOFF_MINI_DEVICE), "config": device})
                        for device_id, device in devices.items() if device['platform'] == SONOFF_LIGHT))

    if len(mini_lights) > 0:
        hass.data[DOMAIN][SONOFF_MINI_DEVICE][SONOFF_LIGHT] = mini_lights
        discovery.load_platform(hass, SONOFF_LIGHT, DOMAIN, {}, config)


def setup(hass, config):
    devices = config.get(DOMAIN, {}).get(SONOFF_DEVICES, {})
    # _LOGGER.warning(devices)

    hass.data[DOMAIN] = {}

    hass.data[DOMAIN][SONOFF_MINI_DEVICE] = {}
    sonoff_mini_devices_load_platform(hass, config, devices.get(SONOFF_MINI_DEVICE))
    # _LOGGER.warning(hass.data[DOMAIN][SONOFF_MINI_DEVICE])

    # hass.data[DOMAIN][SONOFF_OTHER_DEVICE] = {}
    # sonoff_mini_devices_platform(hass, config, devices.get(SONOFF_OTHER_DEVICE))
    # _LOGGER.warning(hass.data[DOMAIN][SONOFF_OTHER_DEVICE])

    return True


class SonoffApiFactory:
    def __init__(self, device_id, device_type, control_type='diy'):
        self.device_id = device_id
        self.device_type = device_type
        self.controlType = control_type

    def get_api(self, device_scheme, device_host, device_port):
        if self.controlType == 'diy':
            if self.device_type == SONOFF_MINI_DEVICE:
                return SonoffMiniDeviceApi(self.device_id, device_scheme, device_host, device_port)
            # if self.device_type == SONOFF_OTHER_DEVICE :
            #     return SonoffOtherDeviceApi(self.device_id, device_scheme, device_host, device_port)
            # if self.device_type == SONOFF_OTHER_DEVICE :
            #     return SonoffOtherDeviceApi(self.device_id, device_scheme, device_host, device_port)
            return None
        else:
            return None


class SonoffMiniDeviceApi:
    def __init__(self, device_id, device_scheme, device_host, device_port):
        self.device_id = device_id
        self.device_host = device_host
        self.device_scheme = device_scheme
        self.device_port = device_port
        self.__switch_url_template = "http://{}:{}/zeroconf/switch"
        self.__info_url_template = "http://{}:{}/zeroconf/info"
        self.__on_command = "on"
        self.__off_command = "off"

    def info(self):
        url = self.__info_url_template.format(self.device_host, self.device_port)
        response = requests.post(url, json={"deviceid": self.device_id, "data": {}})
        state_model = response.json()
        response.close()

        if state_model["error"] == 0:
            return state_model['data']

        return None

    def on(self) -> bool:
        response_json = self.__switch_request(self.__on_command)
        if response_json["error"] == 0:
            return True
        return False

    def off(self) -> bool:
        response_json = self.__switch_request(self.__off_command)
        if response_json["error"] == 0:
            return True
        return False

    def __switch_request(self, command):
        url = self.__switch_url_template.format(self.device_host, self.device_port)
        response = requests.post(url, json={"deviceid": self.device_id, "data": {"switch": command}})
        response_json = response.json()
        response.close()
        return response_json
