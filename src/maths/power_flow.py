import cmath
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

    # p = |V1||V2||Y| cos(theta12 - o1 + o2)
    def calcP(self, other: "Bus", y: complex) -> float:
        theta = cmath.phase(y)
        return self.v * other.v * abs(y) * cos(theta - self.o + other.o)

    # q = |V1||V2||Y| sin(theta12 - o1 + o2)
    def calcQ(self, other: "Bus", y: complex) -> float:
        theta = cmath.phase(y)
        return -self.v * other.v * abs(y) * sin(theta - self.o + other.o)  # TODO pq negativo?

    # Ref https://www.intechopen.com/chapters/65445
    # 66.8 −51.5 19.45
    # −51.5 93.52 -15.45
    # -20.55 15.45 63.2
    def dPdO(self, other: "Bus", y: complex, derivedOnBus: "Bus", y_o_d: complex) -> float:
        # serve para p2/o2 do exemplo (nos 2 termos)
        if self == derivedOnBus and other != derivedOnBus:
            return self.v * other.v * abs(y) * sin(cmath.phase(y) - self.o + other.o)

        # serve para p2/o3 (unico termo)
        if self != derivedOnBus and other == derivedOnBus:
            return -self.v * other.v * abs(y) * sin(cmath.phase(y) - self.o + other.o)

        return 0

    def dPdV(self, other: "Bus", y: complex, derivedOnBus: "Bus", y_o_d: complex) -> float:
        # p2/v2, termos 1 e 3 (cruzado)
        if self == derivedOnBus and other != derivedOnBus:
            return other.v * abs(y) * cos(cmath.phase(y) - self.o + other.o)

        # p2/v2, termo 2 (proprio)
        if self == derivedOnBus and other == derivedOnBus:
            return 2 * self.v * y.real

        # p3/v2, unico termo
        if other == derivedOnBus:
            return self.v * abs(y) * cos(cmath.phase(y) - self.o + other.o)

        return 0

    # precisa do y entre o derivado e o outro
    def dQdO(self, other: "Bus", y: complex, derivedOnBus: "Bus", y_o_d: complex) -> float:
        # q2/o2 (diz q3/o2) termos 1 e 3
        if self == derivedOnBus and self != other:
            return self.v * other.v * abs(y) * cos(cmath.phase(y) - self.o + other.o)

        # q2/o3 (diz q3/o3), unico termo
        if self != derivedOnBus and self == other:
            return (
                -self.v
                * derivedOnBus.v
                * abs(y_o_d)
                * cos(cmath.phase(y_o_d) - self.o + derivedOnBus.o)
            )

        return 0

    def dQdV(self, other: "Bus", y: complex, derivedOnBus: "Bus", y_o_d: complex) -> float:
        # q2/v2 (diz q3/v2), termos 1 e 3 (cruzado)
        if self == derivedOnBus and other != derivedOnBus:
            return -other.v * abs(y_o_d) * sin(cmath.phase(y_o_d) - derivedOnBus.o + other.o)

        if self == derivedOnBus and other == derivedOnBus:
            return -2 * other.v * abs(y) * sin(cmath.phase(y))

        # TODO what if self != derivedOnBus?

        return 0


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
        s_sch: list[float] = list[float]()
        for namedIndex in self.indexes:
            bus = self.buses[namedIndex.index]
            if namedIndex.variable == "o":
                s_sch.append(bus.p)
            else:
                s_sch.append(bus.q)

        for i in range(10):

            def getVariable(busIndex: int, variable: str, _) -> float:
                return self.buses[busIndex].v if variable == "o" else self.buses[busIndex].v

            def getPower(busIndex: int, _, power: str) -> float:
                bus = self.buses[busIndex]
                if power == "p":
                    return sum(
                        [
                            bus.calcP(other, self.yMatrix.y_matrix[busIndex][c])
                            for c, other in enumerate(self.buses)
                        ]
                    )
                return sum(
                    [
                        bus.calcQ(other, self.yMatrix.y_matrix[busIndex][c])
                        for c, other in enumerate(self.buses)
                    ]
                )

            def getJacobianElement(r: int, c: int, __, ___, diff: str) -> float:
                rowBus = self.buses[r]
                columnBus = self.buses[c]
                call = None
                if diff == "∂p/∂o":
                    call = rowBus.dPdO
                elif diff == "∂p/∂v":
                    call = rowBus.dPdV
                elif diff == "∂q/∂o":
                    call = rowBus.dQdO
                else:  # "∂q/∂v":
                    call = rowBus.dQdV
                return sum(
                    [
                        call(
                            other=other,
                            y=self.yMatrix.y_matrix[r][i],
                            derivedOnBus=columnBus,
                            y_o_d=self.yMatrix.y_matrix[c][i],
                        )
                        for (i, other) in enumerate(self.buses)
                    ]
                )

            x = self.__map_indexes_list(getVariable)
            s = self.__map_indexes_list(getPower)
            j = self.__map_indexes_matrix(getJacobianElement)

            ds = [a_i - b_i for a_i, b_i in zip(s_sch, s)]

            dX = numpy.dot(numpy.linalg.inv(j), ds)

            print(f"X: {x}")
            print(f"S: {s}")
            print(f"S_sch: {s_sch}")
            print(f"dS: {ds}")
            print("J: ")
            for row in j:
                print("  [" + ", ".join(str(item) for item in row) + "]")
            # return
            print(f"dX: {dX}")

            # Update
            for i, namedIndex in enumerate(self.indexes):
                busIndex = namedIndex.index
                bus = self.buses[busIndex]
                if namedIndex.variable == "o":
                    bus.o += dX[i]
                    print(f"{namedIndex}: {bus.o}rad / {bus.o * 180 / 3.14} deg")

                elif namedIndex.variable == "v":
                    bus.v += dX[i]
                    print(f"{namedIndex}: {bus.v}")

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
        j = self.__map_indexes_matrix(lambda row, column, v, p, _: f"∂{p}{row+1}/∂{v}{column+1}")
        for r, row in enumerate(j):
            print(
                f"|{x[r]}| {"=" if r == 0 else " "} "
                + "|"
                + ", ".join(str(item) for item in row)
                + "|"
                + f" {"*" if r == 0 else " "} |{s[r]}|"
            )

    def __map_indexes_matrix(
        self, x: Callable[[int, int, str, str, str], Any]  # row, column, variable, power, diff]
    ) -> list[list[Any]]:
        return [
            [
                x(
                    row_index.index,
                    column_index.index,
                    column_index.variable,
                    row_index.power,
                    f"∂{row_index.power}/∂{column_index.variable}",
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
    # powerFlow = PowerFlow()

    # bus1 = powerFlow.add_bus(SlackBus("Slack bus", v_esp=1, o_esp=0))
    # bus2 = powerFlow.add_bus(PQBus("Load", load=complex(0.9, 0.5)))
    # bus3 = powerFlow.add_bus(
    #     PVBus(
    #         "Generator",
    #         v_esp=1.01,
    #         generator=complex(1.3),
    #         load=complex(0.7, 0.4),
    #     ),
    #     y=complex(0),
    # )
    # powerFlow.print_indexes()

    # powerFlow.connectBuses(bus1, bus2, z=complex(0, 0.1))
    # powerFlow.connectBuses(bus1, bus3, z=complex(0, 0.25))
    # powerFlow.connectBuses(bus2, bus3, z=complex(0, 0.2))

    # powerFlow.solve()
    # v2 = 0.96674
    # o2 = -2.7596 graus
    # o3 = 2.347 graus
    powerflow = PowerFlow()
    bus1 = powerflow.add_bus(SlackBus("1 Slack bus", v_esp=1.02, o_esp=0))
    bus2 = powerflow.add_bus(PQBus("2 Load", load=complex(2, 0.5)))
    bus3 = powerflow.add_bus(PVBus("3 Generator", v_esp=1.03, generator=complex(1.5)))
    # bus4 = powerflow.add_bus(PQBus("Load2", load=complex(3)))
    # bus5 = powerflow.add_bus(PVBus("Generator2", v_esp=1.03, generator=complex(2)))

    powerflow.connectBuses(bus1, bus2, y=complex(5, -15))
    powerflow.connectBuses(bus1, bus3, y=complex(10, -40))
    powerflow.connectBuses(bus2, bus3, y=complex(15, -50))
    # powerflow.connectBuses(bus2, bus4, y=complex(10, -30))
    # powerflow.connectBuses(bus3, bus4, y=complex(5, -20))
    # powerflow.connectBuses(bus4, bus5, y=complex(10, -30))
    # powerflow.connectBuses(bus3, bus5, y=complex(10, -30))

    powerflow.print_indexes()
    # return
    powerflow.solve()


if __name__ == "__main__":
    main()
    # TODO make it work lol
