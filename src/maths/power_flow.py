import cmath
from typing import Any, Callable
import numpy
from bus import Bus, BusType
from y_bus_square_matrix import YBusSquareMatrix


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

    def add_bus(self, bus: Bus, y: complex = complex(0), z: complex | None = None) -> Bus:
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
        y: complex = complex(0.0),
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
        j: list[list[float]] = [[0 for _ in range(n)] for _ in range(n)]
        s_sch: list[float] = list[float]()
        for namedIndex in self.indexes:
            bus = self.buses[namedIndex.index]
            if namedIndex.variable == "o" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                s_sch.append(bus.p_sch)
            elif namedIndex.variable == "v" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                s_sch.append(bus.q_sch)

        for iteration in range(1, max_iterations + 1):
            print(f"\nIteration {iteration}:")

            def getPowerResidues(busIndex: int, variable: str, power: str) -> float:
                bus = self.buses[busIndex]
                if power == "p" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                    p_cal = bus.calcP(self.buses, self.yMatrix)
                    p_sch = bus.p_sch / self.base  # TODO where more to update?
                    return p_sch - p_cal
                elif power == "q" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                    q_cal = bus.calcQ(self.buses, self.yMatrix)
                    q_sch = bus.q_sch / self.base  # TODO where more to update?
                    return q_sch - q_cal
                return 0

            def getJacobianElement(r: int, c: int, _: str, __: str, diff: str) -> float:
                dSdX: Callable[[int, int, list[Bus], YBusSquareMatrix], float] = Bus.dPdO
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
            if source.type is BusType.PQ:
                o_indexes.append(VariableIndex(variable="o", power="p", busIndex=index))
                v_indexes.append(VariableIndex(variable="v", power="q", busIndex=index))
            if source.type is BusType.PV:
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
