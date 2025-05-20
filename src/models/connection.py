from models.bus import Bus
from models.network_element import NetworkElement


class BusConnection(NetworkElement):
    def __init__(
        self,
        tap_bus_id: str | Bus,
        z_bus_id: str | Bus,
        y: complex = complex(0.0),
        z: complex | None = None,
        bc: float = 0.0,
        tap: complex = complex(1.0),
        name: str | None = None,
        id: str | None = None,
    ):
        self.tap_bus_id: str = BusConnection.__unrwap_bus_id(tap_bus_id)
        self.z_bus_id: str = BusConnection.__unrwap_bus_id(z_bus_id)
        self.y = BusConnection.__get_z_or_y(z, y)
        self.bc = bc
        self.tap = tap

        if name:
            self.name: str = name
        else:
            self.name: str = f"Line"

        super().__init__(name=self.name, id=id, type="C")

    @staticmethod
    def __get_z_or_y(z: complex | None, y: complex) -> complex:
        if z is not None:
            return 1 / z + y
        return y

    def __str__(self) -> str:
        return f"C {self.tap_bus_id:3d} -> {self.z_bus_id:3d}, y={self.y}, bc = {self.bc} tap = {self.tap}"

    @staticmethod
    def __unrwap_bus_id(bus_id: str | Bus) -> str:
        if isinstance(bus_id, Bus):
            return bus_id.id
        return bus_id

    def copyWith(
        self,
        y: complex | None = None,
        bc: float | None = None,
        tap: complex | None = None,
        name: str | None = None,
    ) -> "BusConnection":
        return BusConnection(
            tap_bus_id=self.tap_bus_id,
            z_bus_id=self.z_bus_id,
            y=y if y is not None else self.y,
            bc=bc if bc is not None else self.bc,
            tap=tap if tap is not None else self.tap,
            name=name if name is not None else self.name,
            id=self.id,
        )
