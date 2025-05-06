from math import cos, sin
from typing import Any, Callable
import numpy
from scipy import linalg
from y_bus_square_matrix import YBusSquareMatrix


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
        s = complex(
            self.v * other.v * (y.real * coso + y.imag * sino),
            self.v * other.v * (y.real * sino - y.imag * coso),
        )
        return s


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


class PVBus(Bus):  #
    def __init__(
        self,
        name: str,
        v_esp: float = 1,
        generator: complex = complex(1),
        load: complex = complex(0),
    ):
        p = generator.real - load.real
        super().__init__(name=name, v=v_esp, o=0, p=p, q=0)
        self.v_esp = v_esp
        self.p_esp = p


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


class VariableIndex:
    def __init__(self, variable: str, power: str, busIndex: int):
        self.variable = variable
        self.power = power
        self.index = busIndex

    def __str__(self) -> str:
        return f"{self.variable}[{self.index + 1}]"


class PowerFlow:
    def __init__(self):
        self.buses: list[Bus] = list[Bus]()
        self.yMatrix: YBusSquareMatrix = YBusSquareMatrix()
        self.indexes = list[VariableIndex]()

    def add_bus(self, bus: Bus, y: complex | None = complex(0), z: complex | None = None) -> Bus:
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
        self.yMatrix.connect_bus_to_bus(self.__get_y_from_z_or_y(z, y), bus1Index, bus2Index)

    def __get_y_from_z_or_y(self, z: complex | None, y: complex | None) -> complex:
        if z is not None:
            return 1 / z
        if y is not None:
            return y
        raise ValueError("Either z or y must be provided")

    def solve(self):
        print("Solving power flow...")

        n: int = len(self.buses)
        x: list[float] = [[0] for _ in range(n)]
        j: list[list[float]] = [[0 for _ in range(n)] for _ in range(n)]
        s: list[float] = [[0] for _ in range(n)]

        for i in range(10):

            def getVariable(busIndex: int, variable: str, _) -> float:
                return self.buses[busIndex].v if variable == "o" else self.buses[busIndex].v

            def getPower(busIndex: int, _, power: str) -> float:
                bus = self.buses[busIndex]
                s: complex = sum(
                    [
                        bus.getPower(other, self.yMatrix.y_matrix[busIndex][c])
                        for c, other in enumerate(self.buses)
                    ]
                )
                return s.real if power == "p" else s.imag

            def getJacobianElement(
                rowIndex: int, columnIndex: int, variable: str, power: str
            ) -> float:
                bus = self.buses[rowIndex]
                other = self.buses[columnIndex]
                g: float = self.yMatrix.y_matrix[rowIndex][columnIndex].real
                b: float = self.yMatrix.y_matrix[rowIndex][columnIndex].imag
                coso: float = cos(bus.o - other.o)
                sino: float = sin(bus.o - other.o)

                if variable == "o" and power == "p":  # ∂p/∂o
                    return bus.v * other.v * (g * sino - b * coso)
                elif variable == "v" and power == "p":  # ∂p/∂v
                    return bus.v * (g * coso + b * sino)
                elif variable == "o" and power == "q":  # ∂q/∂o
                    return -bus.v * other.v * (g * sino + b * coso)
                elif variable == "v" and power == "q":  # ∂q/∂v
                    return bus.v * (g * sino - b * coso)
                else:
                    raise ValueError("Invalid variable or power")

            x = self.__map_indexes_list(getVariable)
            s = self.__map_indexes_list(getPower)
            j = self.__map_indexes_matrix(getJacobianElement)

            dX = numpy.dot(numpy.linalg.inv(j), s)

            print(f"X: {x}")
            print(f"S: {s}")
            print("J: ")
            for row in j:
                print("  [" + ", ".join(str(item) for item in row) + "]")

            print(f"dX: {dX}")

            # Update
            for variable in self.indexes:
                if variable.variable == "o":
                    o = self.buses[variable.index].o - dX[variable.index]
                    self.buses[variable.index].o = o
                    print(f"{variable}: {o}")

                elif variable.variable == "v":
                    v = self.buses[variable.index].v - dX[variable.index]
                    self.buses[variable.index].v = v
                    print(f"{variable}: {v}")
        # end for

    # end solve

    def print_state(self):
        for bus in self.buses:
            print(f"Bus: {bus.name}, V: {bus.v}, O: {bus.o}, P: {bus.p}, Q: {bus.q}")

    def transposeList(self, list: list[float]) -> list[list[float]]:
        return [[list[j]] for j in range(len(list))]

    def __update_indexes(self):
        o_indexes: list[VariableIndex] = list[VariableIndex]()
        v_indexes: list[VariableIndex] = list[VariableIndex]()

        for index, source in enumerate(self.buses):
            if isinstance(source, PQBus):
                o_indexes.append(VariableIndex(variable="o", power="p", busIndex=index))
                v_indexes.append(VariableIndex(variable="v", power="q", busIndex=index))
            if isinstance(source, PVBus):
                o_indexes.append(VariableIndex(variable="o", power="p", busIndex=index))

        self.indexes = o_indexes + v_indexes

    def print_indexes(self):
        x = self.__map_indexes_list(lambda index, variable, _: f"{variable}[{index+1}]")
        s = self.__map_indexes_list(lambda index, _, power: f"{power}[{index+1}]")
        j = self.__map_indexes_matrix(lambda row, column, v, p: f"∂{p}{row+1}/∂{v}{column+1}")
        for r, row in enumerate(j):
            print(
                f"|{x[r]}| {"=" if r == 0 else " "} "
                + "|"
                + ", ".join(str(item) for item in row)
                + "|"
                + f" {"*" if r == 0 else " "} |{s[r]}|"
            )

    def __map_indexes_matrix(
        self, x: Callable[[int, int, str, str], Any]  # row, column, variable, power]
    ) -> list[list[Any]]:
        return [
            [
                x(
                    row_index.index,
                    column_index.index,
                    column_index.variable,
                    row_index.power,
                )
                for _, column_index in enumerate(self.indexes)
            ]
            for _, row_index in enumerate(self.indexes)
        ]

    def __map_indexes_list(
        self, x: Callable[[int, str, str], Any]  # row, variable, power
    ) -> list[Any]:
        return [x(index.index, index.variable, index.power) for _, index in enumerate(self.indexes)]


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
    # v2 = 0.96674
    # o2 = -2.7596 graus
    # o3 = 2.347 graus
    # powerflow = PowerFlow()
    # bus1 = powerflow.add_bus(SlackBus("Slack bus", v_esp=1.02, o_esp=0))
    # bus2 = powerflow.add_bus(PQBus("Load", load=complex(2, 0.5)))
    # bus3 = powerflow.add_bus(
    #     PVBus("Generator", v_esp=1.03, generator=complex(1.5)),
    #     y=complex(0),
    # )

    # powerflow.connectBuses(bus1, bus2, y=complex(5, -15))
    # powerflow.connectBuses(bus1, bus3, y=complex(10, -40))
    # powerflow.connectBuses(bus2, bus3, y=complex(15, -50))

    # powerflow.print_indexes()
    # # return
    # powerflow.solve()


if __name__ == "__main__":
    main()
    # TODO make it work lol
