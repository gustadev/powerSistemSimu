from cmath import pi, sqrt

from models.bus import Bus, BusType
from models.line import Line
from maths.power_flow import PowerFlow

degToRad: float = pi / 180


# Source: https://apnp.ifsul.edu.br/pluginfile.php/1698423/mod_resource/content/4/6%20Fluxo%20de%20Pot%C3%AAncia.pdf
def class_example():
    # 1pu = 100MW
    powerFlow = PowerFlow()
    bus1 = powerFlow.add_bus(Bus(name="Slack Bus", v=1.05, type=BusType.SLACK))
    bus2 = powerFlow.add_bus(Bus(name="Load", p_load=4, q_load=2.5, type=BusType.PQ))
    bus3 = powerFlow.add_bus(Bus(name="Generator", v=1.04, p_gen=2, type=BusType.PV))

    powerFlow.add_connection(Line.from_z(bus1, bus2, z=complex(0.02, 0.04)))
    powerFlow.add_connection(Line.from_z(bus2, bus3, z=complex(0.0125, 0.025)))
    powerFlow.add_connection(Line.from_z(bus3, bus1, z=complex(0.01, 0.03)))

    Y = powerFlow.build_bus_matrix()
    print(f"Y=\n{Y.y_matrix}\n")

    powerFlow.solve()


# Source: https://lmsspada.kemdiktisaintek.go.id/pluginfile.php/18101/mod_resource/content/2/Load-Flow%20dengan%20Gauss%20Seidel%20dan%20Newton%20Raphson.pdf
# Example 3, just compare the Y matrix. The final result for case 1 is done in gauss_seidel, not newton raphson. So it's complicated to compare.
def four_bus_example():
    powerFlow = PowerFlow()

    bus1 = powerFlow.add_bus(Bus(name="Slack Bus", v=1.04, type=BusType.SLACK))
    bus2 = powerFlow.add_bus(Bus(name="Load 1", p_gen=0.5, q_gen=-0.2, type=BusType.PQ))
    bus3 = powerFlow.add_bus(Bus(name="Load 2", p_load=1, q_load=-0.5, type=BusType.PQ))
    bus4 = powerFlow.add_bus(Bus(name="Load 3", p_load=0.3, q_load=0.1, type=BusType.PQ))

    powerFlow.add_connection(Line.from_z(bus1, bus2, z=complex(0.05, 0.15)))
    powerFlow.add_connection(Line.from_z(bus1, bus3, z=complex(0.10, 0.30)))
    powerFlow.add_connection(Line.from_z(bus2, bus3, z=complex(0.15, 0.45)))
    powerFlow.add_connection(Line.from_z(bus2, bus4, z=complex(0.10, 0.30)))
    powerFlow.add_connection(Line.from_z(bus3, bus4, z=complex(0.05, 0.15)))

    y_matrix = powerFlow.build_bus_matrix().y_matrix
    print(f"Y=\n{y_matrix}\n")

    ref_y: list[list[complex]] = [
        [3.0 - 9j, -2.0 + 6j, -1.0 + 3j, 0],
        [-2.0 + 6j, 3.666 - 11j, -0.666 + 2j, -1.0 + 3j],
        [-1.0 + 3j, -0.666 + 2j, 3.666 - 11j, -2.0 + 6j],
        [0, -1.0 + 3j, -2.0 + 6j, 3.0 - 9j],
    ]

    print("Differences for each element of the Y matrix:")
    for i in range(len(ref_y)):
        for j in range(len(ref_y[i])):
            diff = abs(ref_y[i][j] - y_matrix[i][j])
            print(f"Y[{i}][{j}] = {diff:.4f}")

    powerFlow.solve(max_iterations=10)


def tap_tranformer_example():
    pf = PowerFlow()
    bus1 = pf.add_bus(Bus(name="A"))
    bus2 = pf.add_bus(Bus(name="B"))
    bus3 = pf.add_bus(Bus(name="C"))
    bus4 = pf.add_bus(Bus(name="D"))

    def parallel(z1: complex, z2: complex) -> complex:
        return 1 / (1 / z1 + 1 / z2)

    pf.add_connection(Line.from_z(bus1, bus3, z=complex(0, 0.0125), tap=0.8))
    pf.add_connection(Line.from_z(bus4, bus2, z=complex(0, 0.16), tap=1.25))
    pf.add_connection(Line.from_z(bus4, bus3, z=parallel(complex(0, 0.25), complex(0, 0.2))))

    y_matrix = pf.build_bus_matrix().y_matrix
    print(y_matrix)

    ref_y: list[list[complex]] = [
        [-1j * 125, 0, 1j * 100, 0],
        [0, -1j * 6.25, 0, 1j * 5],
        [1j * 100, 0, -1j * 89, 1j * 9],
        [0, 1j * 5, 1j * 9, -1j * 13],
    ]

    print("Differences for each element of the Y matrix:")
    for i in range(len(ref_y)):
        for j in range(len(ref_y[i])):
            diff = abs(ref_y[i][j] - y_matrix[i][j])
            print(f"Y[{i}][{j}] = {diff:.4f}")


def main():
    class_example()
    four_bus_example()
    tap_tranformer_example()


if __name__ == "__main__":
    main()
    # TODO make it work lol
