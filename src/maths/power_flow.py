import cmath
from math import cos, sin
from typing import Any, Callable
import numpy
from y_bus_square_matrix import YBusSquareMatrix


class Bus:
    def __init__(
        self,
        name: str,
        v: float = 1,
        o: float = 0,
        p: float = 1,
        q: float = 0,
        index: int = -1,
    ):
        self.name = name
        self.v: float = v
        self.o: float = o
        self.p: float = p
        self.q: float = q
        self.index: int = index

    # P_i = ∑ |Vi| |Vj| |Yij| cos(θij - δi + δj)
    #       j
    def calcP(
        self,
        buses: list["Bus"],
        Y: YBusSquareMatrix,
    ) -> float:
        sum = 0
        for bus in buses:
            y = abs(Y.y_matrix[self.index][bus.index])
            theta = cmath.phase(Y.y_matrix[self.index][bus.index])
            sum += self.v * bus.v * y * cos(theta - self.o + bus.o)
        return sum

    # Q_i = - ∑ |Vi| |Vj| |Yij| sin(θij - δi + δj)
    #         j
    def calcQ(
        self,
        buses: list["Bus"],
        Y: YBusSquareMatrix,
    ) -> float:
        sum = 0
        for bus in buses:
            y = abs(Y.y_matrix[self.index][bus.index])
            theta = cmath.phase(Y.y_matrix[self.index][bus.index])
            sum += self.v * bus.v * y * sin(theta - self.o + bus.o)
            sum += self.v * self.v * Y.getBc(self.index, bus.index) / 2 # TODO is it really it?!
        return -sum

    @staticmethod
    def dPdO(  # dPi/dOj
        i: int,
        j: int,
        buses: list["Bus"],
        Y: YBusSquareMatrix,
    ) -> float:
        if i != j:
            bus_i = buses[i]
            bus_j = buses[j]
            y_ij = abs(Y.y_matrix[i][j])
            theta_ij = cmath.phase(Y.y_matrix[i][j])
            return -bus_i.v * bus_j.v * y_ij * sin(theta_ij - bus_i.o + bus_j.o)

        bus = buses[i]
        b = Y.y_matrix[i][i].imag
        return -bus.v * bus.v * b - bus.calcQ(buses, Y)

    @staticmethod
    def dPdV(  # dPi/dOj
        i: int,
        j: int,
        buses: list["Bus"],
        Y: YBusSquareMatrix,
    ) -> float:
        if i != j:
            bus_i = buses[i]
            bus_j = buses[j]
            y_ij = abs(Y.y_matrix[i][j])
            theta_ij = cmath.phase(Y.y_matrix[i][j])
            return bus_i.v * y_ij * cos(theta_ij - bus_i.o + bus_j.o)

        bus = buses[i]
        g = Y.y_matrix[i][i].real
        return bus.v * g + bus.calcP(buses, Y) / bus.v

    # precisa do y entre o derivado e o outro
    def dQdO(  # dPi/dOj
        i: int,
        j: int,
        buses: list["Bus"],
        Y: YBusSquareMatrix,
    ) -> float:
        if i != j:
            bus_i = buses[i]
            bus_j = buses[j]
            y_ij = abs(Y.y_matrix[i][j])
            theta_ij = cmath.phase(Y.y_matrix[i][j])
            return -bus_i.v * bus_j.v * y_ij * cos(theta_ij - bus_i.o + bus_j.o)

        bus = buses[i]
        g = Y.y_matrix[i][i].real
        return -bus.v * bus.v * g + bus.calcP(buses, Y)

    def dQdV(  # dPi/dOj
        i: int,
        j: int,
        buses: list["Bus"],
        Y: YBusSquareMatrix,
    ) -> float:
        if i != j:
            bus_i = buses[i]
            bus_j = buses[j]
            y_ij = abs(Y.y_matrix[i][j])
            theta_ij = cmath.phase(Y.y_matrix[i][j])
            return -bus_i.v * y_ij * sin(theta_ij - bus_i.o + bus_j.o)

        bus = buses[i]
        b = Y.y_matrix[i][i].imag
        return -bus.v * b + bus.calcQ(buses, Y) / bus.v

    def __str__(self) -> str:
        return f"#{self.index:2d} | {self.name:12s} | V: {self.v:+4.3f}∠ {(self.o*180/cmath.pi):+5.2f}° | P: {self.p:+4.2f} | Q: {self.q:+4.2f}"


class PQBus(Bus):
    def __init__(
        self,
        name: str,
        load: complex = complex(0),
        generator: complex = complex(0),
        v_ini: float = 1,
        o_ini: float = 0,
    ):
        p: float = generator.real - load.real
        q: float = generator.imag - load.imag
        super().__init__(name=name, v=v_ini, o=o_ini, p=p, q=q)
        self.p_sch = p
        self.q_sch = q
        self.v_ini = v_ini
        self.o_ini = o_ini


