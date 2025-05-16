from cmath import pi, sqrt
from bus import Bus, BusType
from connection import BusConnection
from power_flow import PowerFlow

degToRad: float = pi / 180


# Source: https://apnp.ifsul.edu.br/pluginfile.php/1698423/mod_resource/content/4/6%20Fluxo%20de%20Pot%C3%AAncia.pdf
def class_example():
    # 1pu = 100MW
    powerFlow = PowerFlow()
    bus1 = powerFlow.add_bus(Bus(name="Slack Bus", v=1.05, type=BusType.SLACK))
    bus2 = powerFlow.add_bus(Bus(name="Load", load=complex(4, 2.5), type=BusType.PQ))
    bus3 = powerFlow.add_bus(Bus(name="Generator", v=1.04, generator=complex(2), type=BusType.PV))

    powerFlow.add_connection(BusConnection(bus1, bus2, z=complex(0.02, 0.04)))
    powerFlow.add_connection(BusConnection(bus2, bus3, z=complex(0.0125, 0.025)))
    powerFlow.add_connection(BusConnection(bus3, bus1, z=complex(0.01, 0.03)))

    Y = powerFlow.build_bus_matrix()
    print(f"Y=\n{Y.y_matrix}\n")

    powerFlow.solve()


# https://apnp.ifsul.edu.br/pluginfile.php/1700773/mod_resource/content/1/Trab2-1_IEEE_14_nos.pdf
def example_14_buses():
    # fmt: off
    ## ANAREDE
    # final_v = [1.06, 1.045, 1.01, 1.019, 1.02, 1.07, 1.062, 1.09, 1.056, 1.051, 1.057, 1.055, 1.05, 1.036]
    # final_o = [0.0, -4.98, -12.72, -10.73, -8.78, -14.22, -13.37, -13.36, -14.94, -15.1, -14.79, -15.07, -15.16, -16.04]
    ## Codigo do matlab
    final_v = [1.06, 1.045, 1.01, 1.01767085369177, 1.01951385981906, 1.07, 1.06151953249094, 1.09, 1.05593172063697, 1.05098462499985, 1.05690651854037, 1.05518856319710, 1.05038171362860, 1.03552994585357]
    final_o = [0.0, -4.98258914197497, -12.7250999382679, -10.3129010923315, -8.77385389829527, -14.2209464637019, -13.3596273653462, -13.3596273653462, -14.9385212952289, -15.0972884630709, -14.7906220313214, -15.0755845204241, -15.1562763362218, -16.0336445292053]
    # fmt: on

    powerFlow = PowerFlow(base=100)  # 100MVA
    bus1 = powerFlow.add_bus(
        Bus(
            name="Slack Bus",
            v=1.06,
            type=BusType.SLACK,
        )
    )
    bus2 = powerFlow.add_bus(
        Bus(
            name="Generator",
            v=1.045,
            o=-4.98 * degToRad,
            generator=complex(40),
            load=complex(21.7, 12.7),
            type=BusType.PV,
        )
    )
    bus3 = powerFlow.add_bus(
        Bus(
            name="Generator",
            v=1.01,
            o=-12.72 * degToRad,
            generator=complex(0),
            load=complex(94.2, 19),
            type=BusType.PV,
        )
    )
    bus4 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.019,
            o=-10.73 * degToRad,
            load=complex(47.8, -3.9),
            type=BusType.PQ,
        ),
    )
    bus5 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.02,
            o=-8.78 * degToRad,
            load=complex(7.6, 1.6),
            type=BusType.PQ,
        ),
    )
    bus6 = powerFlow.add_bus(
        Bus(
            name="Generator",
            v=1.07,
            o=-14.22 * degToRad,
            generator=complex(0),
            load=complex(11.2, 7.5),
            type=BusType.PV,
        )
    )
    bus7 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.062,
            o=-13.37 * degToRad,
            load=complex(0),
            type=BusType.PQ,
        ),
    )
    bus8 = powerFlow.add_bus(
        Bus(
            name="Generator",
            v=1.09,
            o=-13.36 * degToRad,
            generator=complex(0),
            type=BusType.PV,
        ),
    )
    bus9 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.056,
            o=-14.94 * degToRad,
            load=complex(29.5, 16.6),
            type=BusType.PQ,
            shunt=complex(0, 0.19),
        ),
    )
    bus10 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.051,
            o=-15.10 * degToRad,
            load=complex(9, 5.8),
            type=BusType.PQ,
        ),
    )
    bus11 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.057,
            o=-14.79 * degToRad,
            load=complex(3.5, 1.8),
            type=BusType.PQ,
        ),
    )
    bus12 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.055,
            o=-15.07 * degToRad,
            load=complex(6.1, 1.6),
            type=BusType.PQ,
        ),
    )
    bus13 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.05,
            o=-15.16 * degToRad,
            load=complex(13.5, 5.8),
            type=BusType.PQ,
        ),
    )
    bus14 = powerFlow.add_bus(
        Bus(
            name="Load",
            v=1.036,
            o=-16.04 * degToRad,
            load=complex(14.9, 5),
            type=BusType.PQ,
        ),
    )

    powerFlow.add_connection(BusConnection(bus1, bus2, z=complex(0.01938, 0.05917), bc=0.0528))
    powerFlow.add_connection(BusConnection(bus1, bus5, z=complex(0.05403, 0.22304), bc=0.0492))
    powerFlow.add_connection(BusConnection(bus2, bus3, z=complex(0.04699, 0.19797), bc=0.0438))
    powerFlow.add_connection(BusConnection(bus2, bus4, z=complex(0.05811, 0.17632), bc=0.034))
    powerFlow.add_connection(BusConnection(bus2, bus5, z=complex(0.05695, 0.17388), bc=0.0346))
    powerFlow.add_connection(BusConnection(bus3, bus4, z=complex(0.06701, 0.17103), bc=0.0128))
    powerFlow.add_connection(BusConnection(bus4, bus5, z=complex(0.01335, 0.04211)))
    powerFlow.add_connection(BusConnection(bus4, bus7, z=complex(0, 0.20912), tap=0.978))
    powerFlow.add_connection(BusConnection(bus4, bus9, z=complex(0, 0.55618), tap=0.969))
    powerFlow.add_connection(BusConnection(bus5, bus6, z=complex(0, 0.25202), tap=0.932))
    powerFlow.add_connection(BusConnection(bus6, bus11, z=complex(0.09498, 0.1989)))
    powerFlow.add_connection(BusConnection(bus6, bus12, z=complex(0.12291, 0.25581)))
    powerFlow.add_connection(BusConnection(bus6, bus13, z=complex(0.06615, 0.13027)))
    powerFlow.add_connection(BusConnection(bus7, bus8, z=complex(0, 0.17615)))
    powerFlow.add_connection(BusConnection(bus7, bus9, z=complex(0, 0.11001)))
    powerFlow.add_connection(BusConnection(bus9, bus10, z=complex(0.03181, 0.0845)))
    powerFlow.add_connection(BusConnection(bus9, bus14, z=complex(0.12711, 0.27038)))
    powerFlow.add_connection(BusConnection(bus10, bus11, z=complex(0.08205, 0.19207)))
    powerFlow.add_connection(BusConnection(bus12, bus13, z=complex(0.22092, 0.19988)))
    powerFlow.add_connection(BusConnection(bus13, bus14, z=complex(0.17093, 0.34802)))

    powerFlow.solve(max_error=10000000, max_iterations=10)
    v_err = 0
    o_err = 0
    for i, bus in enumerate(powerFlow.buses):
        print(
            f"Bus {(i + 1):3d}: diff = {bus.v-final_v[i]:+8.4f}/_{(bus.o * 180 / pi-final_o[i]):+7.4f}o"
        )
        v_err += (bus.v - final_v[i]) ** 2
        o_err += (bus.o * 180 / pi - final_o[i]) ** 2
    print(f"Total error: {sqrt(v_err).real:+12.10f}/_{(sqrt(o_err)).real:+12.10f}o")


