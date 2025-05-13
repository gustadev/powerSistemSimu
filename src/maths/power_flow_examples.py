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
    powerFlow.connectBuses(bus4, bus7, z=complex(0, 0.20912), tap=0.978)
    powerFlow.connectBuses(bus4, bus9, z=complex(0, 0.55618), tap=0.969)
    powerFlow.connectBuses(bus5, bus6, z=complex(0, 0.25202), tap=0.932)
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
    print(f"Total error: {sqrt(v_err).real:+8.4f}∠{(sqrt(o_err)).real:+7.4f}°")


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


def example_30_buses():
    #      08/20/93 UW ARCHIVE           100.0  1961 W IEEE 30 Bus Test Case
    # BUS DATA FOLLOWS                            30 ITEMS
    #    1 Glen Lyn 132  1  1  3 1.060    0.0      0.0      0.0    260.2   -16.1   132.0  1.060     0.0     0.0   0.0    0.0        0
    #    2 Claytor  132  1  1  2 1.043  -5.48     21.7     12.7     40.0    50.0   132.0  1.045    50.0   -40.0   0.0    0.0        0
    #    3 Kumis    132  1  1  0 1.021  -7.96      2.4      1.2      0.0     0.0   132.0  0.0       0.0     0.0   0.0    0.0        0
    #    4 Hancock  132  1  1  0 1.012  -9.62      7.6      1.6      0.0     0.0   132.0  0.0       0.0     0.0   0.0    0.0        0
    #    5 Fieldale 132  1  1  2 1.010 -14.37     94.2     19.0      0.0    37.0   132.0  1.010    40.0   -40.0   0.0    0.0        0
    #    6 Roanoke  132  1  1  0 1.010 -11.34      0.0      0.0      0.0     0.0   132.0  0.0       0.0     0.0   0.0    0.0        0
    #    7 Blaine   132  1  1  0 1.002 -13.12     22.8     10.9      0.0     0.0   132.0  0.0       0.0     0.0   0.0    0.0        0
    #    8 Reusens  132  1  1  2 1.010 -12.10     30.0     30.0      0.0    37.3   132.0  1.010    40.0   -10.0   0.0    0.0        0
    #    9 Roanoke  1.0  1  1  0 1.051 -14.38      0.0      0.0      0.0     0.0     1.0  0.0       0.0     0.0   0.0    0.0        0
    #   10 Roanoke   33  1  1  0 1.045 -15.97      5.8      2.0      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.19       0
    #   11 Roanoke   11  1  1  2 1.082 -14.39      0.0      0.0      0.0    16.2    11.0  1.082    24.0    -6.0   0.0    0.0        0
    #   12 Hancock   33  1  1  0 1.057 -15.24     11.2      7.5      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   13 Hancock   11  1  1  2 1.071 -15.24      0.0      0.0      0.0    10.6    11.0  1.071    24.0    -6.0   0.0    0.0        0
    #   14 Bus 14    33  1  1  0 1.042 -16.13      6.2      1.6      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   15 Bus 15    33  1  1  0 1.038 -16.22      8.2      2.5      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   16 Bus 16    33  1  1  0 1.045 -15.83      3.5      1.8      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   17 Bus 17    33  1  1  0 1.040 -16.14      9.0      5.8      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   18 Bus 18    33  1  1  0 1.028 -16.82      3.2      0.9      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   19 Bus 19    33  1  1  0 1.026 -17.00      9.5      3.4      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   20 Bus 20    33  1  1  0 1.030 -16.80      2.2      0.7      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   21 Bus 21    33  1  1  0 1.033 -16.42     17.5     11.2      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   22 Bus 22    33  1  1  0 1.033 -16.41      0.0      0.0      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   23 Bus 23    33  1  1  0 1.027 -16.61      3.2      1.6      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   24 Bus 24    33  1  1  0 1.021 -16.78      8.7      6.7      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.043      0
    #   25 Bus 25    33  1  1  0 1.017 -16.35      0.0      0.0      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   26 Bus 26    33  1  1  0 1.000 -16.77      3.5      2.3      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   27 Cloverdle 33  1  1  0 1.023 -15.82      0.0      0.0      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   28 Cloverdle132  1  1  0 1.007 -11.97      0.0      0.0      0.0     0.0   132.0  0.0       0.0     0.0   0.0    0.0        0
    #   29 Bus 29    33  1  1  0 1.003 -17.06      2.4      0.9      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    #   30 Bus 30    33  1  1  0 0.992 -17.94     10.6      1.9      0.0     0.0    33.0  0.0       0.0     0.0   0.0    0.0        0
    # -999
    # BRANCH DATA FOLLOWS                         41 ITEMS
    #    1    2  1  1 1 0  0.0192    0.0575      0.0528     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    1    3  1  1 1 0  0.0452    0.1652      0.0408     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    2    4  1  1 1 0  0.0570    0.1737      0.0368     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    3    4  1  1 1 0  0.0132    0.0379      0.0084     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    2    5  1  1 1 0  0.0472    0.1983      0.0418     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    2    6  1  1 1 0  0.0581    0.1763      0.0374     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    4    6  1  1 1 0  0.0119    0.0414      0.0090     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    5    7  1  1 1 0  0.0460    0.1160      0.0204     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    6    7  1  1 1 0  0.0267    0.0820      0.0170     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    6    8  1  1 1 0  0.0120    0.0420      0.0090     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    6    9  1  1 1 0  0.0       0.2080      0.0        0     0     0    0 0  0.978     0.0 0.0    0.0     0.0    0.0   0.0
    #    6   10  1  1 1 0  0.0       0.5560      0.0        0     0     0    0 0  0.969     0.0 0.0    0.0     0.0    0.0   0.0
    #    9   11  1  1 1 0  0.0       0.2080      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    9   10  1  1 1 0  0.0       0.1100      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    4   12  1  1 1 0  0.0       0.2560      0.0        0     0     0    0 0  0.932     0.0 0.0    0.0     0.0    0.0   0.0
    #   12   13  1  1 1 0  0.0       0.1400      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   12   14  1  1 1 0  0.1231    0.2559      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   12   15  1  1 1 0  0.0662    0.1304      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   12   16  1  1 1 0  0.0945    0.1987      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   14   15  1  1 1 0  0.2210    0.1997      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   16   17  1  1 1 0  0.0524    0.1923      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   15   18  1  1 1 0  0.1073    0.2185      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   18   19  1  1 1 0  0.0639    0.1292      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   19   20  1  1 1 0  0.0340    0.0680      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   10   20  1  1 1 0  0.0936    0.2090      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   10   17  1  1 1 0  0.0324    0.0845      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   10   21  1  1 1 0  0.0348    0.0749      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   10   22  1  1 1 0  0.0727    0.1499      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   21   22  1  1 1 0  0.0116    0.0236      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   15   23  1  1 1 0  0.1000    0.2020      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   22   24  1  1 1 0  0.1150    0.1790      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   23   24  1  1 1 0  0.1320    0.2700      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   24   25  1  1 1 0  0.1885    0.3292      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   25   26  1  1 1 0  0.2544    0.3800      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   25   27  1  1 1 0  0.1093    0.2087      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   28   27  1  1 1 0  0.0       0.3960      0.0        0     0     0    0 0  0.968     0.0 0.0    0.0     0.0    0.0   0.0
    #   27   29  1  1 1 0  0.2198    0.4153      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   27   30  1  1 1 0  0.3202    0.6027      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #   29   30  1  1 1 0  0.2399    0.4533      0.0        0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    8   28  1  1 1 0  0.0636    0.2000      0.0428     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    #    6   28  1  1 1 0  0.0169    0.0599      0.0130     0     0     0    0 0  0.0       0.0 0.0    0.0     0.0    0.0   0.0
    powerFlow = PowerFlow()

    bus1 = powerFlow.add_bus(SlackBus(name="Glen Lyn 132", v_esp=1.06, o_esp=0))
    bus2 = powerFlow.add_bus(
        PVBus(
            name="Claytor 132",
            v_sch=1.043,
            o_ini=-5.48 * degToRad,
            load=complex(21.7, 12.7),
            generator=complex(40, 49.56),
        )
    )
    bus3 = powerFlow.add_bus(
        PQBus(
            name="Kumis 132",
            v_ini=1.021,
            o_ini=-7.96 * degToRad,
            load=complex(2.4, 1.2),
        )
    )
    bus4 = powerFlow.add_bus(
        PQBus(
            name="Hancock 132",
            v_ini=1.012,
            o_ini=-9.62 * degToRad,
            load=complex(7.6, 1.6),
        )
    )
    bus5 = powerFlow.add_bus(
        PQBus(
            name="Fieldale 132",
            v_ini=1.01,
            o_ini=-14.37 * degToRad,
            load=complex(94.2, 19),
        )
    )
    bus6 = powerFlow.add_bus(
        PQBus(
            name="Roanoke 132",
            v_ini=1.01,
            o_ini=-11.34 * degToRad,
            load=complex(0, 0),
        )
    )
    bus7 = powerFlow.add_bus(
        PQBus(
            name="Blaine 132",
            v_ini=1.002,
            o_ini=-13.12 * degToRad,
            load=complex(22.8, 10.9),
        )
    )
    bus8 = powerFlow.add_bus(
        PVBus(
            name="Reusens 132",
            v_sch=1.01,
            o_ini=-12.1 * degToRad,
            load=complex(30, 30),
            generator=complex(37.3, 0),
        )
    )
    bus9 = powerFlow.add_bus(
        PQBus(
            name="Roanoke 1.0",
            v_ini=1.051,
            o_ini=-14.38 * degToRad,
            load=complex(0, 0),
        )
    )
    bus10 = powerFlow.add_bus(
        PQBus(
            name="Roanoke 33",
            v_ini=1.045,
            o_ini=-15.97 * degToRad,
            load=complex(5.8, 2),
            generator=complex(0, 19),
        )
    )
    bus11 = powerFlow.add_bus(
        PVBus(
            name="Roanoke 11",
            v_sch=1.082,
            o_ini=-14.39 * degToRad,
            load=complex(0, 0),
            generator=complex(24, -6),
        )
    )
    bus12 = powerFlow.add_bus(
        PQBus(
            name="Hancock 33",
            v_ini=1.057,
            o_ini=-15.24 * degToRad,
            load=complex(11.2, 7.5),
        )
    )
    bus13 = powerFlow.add_bus(
        PVBus(
            name="Hancock 11",
            v_sch=1.071,
            o_ini=-15.24 * degToRad,
            load=complex(0, 0),
            generator=complex(24, -6),
        )
    )
    bus14 = powerFlow.add_bus(
        PQBus(
            name="Bus 14 33",
            v_ini=1.042,
            o_ini=-16.13 * degToRad,
            load=complex(6.2, 1.6),
        )
    )
    bus15 = powerFlow.add_bus(
        PQBus(
            name="Bus 15 33",
            v_ini=1.038,
            o_ini=-16.22 * degToRad,
            load=complex(8.2, 2.5),
        )
    )
    bus16 = powerFlow.add_bus(
        PQBus(
            name="Bus 16 33",
            v_ini=1.045,
            o_ini=-15.83 * degToRad,
            load=complex(3.5, 1.8),
        )
    )
    bus17 = powerFlow.add_bus(
        PQBus(
            name="Bus 17 33",
            v_ini=1.04,
            o_ini=-16.14 * degToRad,
            load=complex(9, 5.8),
        )
    )
    bus18 = powerFlow.add_bus(
        PQBus(
            name="Bus 18 33",
            v_ini=1.028,
            o_ini=-16.82 * degToRad,
            load=complex(3.2, 0.9),
        )
    )
    bus19 = powerFlow.add_bus(
        PQBus(
            name="Bus 19 33",
            v_ini=1.026,
            o_ini=-17.0 * degToRad,
            load=complex(9.5, 3.4),
        )
    )
    bus20 = powerFlow.add_bus(
        PQBus(
            name="Bus 20 33",
            v_ini=1.03,
            o_ini=-16.8 * degToRad,
            load=complex(2.2, 0.7),
        )
    )
    bus21 = powerFlow.add_bus(
        PQBus(
            name="Bus 21 33",
            v_ini=1.033,
            o_ini=-16.42 * degToRad,
            load=complex(17.5, 11.2),
        )
    )
    bus22 = powerFlow.add_bus(
        PQBus(
            name="Bus 22 33",
            v_ini=1.033,
            o_ini=-16.41 * degToRad,
            load=complex(0, 0),
        )
    )
    bus23 = powerFlow.add_bus(
        PQBus(
            name="Bus 23 33",
            v_ini=1.027,
            o_ini=-16.61 * degToRad,
            load=complex(3.2, 1.6),
        )
    )
    bus24 = powerFlow.add_bus(
        PQBus(
            name="Bus 24 33",
            v_ini=1.021,
            o_ini=-16.78 * degToRad,
            load=complex(8.7, 6.7),
            generator=complex(0, 4.3),
        )
    )
    bus25 = powerFlow.add_bus(
        PQBus(
            name="Bus 25 33",
            v_ini=1.017,
            o_ini=-16.35 * degToRad,
            load=complex(0, 0),
        )
    )
    bus26 = powerFlow.add_bus(
        PQBus(
            name="Bus 26 33",
            v_ini=1.0,
            o_ini=-16.77 * degToRad,
            load=complex(3.5, 2.3),
        )
    )
    bus27 = powerFlow.add_bus(
        PQBus(
            name="Cloverdle 33",
            v_ini=1.023,
            o_ini=-15.82 * degToRad,
            load=complex(0, 0),
        )
    )
    bus28 = powerFlow.add_bus(
        PQBus(
            name="Cloverdle 132",
            v_ini=1.007,
            o_ini=-11.97 * degToRad,
            load=complex(0, 0),
        )
    )
    bus29 = powerFlow.add_bus(
        PQBus(
            name="Bus 29 33",
            v_ini=1.003,
            o_ini=-17.06 * degToRad,
            load=complex(2.4, 0.9),
        )
    )
    bus30 = powerFlow.add_bus(
        PQBus(
            name="Bus 30 33",
            v_ini=0.992,
            o_ini=-17.94 * degToRad,
            load=complex(10.6, 1.9),
        )
    )
    powerFlow.connectBuses(bus1, bus2, z=complex(0.0192, 0.0575), bc=0.0528)
    powerFlow.connectBuses(bus1, bus3, z=complex(0.0452, 0.1652), bc=0.0408)
    powerFlow.connectBuses(bus2, bus4, z=complex(0.0570, 0.1737), bc=0.0368)
    powerFlow.connectBuses(bus3, bus4, z=complex(0.0132, 0.0379), bc=0.0084)
    powerFlow.connectBuses(bus2, bus5, z=complex(0.0472, 0.1983), bc=0.0418)
    powerFlow.connectBuses(bus2, bus6, z=complex(0.0581, 0.1763), bc=0.0374)
    powerFlow.connectBuses(bus4, bus6, z=complex(0.0119, 0.0414), bc=0.0090)
    powerFlow.connectBuses(bus4, bus12, z=complex(0, 0.25), tap=0.932)
    powerFlow.connectBuses(bus5, bus7, z=complex(0.0460, 0.1160), bc=0.0204)
    powerFlow.connectBuses(bus6, bus7, z=complex(0.0267, 0.0820), bc=0.0170)
    powerFlow.connectBuses(bus6, bus8, z=complex(0.0120, 0.0420), bc=0.0090)
    powerFlow.connectBuses(bus6, bus9, z=complex(0, 0.208))
    powerFlow.connectBuses(bus6, bus10, z=complex(0, 0.556))
    powerFlow.connectBuses(bus9, bus11, z=complex(0, 0.208))
    powerFlow.connectBuses(bus9, bus10, z=complex(0, 0.11))
    powerFlow.connectBuses(bus4, bus12, z=complex(0, 0.256))
    powerFlow.connectBuses(bus12, bus13, z=complex(0, 0.14))
    powerFlow.connectBuses(bus12, bus14, z=complex(0.1231, 0.2559))
    powerFlow.connectBuses(bus12, bus15, z=complex(0.0662, 0.1304))
    powerFlow.connectBuses(bus12, bus16, z=complex(0.0945, 0.1987))
    powerFlow.connectBuses(bus14, bus15, z=complex(0.2210, 0.1997))
    powerFlow.connectBuses(bus16, bus17, z=complex(0.0524, 0.1923))
    powerFlow.connectBuses(bus15, bus18, z=complex(0.1073, 0.2185))
    powerFlow.connectBuses(bus18, bus19, z=complex(0.0639, 0.1292))
    powerFlow.connectBuses(bus19, bus20, z=complex(0.0340, 0.0680))
    powerFlow.connectBuses(bus10, bus20, z=complex(0.0936, 0.2090))
    powerFlow.connectBuses(bus10, bus17, z=complex(0.0324, 0.0845))
    powerFlow.connectBuses(bus10, bus21, z=complex(0.0348, 0.0749))
    powerFlow.connectBuses(bus10, bus22, z=complex(0.0727, 0.1499))
    powerFlow.connectBuses(bus21, bus22, z=complex(0.0116, 0.0236))
    powerFlow.connectBuses(bus15, bus23, z=complex(0.1000, 0.2020))
    powerFlow.connectBuses(bus22, bus24, z=complex(0.1150, 0.1790))
    powerFlow.connectBuses(bus23, bus24, z=complex(0.1320, 0.2700))
    powerFlow.connectBuses(bus24, bus25, z=complex(0.1885, 0.3292))
    powerFlow.connectBuses(bus25, bus26, z=complex(0.2544, 0.3800))
    powerFlow.connectBuses(bus25, bus27, z=complex(0.1093, 0.2087))
    powerFlow.connectBuses(bus27, bus29, z=complex(0.2198, 0.4153))
    powerFlow.connectBuses(bus27, bus30, z=complex(0.3202, 0.6027))
    powerFlow.connectBuses(bus28, bus27, z=complex(0, 0.396), tap=0.968)
    powerFlow.connectBuses(bus29, bus30, z=complex(0.2399, 0.4533))

    powerFlow.solve()


def main():
    # class_example()
    example_14_buses()
    # example_30_buses()

    # four_bus_example()
    # tap_tranformer_example()
    # eleven_buses_task()


if __name__ == "__main__":
    main()
    # TODO make it work lol
