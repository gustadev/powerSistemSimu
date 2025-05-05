from math import cos, sin
from scipy import linalg
from y_bus_square_matrix import YBusSquareMatrix


j: complex = complex(0, 1)


class Bus:
    def __init__(
        self,
        name: str,
        v: float = 1,
        o: float = 0,
        p: float = 1,
        q: float = 0,
    ):
        self.name = name
        self.v: float = v
        self.o: float = o
        self.p: float = p
        self.q: float = q

    def getPower(self, other: "Bus", y: complex) -> complex:
        coso: float = cos(self.o - other.o)
        sino: float = sin(self.o - other.o)
        return complex(
            self.v * other.v * (y.real * coso + y.imag * sino),
            self.v * other.v * (y.real * sino - y.imag * coso),
        )


class PQBus(Bus):
    def __init__(
        self,
        name: str,
        load: complex = complex(1),
        generator: complex = complex(0),
    ):
        p: float = generator.real - load.real
        q: float = generator.imag - load.imag
        super().__init__(name=name, v=1, o=0, p=p, q=q)
        self.p_esp = p
        self.q_esp = q

    def update_values(self) -> None:
        pass


class PVBus(Bus):  #
    def __init__(
        self,
        name: str,
        v_esp: float = 1,
        generator: complex = complex(0),
        load: complex = complex(1),
    ):
        p = generator.real - load.real
        super().__init__(name=name, v=v_esp, o=0, p=p, q=0)
        self.v_esp = v_esp
        self.p_esp = p

    def update_values(self) -> None:
        pass


class SlackBus(Bus):  # knows delta
    def __init__(
        self,
        name: str,
        v_esp: float = 1,
        o_esp: float = 0,
    ):
        super().__init__(name=name, v=v_esp, o=o_esp, p=1, q=0)
        self.v_esp = v_esp
        self.o_esp = o_esp

    def update_values(self) -> None:
        pass


class NamedMatrixIndex:
    def __init__(self, name: str, row: int, column: int):
        self.name = name
        self.row = row
        self.column = column

    def __str__(self) -> str:
        return f"{self.name}[{self.row + 1},{self.column + 1}]"


class NamedListIndex:
    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index

    def __str__(self) -> str:
        return f"{self.name}[{self.index + 1}]"


