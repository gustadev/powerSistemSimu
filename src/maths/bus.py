import cmath
from math import cos, sin
from y_bus_square_matrix import YBusSquareMatrix
from enum import Enum


class BusType(Enum):
    SLACK = 3
    PV = 2
    PQ = 0


class Bus:
    def __init__(
        self,
        name: str,
        v: float = 1,
        o: float = 0,
        load: complex = complex(0),
        generator: complex = complex(0),
        q_min: float | None = None,
        q_max: float | None = None,
        type: BusType = BusType.PQ,
        v_rated: float = 1,
        index: int = -1,  # to be used by power flow solver
    ):
        self.v_sch: float = v
        self.o_sch: float = o
        self.p_sch: float = (generator - load).real
        self.q_sch: float = (generator - load).imag

        self.name: str = name
        self.v: float = v
        self.o: float = o
        self.p: float = self.p_sch
        self.q: float = self.q_sch
        self.load: complex | None = load if load != complex(0) else None
        self.generator: complex | None = generator if generator != complex(0) else None
        self.q_min: float | None = q_min
        self.q_max: float | None = q_max
        self.index: int = index
        self.type: BusType = type
        self.v_rated: float = v_rated

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
            sum += self.v * self.v * Y.getBc(self.index, bus.index) / 2  # TODO is it really it?!
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
    @staticmethod
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

    @staticmethod
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
        return f"#{self.index:2d} | {self.name:12s} | V: {self.v:+4.3f}/_ {(self.o*180/cmath.pi):+5.2f}o | P: {self.p:+4.2f} | Q: {self.q:+4.2f}"
