from maths.bus import Bus


class BusConnection:
    def __init__(
        self,
        tap_bus: int | Bus,
        z_bus: int | Bus,
        y: complex = complex(0.0),
        z: complex | None = None,
        bc: float = 0.0,
        tap: complex = complex(1.0),
    ):
        self.tap_bus: int = tap_bus.index if isinstance(tap_bus, Bus) else tap_bus
        self.z_bus: int = z_bus.index if isinstance(z_bus, Bus) else z_bus
        self.y = BusConnection.__get_z_or_y(z, y)
        self.bc = bc
        self.tap = tap

    @staticmethod
    def __get_z_or_y(z: complex | None, y: complex) -> complex:
        if z is not None:
            return 1 / z + y
        return y

    def __str__(self) -> str:
        return (
            f"C {self.tap_bus:3d} -> {self.z_bus:3d}, y={self.y}, bc = {self.bc} tap = {self.tap}"
        )
