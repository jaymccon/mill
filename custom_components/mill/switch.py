"""Sensor platform for mill."""
from __future__ import annotations

from homeassistant.components.sensor import SwitchEntity, SwitchEntityDescription, SwitchDeviceClass

from .const import DOMAIN
from .coordinator import MillDataUpdateCoordinator
from .entity import MillEntity

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="dgoCycle",
        name="Cycle",
        icon="mdi:dots-horizontal-circle",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        MillSwitch(
            coordinator=coordinator,
            entity_description=entity_description,
            device=device
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for device in coordinator.data
    )


class MillSwitch(MillEntity, SwitchEntity):
    """mill Switch class."""

    def __init__(
        self,
        coordinator: MillDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
        device,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator,entity_description,device)
        self.entity_description = entity_description
        self.device = device


    async def async_turn_off(self, **kwargs):
        """Turn the mill off."""
        if not self.is_on:
            return
        client = self.coordinator.client
        client.async_set_cycle(self.device, "Idle")

    async def async_turn_on(self, **kwargs):
        """Turn the mill on."""
        if self.is_on:
            return
        client = self.coordinator.client
        client.async_set_cycle(self.device, "DryGrind")

    @property
    def is_on(self) -> bool:
        """Return true if the mill is on."""
        desc = self.entity_description
        value = self.coordinator.data[self.device].get(desc.key)
        if isinstance(value, dict):
            value = value.get('reported')
        if value == 'Idle':
            return False
        return True  
