import pandas as pd
import numpy as np
from typing import Tuple, Optional
from bus import Bus
from power_flow import PowerFlow


def read_data_ieee_cdf(path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:

    lines = []
    with open(path, "+r") as f:
        lines = f.readlines()

    line_bus_size_split = str(lines[1]).split(" ")
    # TO DO: Fazer busca pelas linhas pela linha que começa com "BUS DATA FOLLOWS"
    # e então aplicar nessa linha o comando abaixo subistituindo o indice fixo [3] pela linha encontrada
    # TO DO: Contar quantas linhas entre a linha começando por "BUS DATA FOLLOWS" e a proxima linha iniciando por "-999"
    last_bus_line = int([l.strip() for l in line_bus_size_split if l.strip()][3]) + 2
    buses_ = lines[2:last_bus_line]
    buses = []
    for raw_row in buses_:
        parsed_row = []
        parsed_row.append(str(raw_row[0:4]).strip())  # Columns  1- 4   Bus number (I) *
        parsed_row.append(str(raw_row[5:17]).strip())  # Columns  7-17   Name (A) (left justify) *
        # bar.append(str(b[18:20]).strip()) # Columns 19-20   Load flow area number (I) Don't use zero! *
        # bar.append(str(b[20:23]).strip())  # Columns 21-23   Loss zone number (I)
        parsed_row.append(str(raw_row[24:26]).strip())  # Columns 25-26   Type (I) *
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

    lines = []
    for raw_row in lines_:
        parsed_row = []
        parsed_row.append(int(raw_row[0:4]))  # Columns  1- 4   Tap bus number (I) *
        parsed_row.append(int(raw_row[5:9]))  # Columns  6- 9   Z bus number (I) *
        # parsed_row.append(str(raw_row[10:12]).strip())  # Columns 11-12   Load flow area (I)
        # # parsed_row.append(str(raw_row[12:15]).strip())  # Columns 13-14   Loss zone (I)
        # parsed_row.append(
        #     str(raw_row[16:17]).strip()
        # )  # Column  17      Circuit (I) * (Use 1 for single lines)
        parsed_row.append(str(raw_row[18:19]).strip())  # Column  19      Type (I) *
        parsed_row.append(
            float(raw_row[20:29])
        )  # Columns 20-29   Branch resistance R, per unit (F) *
        parsed_row.append(
            float(raw_row[30:40])
        )  # Columns 30-40   Branch reactance X, per unit (F) * No zero impedance lines
        parsed_row.append(
            float(raw_row[41:50]).strip()
        )  # Columns 41-50   Line charging B, per unit (F) * (total line charging, +B)
        parsed_row.append(
            float(raw_row[51:55]).strip()
        )  # Columns 51-55   Line MVA rating No 1 (I) Left justify!
        parsed_row.append(
            float(raw_row[57:61]).strip()
        )  # Columns 57-61   Line MVA rating No 2 (I) Left justify!
        parsed_row.append(
            str(raw_row[63:67]).strip()
        )  # Columns 63-67   Line MVA rating No 3 (I) Left justify!
        parsed_row.append(str(raw_row[69:72]).strip())  # Columns 69-72   Control bus number
        parsed_row.append(str(raw_row[73]).strip())  # Column  74      Side (I)
        parsed_row.append(
            str(raw_row[76:82]).strip()
        )  # Columns 77-82   Transformer final turns ratio (F)
        parsed_row.append(
            str(raw_row[84:89]).strip()
        )  # Columns 84-90   Transformer (phase shifter) final angle (F)
        parsed_row.append(
            str(raw_row[90:97]).strip()
        )  # Columns 91-97   Minimum tap or phase shift (F)
        parsed_row.append(
            str(raw_row[97:104]).strip()
        )  # Columns 98-104  Maximum tap or phase shift (F)
        parsed_row.append(str(raw_row[105:111]).strip())  # Columns 106-111 Step size (F)
        parsed_row.append(
            str(raw_row[112:117]).strip()
        )  # Columns 113-119 Minimum voltage, MVAR or MW limit (F)
        parsed_row.append(
            str(raw_row[118:126]).strip()
        )  # Columns 120-126 Maximum voltage, MVAR or MW limit (F)
        lines.append(parsed_row)

    lines = pd.DataFrame(lines)
    lines.columns = [
        "Tap bus number",
        "Z bus number",
        "Load flow area",
        "Loss zone",
        "Circuit",
        "Type",
        "Branch resistance R",
        "Branch reactance X",
        "Line charging B",
        "Line MVA rating No 1",
        "Line MVA rating No 2",
        "Line MVA rating No 3",
        "Control bus number",
        "Side",
        "Transformer final turns ratio",
        "Transformer (phase shifter) final angle",
        "Minimum tap or phase shift",
        "Maximum tap or phase shift",
        "Step size",
        "Minimum voltage",
        "Maximum voltage",
    ]

    return buses, lines


if __name__ == "__main__":
    buses, lines = read_data_ieee_cdf(
        "/Users/sthefano/dev-school/powerSistemSimu/src/maths/data/14_Barras/ieee14cdf.txt"
    )
    print(buses.info())
    print(lines.info())
    powerFlow = PowerFlow()
    for _, row in buses.iterrows():
        powerFlow.add_bus(
            Bus(
                name=row["name"],
                v=row["voltage"],
                o=row["angle"],
                load=complex(row["p_load"], row["q_load"]),
                generator=complex(row["p_gen"], row["q_gen"]),
                q_min=row["q_min"],
                q_max=row["q_max"],
                type=row["type"],
                v_rated=row["v_rated"],
            ),
        )

    for bus in powerFlow.buses:
        print(
            f"Bus {bus.name}: Voltage = {bus.v}, Angle = {bus.o}, Load = {bus.load}, Generator = {bus.generator}"
        )
    #  continue8778

    # print("Bus Data:")
    # for field, value in row.items():
    #     print(f" {field}: {value} {row.get(field)}")

    # bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\30_Barras\\ieee30cdf.txt")
    # print(bars.info())
    # print(line_connects.info())
    # bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\57_Barras\\ieee57cdf.txt")
    # print(bars.info())
    # print(line_connects.info())
    # bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\118_Barras\\ieee118cdf.txt")
    # print(bars.info())
    # print(line_connects.info())
    # bars, line_connects = read_data_ieee_cdf("C:\\Users\\gusta\\OneDrive\\PROJETOS\\PySide\\powerSistemSimu\\src\\maths\\data\\300_Barras\\ieee300cdf.txt")
    # print(bars.info())
    # print(line_connects.info())
