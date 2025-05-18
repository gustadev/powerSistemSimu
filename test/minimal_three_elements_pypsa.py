import numpy as np
import pypsa

network: pypsa.Network = pypsa.Network()

n_buses = 3

for i in range(n_buses):
    network.add("Bus", f"My bus {i}", v_nom=20.0)  # type: ignore

print(network.buses)

for i in range(n_buses):
    network.add(  # type: ignore
        "Line",
        f"My line {i}",
        bus0=f"My bus {i}",
        bus1=f"My bus {(i + 1) % n_buses}",
        x=0.1,
        r=0.01,
    )

print(network.lines)

network.add("Generator", "My gen", bus="My bus 0", p_set=100, control="PQ")  # type: ignore

print(network.generators)

print(network.generators.p_set)  # type: ignore

network.add("Load", "My load", bus="My bus 1", p_set=100)  # type: ignore

print(network.loads)

print(network.loads.p_set)  # type: ignore

network.loads.q_set = 100.0

network.pf()  # type: ignore

print(network.lines_t.p0)

print(network.buses_t.v_ang * 180 / np.pi)

print(network.buses_t.v_mag_pu)
