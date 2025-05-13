from cmath import pi, sqrt
from power_flow import PQBus, PVBus, PowerFlow, SlackBus

degToRad: float = pi / 180


# Source: https://apnp.ifsul.edu.br/pluginfile.php/1698423/mod_resource/content/4/6%20Fluxo%20de%20Pot%C3%AAncia.pdf
def class_example():
    # 1pu = 100MW
    powerFlow = PowerFlow()
    bus1 = powerFlow.add_bus(SlackBus(name="Slack Bus", v_esp=1.05))
    bus2 = powerFlow.add_bus(PQBus(name="Load", load=complex(4, 2.5)))
    bus3 = powerFlow.add_bus(PVBus(name="Generator", v_sch=1.04, generator=complex(2)))

    powerFlow.connectBuses(bus1, bus2, z=complex(0.02, 0.04))
    powerFlow.connectBuses(bus2, bus3, z=complex(0.0125, 0.025))
    powerFlow.connectBuses(bus3, bus1, z=complex(0.01, 0.03))

    print(f"Y=\n{powerFlow.yMatrix}\n")

    powerFlow.solve()


# https://apnp.ifsul.edu.br/pluginfile.php/1700773/mod_resource/content/1/Trab2-1_IEEE_14_nos.pdf
def example_14_buses():
    #     1 Bus 1     HV  1  1  3 1.060    0.0      0.0      0.0    232.4   -16.9     0.0  1.060     0.0     0.0   0.0    0.0        0
    #    2 Bus 2     HV  1  1  2 1.045  -4.98     21.7     12.7     40.0    42.4     0.0  1.045    50.0   -40.0   0.0    0.0        0
    #    3 Bus 3     HV  1  1  2 1.010 -12.72     94.2     19.0      0.0    23.4     0.0  1.010    40.0     0.0   0.0    0.0        0
    #    4 Bus 4     HV  1  1  0 1.019 -10.33     47.8     -3.9      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #    5 Bus 5     HV  1  1  0 1.020  -8.78      7.6      1.6      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #    6 Bus 6     LV  1  1  2 1.070 -14.22     11.2      7.5      0.0    12.2     0.0  1.070    24.0    -6.0   0.0    0.0        0
    #    7 Bus 7     ZV  1  1  0 1.062 -13.37      0.0      0.0      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #    8 Bus 8     TV  1  1  2 1.090 -13.36      0.0      0.0      0.0    17.4     0.0  1.090    24.0    -6.0   0.0    0.0        0
    #    9 Bus 9     LV  1  1  0 1.056 -14.94     29.5     16.6      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.19       0
    #   10 Bus 10    LV  1  1  0 1.051 -15.10      9.0      5.8      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #   11 Bus 11    LV  1  1  0 1.057 -14.79      3.5      1.8      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #   12 Bus 12    LV  1  1  0 1.055 -15.07      6.1      1.6      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #   13 Bus 13    LV  1  1  0 1.050 -15.16     13.5      5.8      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    #   14 Bus 14    LV  1  1  0 1.036 -16.04     14.9      5.0      0.0     0.0     0.0  0.0       0.0     0.0   0.0    0.0        0
    # fmt: off
    final_v = [1.06, 1.045, 1.01, 1.019, 1.02, 1.07, 1.062, 1.09, 1.056, 1.051, 1.057, 1.055, 1.05, 1.036]
    final_o = [0.0, -4.98, -12.72, -10.73, -8.78, -14.22, -13.37, -13.36, -14.94, -15.1, -14.79, -15.07, -15.16, -16.04]
    # fmt: on

    powerFlow = PowerFlow(base=100)  # 100MVA
    bus1 = powerFlow.add_bus(SlackBus(name="Slack Bus", v_esp=1.06))
    bus2 = powerFlow.add_bus(
        PVBus(
            name="Generator",
            v_sch=1.045,
            o_ini=-4.98 * degToRad,
            generator=complex(40),
            load=complex(21.7, 12.7),
        )
    )
    bus3 = powerFlow.add_bus(
        PVBus(
            name="Generator",
            v_sch=1.01,
            o_ini=-12.72 * degToRad,
            generator=complex(0),
            load=complex(94.2, 19),
        )
    )
    bus4 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.019,
            o_ini=-10.73 * degToRad,
            load=complex(47.8, -3.9),
        ),
    )
    bus5 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.02,
            o_ini=-8.78 * degToRad,
            load=complex(7.6, 1.6),
        ),
    )
    bus6 = powerFlow.add_bus(
        PVBus(
            name="Generator",
            v_sch=1.07,
            o_ini=-14.22 * degToRad,
            generator=complex(0),
            load=complex(11.2, 7.5),
        )
    )
    bus7 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.062,
            o_ini=-13.37 * degToRad,
            load=complex(0),
        ),
    )
    bus8 = powerFlow.add_bus(
        PVBus(
            name="Generator",
            v_sch=1.09,
            o_ini=-13.36 * degToRad,
            generator=complex(0),
        ),
    )
    bus9 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.056,
            o_ini=-14.94 * degToRad,
            generator=complex(0, 19),  # shunt
            load=complex(29.5, 16.6),
        ),
    )
    bus10 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.051,
            o_ini=-15.10 * degToRad,
            load=complex(9, 5.8),
        ),
    )
    bus11 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.057,
            o_ini=-14.79 * degToRad,
            load=complex(3.5, 1.8),
        ),
    )
    bus12 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.055,
            o_ini=-15.07 * degToRad,
            load=complex(6.1, 1.6),
        ),
    )
    bus13 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.05,
            o_ini=-15.16 * degToRad,
            load=complex(13.5, 5.8),
        ),
    )
    bus14 = powerFlow.add_bus(
        PQBus(
            name="Load",
            v_ini=1.036,
            o_ini=-16.04 * degToRad,
            load=complex(14.9, 5),
        ),
    )

    powerFlow.connectBuses(bus1, bus2, z=complex(0.01938, 0.05917), bc=0.0528)
    powerFlow.connectBuses(bus1, bus5, z=complex(0.05403, 0.22304), bc=0.0492)
    powerFlow.connectBuses(bus2, bus3, z=complex(0.04699, 0.19797), bc=0.0438)
    powerFlow.connectBuses(bus2, bus4, z=complex(0.05811, 0.17632), bc=0.034)
    powerFlow.connectBuses(bus2, bus5, z=complex(0.05695, 0.17388), bc=0.0346)
    powerFlow.connectBuses(bus3, bus4, z=complex(0.06701, 0.17103), bc=0.0128)
    powerFlow.connectBuses(bus4, bus5, z=complex(0.01335, 0.04211))
    powerFlow.connectBuses(bus7, bus4, z=complex(0, 0.20912), tap=0.978)
    powerFlow.connectBuses(bus9, bus4, z=complex(0, 0.55618), tap=0.969)
    powerFlow.connectBuses(bus6, bus5, z=complex(0, 0.25202), tap=0.932)
    powerFlow.connectBuses(bus6, bus11, z=complex(0.09498, 0.1989))
    powerFlow.connectBuses(bus6, bus12, z=complex(0.12291, 0.25581))
    powerFlow.connectBuses(bus6, bus13, z=complex(0.06615, 0.13027))
    powerFlow.connectBuses(bus7, bus8, z=complex(0, 0.17615))
    powerFlow.connectBuses(bus7, bus9, z=complex(0, 0.11001))
    powerFlow.connectBuses(bus9, bus10, z=complex(0.03181, 0.0845))
    powerFlow.connectBuses(bus9, bus14, z=complex(0.12711, 0.27038))
    powerFlow.connectBuses(bus10, bus11, z=complex(0.08205, 0.19207))
    powerFlow.connectBuses(bus12, bus13, z=complex(0.22092, 0.19988))
    powerFlow.connectBuses(bus13, bus14, z=complex(0.17093, 0.34802))

    powerFlow.solve(max_error=10000000, max_iterations=10)
    v_err = 0
    o_err = 0
    for i, bus in enumerate(powerFlow.buses):
        print(
            f"Bus {(i + 1):3d}: diff = {bus.v-final_v[i]:+8.4f}∠{(bus.o * 180 / pi-final_o[i]):+7.4f}°"
        )
        v_err += (bus.v - final_v[i]) ** 2
        o_err += (bus.o * 180 / pi - final_o[i]) ** 2
    print(f"Total error: {sqrt(v_err + o_err).real:+8.4f}∠{(sqrt(o_err)).real:+7.4f}°")


