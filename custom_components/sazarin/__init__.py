from homeassistant.helpers import discovery

DOMAIN = 'sazarin'
SAZARIN_DEVICES = 'devices'
SIMPLE_RGB_DEVICE = 'simple_rgb_light'


async def async_setup(hass, config):
    devices = config.get(DOMAIN, {}).get(SAZARIN_DEVICES, {})

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][SIMPLE_RGB_DEVICE] = {}

    simple_rgb_light_devices = devices.get(SIMPLE_RGB_DEVICE, {}).items()
    _LOGGER.warning(simple_rgb_light_devices)

    simple_rgb_lights = list((({"config": device})
                              for device_ip, device in simple_rgb_light_devices))

    if len(simple_rgb_lights) > 0:
        hass.data[DOMAIN][SIMPLE_RGB_DEVICE][SONOFF_LIGHT] = mini_lights
        discovery.async_load_platform(hass, SONOFF_LIGHT, DOMAIN, {}, config)

    return True
