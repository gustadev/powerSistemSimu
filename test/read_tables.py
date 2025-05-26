import os

import numpy as np

from storage.read_tables_ieee import read_power_flow_from_ieee


def __test_14_bus():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "../assets/ieee_examples/ieee14cdf.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    power_flow = read_power_flow_from_ieee(abs_file_path)

    # fmt:off
    # final_v : list[float] = [1.06, 1.045, 1.01, 1.01767085369177, 1.01951385981906, 1.07, 1.06151953249094, 1.09, 1.05593172063697, 1.05098462499985, 1.05690651854037, 1.05518856319710, 1.05038171362860, 1.03552994585357]
    # final_o : list[float] = [0.0, -4.98258914197497, -12.7250999382679, -10.3129010923315, -8.77385389829527, -14.2209464637019, -13.3596273653462, -13.3596273653462, -14.9385212952289, -15.0972884630709, -14.7906220313214, -15.0755845204241, -15.1562763362218, -16.0336445292053]
    # fmt:on

    power_flow.solve(max_iterations=100)


# https://apnp.ifsul.edu.br/pluginfile.php/1700773/mod_resource/content/1/Trab2-1_IEEE_14_nos.pdf
def __test_14_bus_class():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "../assets/ieee_examples/ieee14cdf_class.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    power_flow = read_power_flow_from_ieee(abs_file_path)

    power_flow.solve(max_iterations=100)

    pass


if __name__ == "__main__":
    __test_14_bus()
    __test_14_bus_class()
