import async_timeout
from datetime import timedelta
from typing import Any, Optional, Dict

from homeassistant.helpers.event import async_track_time_interval
from homeassistant.components.light import LightEntity

from .__init__ import _LOGGER, DOMAIN, SONOFF_LIGHT, SONOFF_MINI_DEVICE
from .__init__ import SonoffMiniDeviceApi

CUSTOM_INTEGRATION_PREFIX = "cusint"
SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    _LOGGER.warning("Sonoff platform loaded!")

    for light in hass.data[DOMAIN][SONOFF_MINI_DEVICE][SONOFF_LIGHT]:
        config = light["config"]
        api = light["api_factory"].get_api(config["scheme"], config["ip_address"], config["port"])
        default_friendly_name = SONOFF_MINI_DEVICE + "_" + config["ip_address"] + ":" + str(config["port"])
        entity = SonoffMiniSwitchLight(api, config.get("friendly_name", default_friendly_name))

        unsub_interval = async_track_time_interval(hass, entity.async_update, SCAN_INTERVAL)
        #TODO: usnsubscribe... When does it?
        # unsub_interval()
        # unsub_interval = None

        async_add_entities([entity])


class SonoffMiniSwitchLight(LightEntity):
    """
    State model:
     {
        "switch": "off",
        "startup": "off",
        "pulse": "off",
        "pulseWidth": 500,
        "ssid": "TP-LINK_014E",
        "otaUnlock": false,
        "fwVersion": "3.6.0",
        "deviceid": "1000b61314",
        "bssid": "84:16:f9:61:1:4e",
        "signalStrength": -62
    }
    """

    def __init__(self, api: SonoffMiniDeviceApi, friendly_name: str):
        self.friendly_name = friendly_name
        self.api = api
        self.switch_state = None
        self.entity_id = CUSTOM_INTEGRATION_PREFIX + "." + SONOFF_MINI_DEVICE + "." + self.api.device_id
        _LOGGER.warning("Entity #{}# registered".format(friendly_name))

    @property
    def unique_id(self):
        return self.entity_id

    @property
    def name(self):
        return self.friendly_name

    @property
    def enabled(self) -> bool:
        return self.switch_state is not None and (self.registry_entry is None or not self.registry_entry.disabled)

    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        return self.switch_state

    @property
    def is_on(self) -> bool:
        return self.switch_state is not None and self.switch_state["switch"] != "off"

    async def async_turn_off(self, **kwargs: Any) -> None:
        self.api.off()

    async def async_turn_on(self, **kwargs: Any) -> None:
        self.api.on()

    @property
    def should_poll(self) -> bool:
        return True

    async def async_update(self, *args):
        _LOGGER.warning("{},{},{},{}", args)
        self.switch_state = self.api.info()