class PVBus(Bus):  #
    def __init__(
        self,
        name: str,
        v_sch: float = 1,
        o_ini: float = 0,
        generator: complex = complex(1),
        load: complex = complex(0),
    ):
        p = generator.real - load.real
        super().__init__(name=name, v=v_sch, o=o_ini, p=p, q=0)
        self.v_sch = v_sch
        self.p_sch = p
        self.o_ini = o_ini


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
    def __init__(self, base: float = 1):
        self.buses: list[Bus] = list[Bus]()
        self.yMatrix: YBusSquareMatrix = YBusSquareMatrix()
        self.indexes = list[VariableIndex]()
        self.taps = dict[str, float]()
        self.base = base

    def add_bus(self, bus: Bus, y: complex | None = complex(0), z: complex | None = None) -> Bus:
        self.buses.append(bus)
        self.yMatrix.add_bus(self.__get_y_from_z_or_y(z, y))
        self.__update_indexes()
        bus.index = len(self.buses) - 1
        return bus

    # tap on bus2
    def connectBuses(
        self,
        bus1: Bus,
        bus2: Bus,
        y: complex | None = complex(0.0),
        z: complex | None = None,
        bc: float = 0.0,
        tap: complex = complex(1.0),
    ) -> None:
        bus1Index = self.buses.index(bus1)
        bus2Index = self.buses.index(bus2)
        self.yMatrix.connect_bus_to_bus(
            self.__get_y_from_z_or_y(z, y),
            bus1Index,
            bus2Index,
            bc,
            tap,
        )

    # TODO include tap LT
    def __get_y_from_z_or_y(self, z: complex | None, y: complex) -> complex:
        if z is not None:
            return 1 / z + y
        return y

    def solve(self, max_iterations: int = 10, max_error: float = 100.0) -> None:
        print("Solving power flow...")

        n: int = len(self.buses)
        x: list[float] = [[0] for _ in range(n)]
        j: list[list[float]] = [[0 for _ in range(n)] for _ in range(n)]
        s: list[float] = [[0] for _ in range(n)]
        s_sch: list[float] = list[float]()
        for namedIndex in self.indexes:
            bus = self.buses[namedIndex.index]
            if namedIndex.variable == "o" and (isinstance(bus, PVBus) or isinstance(bus, PQBus)):
                s_sch.append(bus.p_sch)
            elif namedIndex.variable == "v" and (isinstance(bus, PVBus) or isinstance(bus, PQBus)):
                s_sch.append(bus.q_sch)

        for iteration in range(1, max_iterations + 1):
            print(f"\nIteration {iteration}:")

            def getPowerResidues(busIndex: int, variable: str, power: str) -> float:
                bus = self.buses[busIndex]
                if power == "p" and (isinstance(bus, PQBus) or isinstance(bus, PVBus)):
                    p_cal = bus.calcP(self.buses, self.yMatrix)
                    p_sch = bus.p_sch / self.base  # TODO where more to update?
                    return p_sch - p_cal
                elif power == "q" and (isinstance(bus, PQBus) or isinstance(bus, PVBus)):
                    q_cal = bus.calcQ(self.buses, self.yMatrix)
                    q_sch = bus.q_sch / self.base  # TODO where more to update?
                    return q_sch - q_cal
                return 0

            def getJacobianElement(r: int, c: int, __, ___, diff: str) -> float:
                dSdX = None
                if diff == "∂p/∂o":
                    dSdX = Bus.dPdO
                elif diff == "∂p/∂v":
                    dSdX = Bus.dPdV
                elif diff == "∂q/∂o":
                    dSdX = Bus.dQdO
                else:
                    dSdX = Bus.dQdV
                return dSdX(i=r, j=c, buses=self.buses, Y=self.yMatrix)

            ds = self.__map_indexes_list(getPowerResidues)
            j = self.__map_indexes_matrix(getJacobianElement)

            dX = numpy.dot(numpy.linalg.inv(j), ds)

            print("J: ")
            for row in j:
                print("  [" + ", ".join(f"{item:10.4f}" for item in row) + "]")

            print(f"dX: {dX}")

            for i, namedIndex in enumerate(self.indexes):
                busIndex = namedIndex.index
                bus = self.buses[busIndex]
                if namedIndex.variable == "o":
                    newO = bus.o + dX[i]
                    if newO > 2 * cmath.pi:
                        newO = newO % (2 * cmath.pi)
                    elif newO < -2 * cmath.pi:
                        newO = newO % (-2 * cmath.pi)
                    bus.o = newO
                    print(f"{namedIndex}: {bus.o:20.6f}rad / {(bus.o * 180 / cmath.pi):20.6f} deg")

                elif namedIndex.variable == "v":
                    bus.v = abs(bus.v + dX[i])
                    print(f"{namedIndex}: {bus.v:20.6f}pu")

            err = sum([abs(x) for x in dX])
            if err > max_error:
                print(f"|E| = {err}.  Diverged at {iteration}.")
                return

            if sum([abs(x) for x in dX]) < 1e-10:
                print(f"|E| = {err}.  Converged at {iteration}.")
                break
            else:
                print(f"|E| = {err}.  End.")

        print("\nPower flow solved.")
        for bus in self.buses:
            bus.p = bus.calcP(self.buses, self.yMatrix)
            bus.q = bus.calcQ(self.buses, self.yMatrix)
            print(bus)

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
