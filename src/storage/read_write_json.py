import json
from typing import Tuple, cast

from maths.power_flow import PowerFlow
from models.bus import Bus, BusType
from models.line import Line


def save_json_file(
    path: str, buses: list[Bus], lines: list[Line], positions: list[Tuple[float, float]]
) -> None:
    buses_json = list[dict[str, object]]()
    lines_json = list[dict[str, object]]()
    for index, bus in enumerate(buses):
        buses_json.append(
            {
                "id": bus.id,
                "name": bus.name,
                "v": bus.v,
                "o": bus.o,
                "p_load": bus.p_load,
                "q_load": bus.q_load,
                "p_gen": bus.p_gen,
                "q_gen": bus.q_gen,
                "q_min": bus.q_min,
                "q_max": bus.q_max,
                "type": bus.type.value,
                "v_rated": bus.v_rated,
                "b_shunt": bus.b_shunt,
                "g_shunt": bus.g_shunt,
                "position": positions[index],
            }
        )
    for line in lines:
        lines_json.append(
            {
                "id": line.id,
                "name": line.name,
                "b": line.b,
                "g": line.g,
                "bc": line.bc,
                "tap": line.tap,
                "tapBus": line.tap_bus_id,
                "zBus": line.z_bus_id,
            }
        )
    with open(path, "w") as f:
        json.dump({"buses": buses_json, "lines": lines_json}, f, indent=4)
    pass


def read_json_file(path: str) -> Tuple[list[Bus], list[Line], list[Tuple[float, float]]]:
    with open(path, "r") as f:
        data = json.load(f)
    powerFlow = PowerFlow()
    positions: list[Tuple[float, float]] = []
    for busJson in data["buses"]:
        bus = Bus(
            id=busJson["id"],
            name=busJson["name"],
            v=busJson["v"],
            o=busJson["o"],
            p_load=busJson["p_load"],
            q_load=busJson["q_load"],
            p_gen=busJson["p_gen"],
            q_gen=busJson["q_gen"],
            q_min=busJson["q_min"],
            q_max=busJson["q_max"],
            type=BusType(busJson["type"]),
            v_rated=busJson["v_rated"],
            b_shunt=busJson["b_shunt"],
            g_shunt=busJson["g_shunt"],
        )
        powerFlow.add_bus(bus)
        positions.append(tuple(busJson["position"]))
    for lineJson in data["lines"]:
        line = Line(
            id=lineJson["id"],
            name=lineJson["name"],
            b=lineJson["b"],
            g=lineJson["g"],
            bc=lineJson["bc"],
            tap=lineJson["tap"],
            tap_bus_id=powerFlow.buses[lineJson["tapBus"]],
            z_bus_id=powerFlow.buses[lineJson["zBus"]],
        )
        powerFlow.add_connection(line)
    return (
        cast(list[Bus], powerFlow.buses.values()),
        cast(list[Line], powerFlow.connections.values()),
        positions,
    )
