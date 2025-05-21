import cmath
from typing import Any, Callable
import numpy

from maths.power_calculator import calcP, calcQ, dPdO, dPdV, dQdO, dQdV
from models.connection import BusConnection
from models.bus import Bus, BusType
from models.y_bus_square_matrix import YBusSquareMatrix


class VariableIndex:
    def __init__(self, variable: str, power: str, busIndex: int, busId: str):
        self.variable = variable
        self.power = power
        self.index = busIndex
        self.busId = busId

    def __str__(self) -> str:
        return f"{self.variable}[{self.index + 1}]"


class PowerFlow:
    def __init__(self, base: float = 1):
        self.buses = dict[str, Bus]()
        self.connections = dict[str, BusConnection]()
        self.__yMatrix: YBusSquareMatrix = YBusSquareMatrix()
        self.indexes = list[VariableIndex]()
        self.base = base

    def add_bus(self, bus: Bus) -> Bus:
        self.buses[bus.id] = bus
        bus.index = len(self.buses) - 1
        return bus

    def add_connection(self, connection: BusConnection) -> None:
        self.connections[connection.id] = connection

    def build_bus_matrix(self) -> YBusSquareMatrix:
        bus_matrix: YBusSquareMatrix = YBusSquareMatrix()

        for index, bus in enumerate(self.buses.values()):
            bus_matrix.add_bus(complex(bus.g_shunt, bus.b_shunt))
            bus.index = index

        for connection in self.connections.values():
            bus_matrix.connect_bus_to_bus(
                y=connection.y,
                source=self.buses[connection.tap_bus_id].index,
                target=self.buses[connection.z_bus_id].index,
                bc=connection.bc,
                tap=connection.tap,
            )
        return bus_matrix

    def solve(self, max_iterations: int = 10, max_error: float = 100.0) -> None:
        print("Solving power flow...")
        self.__yMatrix = self.build_bus_matrix()
        self.__update_indexes()

        n: int = len(self.buses)
        j: list[list[float]] = [[0 for _ in range(n)] for _ in range(n)]
        s_sch: list[float] = list[float]()
        for namedIndex in self.indexes:
            bus = self.buses[namedIndex.busId]
            if namedIndex.variable == "o" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                s_sch.append(bus.p_sch)
            elif namedIndex.variable == "v" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                s_sch.append(bus.q_sch)

        for iteration in range(1, max_iterations + 1):
            print(f"\nIteration {iteration}:")

            def getPowerResidues(bus_id: str, variable: str, power: str) -> float:
                bus = self.buses[bus_id]
                if power == "p" and (
                    bus.type.value == BusType.PV.value or bus.type.value == BusType.PQ.value
                ):
                    p_cal = calcP(bus, self.buses, self.__yMatrix)
                    p_sch = bus.p_sch / self.base  # TODO where more to update?
                    return p_sch - p_cal
                elif power == "q" and (bus.type == BusType.PV or bus.type == BusType.PQ):
                    q_cal = calcQ(bus, self.buses, self.__yMatrix)
                    q_sch = bus.q_sch / self.base  # TODO where more to update?
                    return q_sch - q_cal
                return 0

            def getJacobianElement(r_id: str, c_id: str, _: str, __: str, diff: str) -> float:
                dSdX: Callable[[str, str, dict[str, Bus], YBusSquareMatrix], float] = dPdO
                if diff == "∂p/∂o":
                    dSdX = dPdO
                elif diff == "∂p/∂v":
                    dSdX = dPdV
                elif diff == "∂q/∂o":
                    dSdX = dQdO
                else:
                    dSdX = dQdV
                return dSdX(i_id=r_id, j_id=c_id, buses=self.buses, Y=self.__yMatrix)

            ds = self.__map_indexes_list(getPowerResidues)
            j = self.__map_indexes_matrix(getJacobianElement)

            dX = numpy.dot(numpy.linalg.inv(j), ds)

            print("J: ")
            for row in j:
                print("  [" + ", ".join(f"{item:10.4f}" for item in row) + "]")

            print(f"dX: {dX}")

            for i, namedIndex in enumerate(self.indexes):
                bus_id = namedIndex.busId
                bus = self.buses[bus_id]
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
        for bus in self.buses.values():
            bus.p = calcP(bus, self.buses, self.__yMatrix)
            bus.q = calcQ(bus, self.buses, self.__yMatrix)
            print(bus)

    def print_state(self):
        for bus in self.buses.values():
            print(f"Bus: {bus.name}, V: {bus.v}, O: {bus.o}, P: {bus.p}, Q: {bus.q}")

    def transposeList(self, list: list[float]) -> list[list[float]]:
        return [[list[j]] for j in range(len(list))]

    def __update_indexes(self):
        o_indexes: list[VariableIndex] = list[VariableIndex]()
        v_indexes: list[VariableIndex] = list[VariableIndex]()

        for source in self.buses.values():
            if source.type is BusType.PQ:
                o_indexes.append(
                    VariableIndex(variable="o", power="p", busIndex=source.index, busId=source.id)
                )
                v_indexes.append(
                    VariableIndex(variable="v", power="q", busIndex=source.index, busId=source.id)
                )
            if source.type is BusType.PV:
                o_indexes.append(
                    VariableIndex(variable="o", power="p", busIndex=source.index, busId=source.id)
                )

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
        self, x: Callable[[str, str, str, str, str], Any]  # row, column, variable, power, diff]
    ) -> list[list[Any]]:
        return [
            [
                x(
                    row_index.busId,
                    column_index.busId,
                    column_index.variable,
                    row_index.power,
                    f"∂{row_index.power}/∂{column_index.variable}",
                )
                for _, column_index in enumerate(self.indexes)
            ]
            for _, row_index in enumerate(self.indexes)
        ]

    def __map_indexes_list(
        self, x: Callable[[str, str, str], Any]  # row, variable, power
    ) -> list[Any]:
        return [x(index.busId, index.variable, index.power) for _, index in enumerate(self.indexes)]
