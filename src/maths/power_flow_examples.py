from power_flow import PQBus, PVBus, PowerFlow, SlackBus


# Source: https://apnp.ifsul.edu.br/pluginfile.php/1698423/mod_resource/content/4/6%20Fluxo%20de%20Pot%C3%AAncia.pdf
def class_example():
    # 1pu = 100MW
    powerFlow = PowerFlow()
    bus1 = powerFlow.add_bus(SlackBus(name="Slack Bus", v_esp=1.05))
    bus2 = powerFlow.add_bus(PQBus(name="Load", load=complex(4, 2.5)))
    bus3 = powerFlow.add_bus(PVBus(name="Generator", v_esp=1.04, generator=complex(2)))

    powerFlow.connectBuses(bus1, bus2, z=complex(0.02, 0.04))
    powerFlow.connectBuses(bus2, bus3, z=complex(0.0125, 0.025))
    powerFlow.connectBuses(bus3, bus1, z=complex(0.01, 0.03))

    print(f"Y=\n{powerFlow.yMatrix}\n")

    powerFlow.solve()


def main():
    class_example()


if __name__ == "__main__":
    main()
    # TODO make it work lol
