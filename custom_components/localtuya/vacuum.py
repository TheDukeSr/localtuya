"""Platform to locally control Tuya-based vacuum devices."""
import logging
from functools import partial

import voluptuous as vol

from homeassistant.components.vacuum import (
    VacuumEntity,
    DOMAIN,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_RETURNING,
    STATE_ERROR,
)
from homeassistant.const import (
    STATE_IDLE,
    STATE_PAUSED,
)

from .const import (
    CONF_BATTERY_DP,
)
from .common import LocalTuyaEntity, async_setup_entry

_LOGGER = logging.getLogger(__name__)


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(CONF_BATTERY_DP): vol.In(dps),
    }


class LocaltuyaVacuum(LocalTuyaEntity, VacuumEntity):
    """Tuya vacuum device."""

    def __init__(
        self,
        device,
        config_entry,
        switchid,
        **kwargs,
    ):
        """Initialize a new LocaltuyaVacuum."""
        super().__init__(device, config_entry, switchid, **kwargs)
        self._state = None
        self._battery_level = None
        print("Initialized vacuum [{}]".format(self.name))

    @property
    def state(self):
        """Return the vacuum state."""
        return STATE_IDLE

    @property
    def battery_level(self):
        """Return the current battery level."""
        return self._battery_level

    @property
    def cleaning_mode(self):
        """Return the current cleaning mode."""
        return None

    @property
    def cleaning_mode_list(self):
        """Return the list of available fan speeds and cleaning modes."""
        return NotImplementedError()

    async def async_turn_on():
        """Turn the vacuum on and start cleaning."""
        return None

    async def async_turn_off():
        """Turn the vacuum off stopping the cleaning and returning home."""
        return None

    async def async_return_to_base():
        """Set the vacuum cleaner to return to the dock."""
        return None

    async def async_stop():
        """Stop the vacuum cleaner, do not return to base."""
        return None

    async def async_clean_spot():
        """Perform a spot clean-up."""
        return None

    async def async_locate():
        """Locate the vacuum cleaner."""
        return None

    async def async_set_cleaning_mode():
        """Set the cleaning mode."""
        return None

    async def async_send_command():
        """Send a command to a vacuum cleaner."""
        return None

    def status_updated(self):
        """Device status was updated."""
        self._state = self.dps(self._dps_id)

        if self.has_config(CONF_BATTERY_DP):
            self._battery_level = self.dps_conf(CONF_BATTERY_DP)


async_setup_entry = partial(async_setup_entry, DOMAIN, LocaltuyaVacuum, flow_schema)