# Source: https://lmsspada.kemdiktisaintek.go.id/pluginfile.php/18101/mod_resource/content/2/Load-Flow%20dengan%20Gauss%20Seidel%20dan%20Newton%20Raphson.pdf
# Example 3
def four_bus_example():
    powerFlow = PowerFlow()

    bus1 = powerFlow.add_bus(SlackBus(name="Slack Bus", v_esp=1.05))
    bus2 = powerFlow.add_bus(PVBus(name="Load 1", v_sch=1.04, generator=complex(0.5)))
    bus3 = powerFlow.add_bus(PQBus(name="Load 2", load=complex(1, -0.5)))
    bus4 = powerFlow.add_bus(PQBus(name="Load 3", load=complex(0.3, -0.1)))

    powerFlow.connectBuses(bus1, bus2, z=complex(0.05, 0.15))
    powerFlow.connectBuses(bus1, bus3, z=complex(0.10, 0.30))
    powerFlow.connectBuses(bus2, bus3, z=complex(0.15, 0.45))
    powerFlow.connectBuses(bus2, bus4, z=complex(0.10, 0.30))
    powerFlow.connectBuses(bus3, bus4, z=complex(0.05, 0.15))

    print(f"Y=\n{powerFlow.yMatrix}\n")

    powerFlow.solve(max_iterations=1000)


