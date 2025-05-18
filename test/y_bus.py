from maths.y_bus_square_matrix import YBusSquareMatrix


def main():
    y = YBusSquareMatrix(log_print=True)

    bus1 = y.add_bus(1 / 1.2j)  # De 1 para 0, z(pu) = j1.2

    bus2 = y.add_bus(0)  # De 2 para 0, z(pu) = 0

    bus3 = y.add_bus(1 / 1.5j)  # De 3 para 0, z(pu) = j1.5

    y.connect_bus_to_bus(1 / 0.2j, bus1, bus2)  # De 1 para 2, z(pu) = j0.2

    y.connect_bus_to_bus(1 / 0.3j, bus1, bus3)  # De 1 para 3, z(pu) = j0.3

    y.connect_bus_to_bus(1 / 0.15j, bus2, bus3)  # De 2 para 3, z(pu) = j0.15

    print(y.z_matrix)

    # Z = FINAL
    # 0.00+0.70j 0.00+0.66j 0.00+0.63j
    # 0.00+0.66j 0.00+0.75j 0.00+0.68j
    # 0.00+0.63j 0.00+0.68j 0.00+0.71j

    # Y =
    # 0.00-9.17j 0.00+5.00j -0.00+3.33j
    # 0.00+5.00j 0.00-11.67j -0.00+6.67j
    # 0.00+3.33j 0.00+6.67j 0.00-10.67j

    # TODO make it work


if __name__ == "__main__":
    main()