# Source: https://lmsspada.kemdiktisaintek.go.id/pluginfile.php/18101/mod_resource/content/2/Load-Flow%20dengan%20Gauss%20Seidel%20dan%20Newton%20Raphson.pdf
# Example 3, just compare the Y matrix. The final result for case 1 is done in gauss_seidel, not newton raphson. So it's complicated to compare.
def four_bus_example():
    powerFlow = PowerFlow()

    bus1 = powerFlow.add_bus(Bus(name="Slack Bus", v=1.04, type=BusType.SLACK))
    bus2 = powerFlow.add_bus(Bus(name="Load 1", generator=complex(0.5, -0.2), type=BusType.PQ))
    bus3 = powerFlow.add_bus(Bus(name="Load 2", generator=complex(-1, 0.5), type=BusType.PQ))
    bus4 = powerFlow.add_bus(Bus(name="Load 3", generator=complex(-0.3, -0.1), type=BusType.PQ))

    powerFlow.add_connection(BusConnection(bus1, bus2, z=complex(0.05, 0.15)))
    powerFlow.add_connection(BusConnection(bus1, bus3, z=complex(0.10, 0.30)))
    powerFlow.add_connection(BusConnection(bus2, bus3, z=complex(0.15, 0.45)))
    powerFlow.add_connection(BusConnection(bus2, bus4, z=complex(0.10, 0.30)))
    powerFlow.add_connection(BusConnection(bus3, bus4, z=complex(0.05, 0.15)))

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

    pf.add_connection(BusConnection(bus1, bus3, z=complex(0, 0.0125), tap=0.8))
    pf.add_connection(BusConnection(bus4, bus2, z=complex(0, 0.16), tap=1.25))
    pf.add_connection(BusConnection(bus4, bus3, z=parallel(complex(0, 0.25), complex(0, 0.2))))

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
    example_14_buses()
    four_bus_example()
    tap_tranformer_example()


if __name__ == "__main__":
    main()
    # TODO make it work lol
