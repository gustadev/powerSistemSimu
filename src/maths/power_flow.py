j: complex = complex(0, 1)

class Connection:
    def __init__(self, source: "Bus", target: "Bus", z: complex):
        self.source = source
        self.target = target
        self.z = z
        self.r = z.real
        self.x = z.imag
        self.y = 1 / z
        self.g = self.y.real
        self.b = self.y.imag


class Bus:
    def __init__(self, name: str, v: float, o: float, p: float, q: float):
        self.name = name
        self.v = v
        self.o = o
        self.p = p
        self.q = q
        self.connections: list[Connection] = list[Connection]()

    def connect(self, bus: "Bus", z: complex) -> None:
        self.connections.append(Connection(source=self, target=bus, z=z))
        bus.connections.append(Connection(source=bus, target=self, z=z))

    def update_values(self) -> None:
        pass


class LoadBus(Bus):
    def __init__(
        self,
        name: str,
        p_esp: float,
        q_esp: float,
    ):
        super().__init__(name=name, v=1, o=0, p=p_esp, q=q_esp)
        self.p_esp = p_esp
        self.q_esp = q_esp

    def update_values(self) -> None:
        pass


class VoltageControllerBus(Bus):
    def __init__(
        self,
        name: str,
        v_esp: float,
        p_esp: float,
    ):
        super().__init__(name=name, v=v_esp, o=0, p=p_esp, q=0)
        self.v_esp = v_esp
        self.p_esp = p_esp

    def update_values(self) -> None:
        pass


class SlackBus(Bus):
    def __init__(
        self,
        name: str,
        v_esp: float,
        o_esp: float,
    ):
        super().__init__(name=name, v=v_esp, o=o_esp, p=1, q=0)
        self.v_esp = v_esp
        self.o_esp = o_esp

    def update_values(self) -> None:
        pass


class PowerFlow:
    def __init__(self):
        self.buses: list[Bus] = list[Bus]()

    def add_bus(self, bus: Bus) -> Bus:
        self.buses.append(bus)
        return bus

    def solve(self):
        print("Solving power flow...")
        self.print_state()

        for iteration in range(10):
            print(f"Iteration {iteration+1}")
            for bus in self.buses:
                bus.update_values()
            self.print_state()

    def print_state(self):
        for bus in self.buses:
            print(f"Bus: {bus.name}, V: {bus.v}, O: {bus.o}, P: {bus.p}, Q: {bus.q}")


def main():
    powerFlow = PowerFlow()

    bus3 = powerFlow.add_bus(SlackBus("Slack bus", v=1.05, o=0.0))
    bus1 = powerFlow.add_bus(LoadBus("Load", 1.0, 0.5))
    bus2 = powerFlow.add_bus(VoltageControllerBus("Generator", 1.0, 1.0))

    bus1.connect(bus2)
    bus2.connect(bus3)

    powerFlow.solve()


if __name__ == "__main__":
    main()
    # TODO make it work lol
    