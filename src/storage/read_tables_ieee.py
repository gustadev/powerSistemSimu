import pandas as pd
import numpy as np
from typing import Any, Tuple

from models.bus import Bus, BusType
from models.line import Line
from maths.power_flow import PowerFlow


def __read_data_ieee_cdf(path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    lines = []
    with open(path, "+r") as f:
        lines = f.readlines()

    line_bus_size_split = str(lines[1]).split(" ")
    # TO DO: Fazer busca pelas linhas pela linha que começa com "BUS DATA FOLLOWS"
    # e então aplicar nessa linha o comando abaixo subistituindo o indice fixo [3] pela linha encontrada
    # TO DO: Contar quantas linhas entre a linha começando por "BUS DATA FOLLOWS" e a proxima linha iniciando por "-999"
    last_bus_line = int([l.strip() for l in line_bus_size_split if l.strip()][3]) + 2
    buses_ = lines[2:last_bus_line]
    buses = list[Any]()
    for raw_row in buses_:
        parsed_row = list[str | float]()
        parsed_row.append(int(raw_row[0:4]))  # Columns  1- 4   Bus number (I) *
        parsed_row.append(str(raw_row[5:17]).strip())  # Columns  7-17   Name (A) (left justify) *
        # bar.append(str(b[18:20]).strip()) # Columns 19-20   Load flow area number (I) Don't use zero! *
        # bar.append(str(b[20:23]).strip())  # Columns 21-23   Loss zone number (I)
        parsed_row.append(int(raw_row[24:26]))  # Columns 25-26   Type (I) *
        parsed_row.append(float(raw_row[27:33]))  # Columns 28-33   Final voltage, p.u. (F) *
        parsed_row.append(float(raw_row[33:40]))  # Columns 34-40   Final angle, degrees (F) *
        parsed_row.append(float(raw_row[41:49]))  # Columns 41-49   Load MW (F) *
        parsed_row.append(float(raw_row[49:59]))  # Columns 50-59   Load MVAR (F) *
        parsed_row.append(float(raw_row[59:67]))  # Columns 60-67   Generation MW (F) *
        parsed_row.append(float(raw_row[67:75]))  # Columns 68-75   Generation MVAR (F) *
        parsed_row.append(float(raw_row[76:83]))  # Columns 77-83   Base KV (F)
        # Columns 85-90   Desired volts (pu) (F) (This is desired remote voltage if this bus is controlling another bus.
        # bar.append(float(b[84:90]))
        parsed_row.append(
            float(raw_row[90:98])
        )  # Columns 91-98   Maximum MVAR or voltage limit (F)
        parsed_row.append(
            float(raw_row[98:106])
        )  # Columns 99-106  Minimum MVAR or voltage limit (F)
        parsed_row.append(
            float(raw_row[106:114])
        )  # Columns 107-114 Shunt conductance G (per unit) (F) *
        parsed_row.append(
            float(raw_row[114:122])
        )  # Columns 115-122 Shunt susceptance B (per unit) (F) *
        # bar.append(float(b[123:127]))  # Columns 124-127 Remote controlled bus number
        buses.append(parsed_row)

    buses = pd.DataFrame(buses)
    buses.columns = [
        "number",
        "name",
        "type",
        "voltage",
        "angle",
        "p_load",
        "q_load",
        "p_gen",
        "q_gen",
        "v_rated",
        # "Desired volts (pu)",
        "q_max",
        "q_min",
        "shunt_g",
        "shunt_b",
        # "Remote controlled bus number",
    ]

    # TO DO: Fazer busca pelas linhas pela linha que começa com "BRANCH DATA FOLLOWS"
    # e então aplicar nessa linha o comando abaixo subistituindo o calcuo de indice pela linha encontrada
    # TO DO: Contar quantas linhas entre a linha começando por "BRANCH DATA FOLLOWS" e a proxima linha iniciando por "-999"
    line_lines_size_split = str(lines[last_bus_line + 1]).split(" ")
    last_line_line = [l.strip() for l in line_lines_size_split if l.strip()]
    last_line_line = int(last_line_line[3]) + 1
    lines_ = lines[(last_bus_line + 2) : (last_bus_line + last_line_line)]

    lines = list[Any]()
    for raw_row in lines_:
        parsed_row = list[str | float]()
        parsed_row.append(int(raw_row[0:4]))  # Columns  1- 4   Tap bus number (I) *
        parsed_row.append(int(raw_row[5:9]))  # Columns  6- 9   Z bus number (I) *
        # parsed_row.append(str(raw_row[10:12]).strip())  # Columns 11-12   Load flow area (I)
        # # parsed_row.append(str(raw_row[12:15]).strip())  # Columns 13-14   Loss zone (I)
        # parsed_row.append(
        #     str(raw_row[16:17]).strip()
        # )  # Column  17      Circuit (I) * (Use 1 for single lines)
        # parsed_row.append(str(raw_row[18:19]).strip())  # Column  19      Type (I) *
        parsed_row.append(float(raw_row[20:29]))
        # Columns 20-29   Branch resistance R, per unit (F) *
        parsed_row.append(float(raw_row[30:40]))
        # Columns 30-40   Branch reactance X, per unit (F) * No zero impedance lines
        parsed_row.append(float(raw_row[41:50]))

        # Columns 41-50   Line charging B, per unit (F) * (total line charging, +B)
        # parsed_row.append(
        #     float(raw_row[51:55]).strip()
        # )  # Columns 51-55   Line MVA rating No 1 (I) Left justify!
        # parsed_row.append(
        #     float(raw_row[57:61]).strip()
        # )  # Columns 57-61   Line MVA rating No 2 (I) Left justify!
        # parsed_row.append(
        #     str(raw_row[63:67]).strip()
        # )  # Columns 63-67   Line MVA rating No 3 (I) Left justify!
        # parsed_row.append(str(raw_row[69:72]).strip())  # Columns 69-72   Control bus number
        # parsed_row.append(str(raw_row[73]).strip())  # Column  74      Side (I)
        # parsed_row.append(
        #     str(raw_row[76:82]).strip()
        # )  # Columns 77-82   Transformer final turns ratio (F)
        # parsed_row.append(
        #     str(raw_row[84:89]).strip()
        # )  # Columns 84-90   Transformer (phase shifter) final angle (F)
        parsed_row.append(float(raw_row[77:82]))
        # )  # Columns 91-97   Minimum tap or phase shift (F)
        # parsed_row.append(
        #     str(raw_row[97:104]).strip()
        # )  # Columns 98-104  Maximum tap or phase shift (F)
        # parsed_row.append(str(raw_row[105:111]).strip())  # Columns 106-111 Step size (F)
        # parsed_row.append(
        #     str(raw_row[112:117]).strip()
        # )  # Columns 113-119 Minimum voltage, MVAR or MW limit (F)
        # parsed_row.append(
        #     str(raw_row[118:126]).strip()
        # )  # Columns 120-126 Maximum voltage, MVAR or MW limit (F)
        lines.append(parsed_row)

    lines = pd.DataFrame(lines)
    lines.columns = [
        "tap_bus",
        "z_bus",
        # "Load flow area",
        # "Loss zone",
        # "Circuit",
        # "Type",
        "r",
        "x",
        "b",
        # "Line MVA rating No 1",
        # "Line MVA rating No 2",
        # "Line MVA rating No 3",
        # "Control bus number",
        # "Side",
        # "Transformer final turns ratio", -> tap
        "tap",
        # "Transformer (phase shifter) final angle",
        # "Minimum tap or phase shift",
        # "Maximum tap or phase shift",
        # "Step size",
        # "Minimum voltage",
        # "Maximum voltage",
    ]

    return buses, lines


def read_power_flow_from_ieee(path: str, base_mw: int = 100) -> PowerFlow:
    buses, lines = __read_data_ieee_cdf(path)
    powerFlow = PowerFlow(base_mw)
    for _, row in buses.iterrows():  # type: ignore
        number: int = int(row["number"])  # type: ignore
        name: str = str(row["name"])  # type: ignore
        v: float = float(row["voltage"])  # type: ignore
        o: float = float(row["angle"]) * np.pi / 180  # type: ignore
        p_load: float = float(row["p_load"])  # type: ignore
        q_load: float = float(row["q_load"])  # type: ignore
        p_gen: float = float(row["p_gen"])  # type: ignore
        q_gen: float = float(row["q_gen"])  # type: ignore
        q_min: float = float(row["q_min"])  # type: ignore
        q_max: float = float(row["q_max"])  # type: ignore
        bus_type: BusType = BusType(row["type"])  # type: ignore
        v_rated: float = float(row["v_rated"])  # type: ignore
        g_shunt: float = float(row["shunt_g"])  # type: ignore
        b_shunt: float = float(row["shunt_b"])  # type: ignore

        bus: Bus = Bus(
            id=f"{number}b",
            name=name,
            number=number,
            v=v,
            o=o,
            p_load=p_load,
            q_load=q_load,
            p_gen=p_gen,
            q_gen=q_gen,
            q_min=q_min if q_min != 0 else float("-inf"),
            q_max=q_max if q_max != 0 else float("inf"),
            type=bus_type,
            v_rated=v_rated,
            b_shunt=b_shunt,
            g_shunt=g_shunt,
        )

        powerFlow.add_bus(bus)

    for _, row in lines.iterrows():  # type: ignore
        tapBus: int = int(row["tap_bus"])  # type: ignore
        zBus: int = int(row["z_bus"])  # type: ignore
        bc: float = float(row["b"])  # type: ignore
        z: complex = complex(float(row["r"]), float(row["x"]))  # type: ignore
        tap: float = float(row["tap"]) if float(row["tap"]) != 0 else 1.0  # type: ignore

        connection: Line = Line.from_z(
            powerFlow.buses[f"{tapBus}b"],
            powerFlow.buses[f"{zBus}b"],
            z=z,
            bc=bc,
            tap=tap,
        )

        powerFlow.add_connection(connection)

    return powerFlow