class PowerFlow:
    def __init__(self):
        self.buses: list[Bus] = list[Bus]()
        self.yMatrix: YBusSquareMatrix = YBusSquareMatrix()
        self.variables = list[NamedMatrixIndex]()
        self.jacobian = list[list[NamedMatrixIndex]]()
        self.powers = list[NamedMatrixIndex]()

    def add_bus(
        self, bus: Bus, y: complex | None = complex(0), z: complex | None = None
    ) -> Bus:
        self.buses.append(bus)
        self.yMatrix.add_bus(self.__get_y_from_z_or_y(z, y))
        self.__update_indexes()
        return bus

    def connectBuses(
        self,
        bus1: Bus,
        bus2: Bus,
        y: complex | None = complex(0),
        z: complex | None = None,
    ) -> None:
        bus1Index = self.buses.index(bus1)
        bus2Index = self.buses.index(bus2)
        self.yMatrix.connect_bus_to_bus(
            self.__get_y_from_z_or_y(z, y), bus1Index, bus2Index
        )

    def __get_y_from_z_or_y(self, z: complex | None, y: complex | None) -> complex:
        if z is not None:
            return 1 / z
        if y is not None:
            return y
        raise ValueError("Either z or y must be provided")

    def solve(self):
        print("Solving power flow...")
        self.print_state()

        n: int = len(self.buses)
        x: list[float] = [[0] for _ in range(n)]
        j: list[list[float]] = [[0 for _ in range(n)] for _ in range(n)]
        s: list[float] = [[0] for _ in range(n)]

        for i in range(10):
            for row, variable in enumerate(self.variables):
                if variable.name == "o":
                    x[row] = self.buses[row].o
                elif variable.name == "v":
                    x[row] = self.buses[row].v

            for row in range(n):
                bus = self.buses[row]
                sSum = complex(0)
                for column, other in enumerate(self.buses):
                    sSum = sSum + bus.getPower(
                        other=other, y=self.yMatrix.y_matrix[row][column]
                    )

                if self.powers[row].name == "p":
                    s[row] = sSum.real
                elif self.powers[row].name == "q":
                    s[row] = sSum.imag

            for row in range(n):
                for column in range(n):
                    bus = self.buses[row]
                    other = self.buses[column]
                    g = self.yMatrix.y_matrix[row][column].real
                    b = self.yMatrix.y_matrix[row][column].imag
                    coso = cos(bus.o - other.o)
                    sino = sin(bus.o - other.o)

                    if self.jacobian[row][column].name == "∂p/∂o":
                        j[row][column] = bus.v * other.v * (g * sino - b * coso)
                    elif self.jacobian[row][column].name == "∂p/∂v":
                        j[row][column] = bus.v * (g * coso + b * sino)
                    elif self.jacobian[row][column].name == "∂q/∂o":
                        j[row][column] = -bus.v * other.v * (g * sino + b * coso)
                    elif self.jacobian[row][column].name == "∂q/∂v":
                        j[row][column] = bus.v * (g * sino - b * coso)

            x = linalg.inv(j) * self.transposeList(s)

            for variable in self.variables:
                if variable.name == "o":
                    self.buses[variable.index].o = (
                        self.buses[variable.index].o - x[variable.index][0]
                    )
                    print(
                        f"Updating {self.buses[variable.index].name} o: {self.buses[variable.index].o}"
                    )
                elif variable.name == "v":
                    self.buses[variable.index].v = (
                        self.buses[variable.index].v - x[variable.index][0]
                    )
                    print(
                        f"Updating {self.buses[variable.index].name} v: {self.buses[variable.index].v}"
                    )

    def print_state(self):
        for bus in self.buses:
            print(f"Bus: {bus.name}, V: {bus.v}, O: {bus.o}, P: {bus.p}, Q: {bus.q}")

    def transposeList(self, list: list[float]) -> list[list[float]]:
        return [[list[j]] for j in range(len(list))]

    def __update_indexes(self):
        o: list[NamedListIndex] = list[NamedListIndex]()
        v: list[NamedListIndex] = list[NamedListIndex]()
        p: list[NamedListIndex] = list[NamedListIndex]()
        q: list[NamedListIndex] = list[NamedListIndex]()

        for r, source in enumerate(self.buses):
            if isinstance(source, PQBus):
                o.append(NamedListIndex("o", r))
                v.append(NamedListIndex("v", r))
                p.append(NamedListIndex("p", r))
                q.append(NamedListIndex("q", r))
            if isinstance(source, PVBus):
                o.append(NamedListIndex("o", r))
                p.append(NamedListIndex("p", r))

        variables = o + v
        powers = p + q
        n = len(variables)
        jacobian = [["" for _ in range(n)] for _ in range(n)]

        for row, variable in enumerate(variables):
            for column, power in enumerate(powers):
                jacobian[row][column] = NamedMatrixIndex(
                    f"∂{power.name}/∂{variable.name}", variable.index, power.index
                )

        self.variables = variables
        self.powers = powers
        self.jacobian = jacobian

    def print_indexes(self):
        print("X:  [" + ", ".join(str(item) for item in self.variables) + "]")
        print(f"S: [" + ", ".join(str(item) for item in self.powers) + "]")
        print("J: ")
        for row in self.jacobian:
            print("  [" + ", ".join(str(item) for item in row) + "]")


def main():
    powerFlow = PowerFlow()

    bus1 = powerFlow.add_bus(SlackBus("Slack bus", v_esp=1, o_esp=0))
    bus2 = powerFlow.add_bus(PQBus("Load", load=complex(0.9, 0.5)))
    bus3 = powerFlow.add_bus(
        PVBus(
            "Generator",
            v_esp=1.01,
            generator=complex(1.3),
            load=complex(0.7, 0.4),
        ),
        y=complex(0),
    )
    powerFlow.print_indexes()

    powerFlow.connectBuses(bus1, bus2, z=complex(0, 0.1))
    powerFlow.connectBuses(bus1, bus3, z=complex(0, 0.25))
    powerFlow.connectBuses(bus2, bus3, z=complex(0, 0.2))

    powerFlow.solve()


if __name__ == "__main__":
    main()
    # TODO make it work lol
