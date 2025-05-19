import cmath
from math import cos, sin

from models.bus import Bus
from models.y_bus_square_matrix import YBusSquareMatrix


# P_i = ∑ |Vi| |Vj| |Yij| cos(θij - δi + δj)
#       j
def calcP(
    self: Bus,
    buses: list["Bus"],
    Y: YBusSquareMatrix,
) -> float:
    sum: float = 0.0
    for bus in buses:
        y = abs(Y.y_matrix[self.index][bus.index])
        theta = cmath.phase(Y.y_matrix[self.index][bus.index])
        sum += self.v * bus.v * y * cos(theta - self.o + bus.o)
    return sum


# Q_i = - ∑ |Vi| |Vj| |Yij| sin(θij - δi + δj)
#         j
def calcQ(
    self: Bus,
    buses: list["Bus"],
    Y: YBusSquareMatrix,
) -> float:
    sum: float = 0.0
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
    return -bus.v * bus.v * b - calcQ(bus, buses, Y)


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
    return bus.v * g + calcP(bus, buses, Y) / bus.v


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
    return -bus.v * bus.v * g + calcP(bus, buses, Y)


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
    return -bus.v * b + calcQ(bus, buses, Y) / bus.v
