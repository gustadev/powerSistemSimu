from y_bus_square_matrix import YBusSquareMatrix
from z_bus_square_matrix import ZBusSquareMatrix
import numpy as np


def main():
    z_1 = complex(0, 1.2)  # De 1 para 0, z(pu) = j1.2
    z_3 = complex(0, 1.5)  # De 3 para 0, z(pu) = j1.5

    z_1_2 = complex(0, 0.2)  # De 1 para 2, z(pu) = j0.2
    z_1_3 = complex(0, 0.3)  # De 1 para 3, z(pu) = j0.3
    z_2_3 = complex(0, 0.15)  # De 2 para 3, z(pu) = j0.15

    z = ZBusSquareMatrix(log_print=False)

    bus1 = z.add_bus_and_connect_to_ground(z_1)  # De 1 para 0, z(pu) = j1.2

    bus2 = z.add_bus_and_connect_to_bus(z_1_2, bus1)  # De 1 para 2, z(pu) = j0.2

    bus3 = z.add_bus_and_connect_to_bus(z_1_3, bus1)  # De 1 para 3, z(pu) = j0.3

    z.connect_bus_to_ground(z_3, bus3)  # De 3 para 0, z(pu) = j1.5

    z.connect_bus_to_bus(z_2_3, bus2, bus3)  # De 2 para 3, z(pu) = j0.15

    y = YBusSquareMatrix(log_print=False)

    bus1 = y.add_bus(1 / z_1)  # De 1 para 0, z(pu) = j1.2

    bus2 = y.add_bus(0)  # De 2 para 0, z(pu) = 0

    bus3 = y.add_bus(1 / z_3)  # De 3 para 0, z(pu) = j1.5

    y.connect_bus_to_bus(1 / z_1_2, bus1, bus2)  # De 1 para 2, z(pu) = j0.2

    y.connect_bus_to_bus(1 / z_1_3, bus1, bus3)  # De 1 para 3, z(pu) = j0.3

    y.connect_bus_to_bus(1 / z_2_3, bus2, bus3)  # De 2 para 3, z(pu) = j0.15

    print(f"Z from z = \n{z.z_matrix}")
    print(f"Z from y = \n{y.z_matrix}")
    diff = z.z_matrix - y.z_matrix
    avg_sq_error = np.mean(np.abs(diff) ** 2)
    print(f"Average Squared Error between Z matrices = {avg_sq_error}")

    print(f"Y from z = \n{z.y_matrix}")
    print(f"Y from y = \n{y.y_matrix}")
    print(f"Y difference = \n{z.y_matrix - y.y_matrix}")
    diff = z.y_matrix - y.y_matrix
    avg_sq_error = np.mean(np.abs(diff) ** 2)
    print(f"Average Squared Error between Y matrices = {avg_sq_error}")


if __name__ == "__main__":
    main()
