from models.z_bus_square_matrix import ZBusSquareMatrix


def main():
    z = ZBusSquareMatrix(log_print=True)

    bus1 = z.add_bus_and_connect_to_ground(1.2j)  # De 1 para 0, z(pu) = j1.2

    bus2 = z.add_bus_and_connect_to_bus(0.2j, bus1)  # De 1 para 2, z(pu) = j0.2

    bus3 = z.add_bus_and_connect_to_bus(0.3j, bus1)  # De 1 para 3, z(pu) = j0.3

    z.connect_bus_to_ground(1.5j, bus3)  # De 3 para 0, z(pu) = j1.5

    z.connect_bus_to_bus(0.15j, bus2, bus3)  # De 2 para 3, z(pu) = j0.15

    print(f"Y = \n{z.y_matrix}")

    # Z = FINAL
    # 0.00+0.70j 0.00+0.66j 0.00+0.63j
    # 0.00+0.66j 0.00+0.75j 0.00+0.68j
    # 0.00+0.63j 0.00+0.68j 0.00+0.71j

    # Y =
    # 0.00-9.17j 0.00+5.00j -0.00+3.33j
    # 0.00+5.00j 0.00-11.67j -0.00+6.67j
    # 0.00+3.33j 0.00+6.67j 0.00-10.67j

    # z = ZBusMatrix(log_print=True)
    # bus1 = z.add_bus_and_connect_to_ground(100000000)
    # bus2 = z.add_bus_and_connect_to_bus(0.1 * j, bus1)
    # bus3 = z.add_bus_and_connect_to_bus(0.25 * j, bus1)
    # z.connect_bus_to_bus(0.2 * j, bus2, bus3)
    # print(z.ybus)


if __name__ == "__main__":
    main()
