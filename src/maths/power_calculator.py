import cmath
from math import cos, sin

from models.bus import Bus
from models.y_bus_square_matrix import YBusSquareMatrix


# P_i = ∑ |Vi| |Vj| |Yij| cos(θij - δi + δj)
#       j
def calcP(
    self: Bus,
    buses: dict[str, "Bus"],
    Y: YBusSquareMatrix,
) -> float:
    sum: float = 0.0
    for bus in buses.values():
        y = abs(Y.y_matrix[self.index][bus.index])
        theta = cmath.phase(Y.y_matrix[self.index][bus.index])
        sum += self.v * bus.v * y * cos(theta - self.o + bus.o)
    return sum


# Q_i = - ∑ |Vi| |Vj| |Yij| sin(θij - δi + δj)
#         j
def calcQ(
    self: Bus,
    buses: dict[str, "Bus"],
    Y: YBusSquareMatrix,
) -> float:
    sum: float = 0.0
    for bus in buses.values():
        y = abs(Y.y_matrix[self.index][bus.index])
        theta = cmath.phase(Y.y_matrix[self.index][bus.index])
        sum += self.v * bus.v * y * sin(theta - self.o + bus.o)
        sum += self.v * self.v * Y.getBc(self.index, bus.index) / 2  # TODO is it really it?!
    return -sum


@staticmethod
def dPdO(  # dPi/dOj
    i_id: str,
    j_id: str,
    buses: dict[str, "Bus"],
    Y: YBusSquareMatrix,
) -> float:
    if i_id != j_id:
        bus_i = buses[i_id]
        bus_j = buses[j_id]
        y_ij = abs(Y.y_matrix[bus_i.index][bus_j.index])
        theta_ij = cmath.phase(Y.y_matrix[bus_i.index][bus_j.index])
        return -bus_i.v * bus_j.v * y_ij * sin(theta_ij - bus_i.o + bus_j.o)

    bus = buses[i_id]
    b = Y.y_matrix[bus.index][bus.index].imag
    return -bus.v * bus.v * b - calcQ(bus, buses, Y)


def dPdV(  # dPi/dOj
    i_id: str,
    j_id: str,
    buses: dict[str, "Bus"],
    Y: YBusSquareMatrix,
) -> float:
    if i_id != j_id:
        bus_i = buses[i_id]
        bus_j = buses[j_id]
        y_ij = abs(Y.y_matrix[bus_i.index][bus_j.index])
        theta_ij = cmath.phase(Y.y_matrix[bus_i.index][bus_j.index])
        return bus_i.v * y_ij * cos(theta_ij - bus_i.o + bus_j.o)

    bus = buses[i_id]
    g = Y.y_matrix[bus.index][bus.index].real
    return bus.v * g + calcP(bus, buses, Y) / bus.v


def dQdO(  # dPi/dOj
    i_id: str,
    j_id: str,
    buses: dict[str, "Bus"],
    Y: YBusSquareMatrix,
) -> float:
    if i_id != j_id:
        bus_i = buses[i_id]
        bus_j = buses[j_id]
        y_ij = abs(Y.y_matrix[bus_i.index][bus_j.index])
        theta_ij = cmath.phase(Y.y_matrix[bus_i.index][bus_j.index])
        return -bus_i.v * bus_j.v * y_ij * cos(theta_ij - bus_i.o + bus_j.o)

    bus = buses[i_id]
    g = Y.y_matrix[bus.index][bus.index].real
    return -bus.v * bus.v * g + calcP(bus, buses, Y)


def dQdV(  # dPi/dOj
    i_id: str,
    j_id: str,
    buses: dict[str, "Bus"],
    Y: YBusSquareMatrix,
) -> float:
    if i_id != j_id:
        bus_i = buses[i_id]
        bus_j = buses[j_id]
        y_ij = abs(Y.y_matrix[bus_i.index][bus_j.index])
        theta_ij = cmath.phase(Y.y_matrix[bus_i.index][bus_j.index])
        return -bus_i.v * y_ij * sin(theta_ij - bus_i.o + bus_j.o)

    bus = buses[i_id]
    b = Y.y_matrix[bus.index][bus.index].imag
    return -bus.v * b + calcQ(bus, buses, Y) / bus.v