def tap_tranformer_example():
    pf = PowerFlow()
    bus1 = pf.add_bus(SlackBus(name="Any", v_esp=1.05))
    bus2 = pf.add_bus(PQBus(name="Any"))
    bus3 = pf.add_bus(PQBus(name="Any"))
    bus4 = pf.add_bus(PQBus(name="Any"))

    def parallel(z1, z2):
        return 1 / (1 / z1 + 1 / z2)

    pf.connectBuses(bus3, bus1, z=complex(0, 0.0125), tap=0.8)
    pf.connectBuses(bus2, bus4, z=complex(0, 0.16), tap=1.25)
    pf.connectBuses(bus3, bus4, z=parallel(complex(0, 0.25), complex(0, 0.2)))

    print(pf.yMatrix)

    # Y = |-j125       0  j100      0|
    #     |    0  -j6.25     0     j5|
    #     | j100       0  -j89     j9|
    #     |    0      j5    j9   -j13|


def eleven_buses_task():
    powerFlow = PowerFlow()
    bus1 = powerFlow.add_bus(PQBus.from_v_o(v_ini=1.20, o_ini=0), z=complex(0, 0.2))

    bus2 = powerFlow.add_bus(PQBus(name="Load1"))
    bus3 = powerFlow.add_bus(PQBus(name="Load2"))
    bus4 = powerFlow.add_bus(PQBus(name="Load3"))
    bus5 = powerFlow.add_bus(PQBus(name="Load4", load=complex(0, -5)))
    bus6 = powerFlow.add_bus(PQBus(name="Load5"))
    bus7 = powerFlow.add_bus(PQBus(name="Load6"))
    bus8 = powerFlow.add_bus(PQBus(name="Load7"))
    bus9 = powerFlow.add_bus(PQBus(name="Load8"))

    bus10 = powerFlow.add_bus(PQBus.from_v_o(v_ini=1.10, o_ini=-26 * degToRad), z=complex(0, 0.15))
    bus11 = powerFlow.add_bus(PQBus.from_v_o(v_ini=1.05, o_ini=-degToRad), z=complex(0, 0.25))

    powerFlow.connectBuses(bus1, bus2, z=complex(0, 0.06))
    powerFlow.connectBuses(bus2, bus3, z=complex(0, 0.30))
    powerFlow.connectBuses(bus2, bus5, z=complex(0, 0.15))
    powerFlow.connectBuses(bus2, bus6, z=complex(0, 0.45))
    powerFlow.connectBuses(bus3, bus4, z=complex(0, 0.40))
    powerFlow.connectBuses(bus3, bus6, z=complex(0, 0.40))
    powerFlow.connectBuses(bus4, bus6, z=complex(0, 0.60))
    powerFlow.connectBuses(bus4, bus9, z=complex(0, 0.70))
    powerFlow.connectBuses(bus4, bus10, z=complex(0, 0.08))
    powerFlow.connectBuses(bus5, bus7, z=complex(0, 0.43))
    powerFlow.connectBuses(bus6, bus8, z=complex(0, 0.48))
    powerFlow.connectBuses(bus7, bus8, z=complex(0, 0.35))
    powerFlow.connectBuses(bus7, bus11, z=complex(0, 0.10))
    powerFlow.connectBuses(bus8, bus9, z=complex(0, 0.48))

    powerFlow.solve(max_iterations=1000, max_error=100000000)
    # print(powerFlow.yMatrix)


def main():
    # class_example()
    example_14_buses()
    # four_bus_example()
    # tap_tranformer_example()
    # eleven_buses_task()


if __name__ == "__main__":
    main()
    # TODO make it work lol
