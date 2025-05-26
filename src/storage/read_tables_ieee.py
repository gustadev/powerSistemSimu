from cmath import pi
from enum import Enum

from models.bus import Bus, BusType
from models.line import Line
from maths.power_flow import PowerFlow


class __ReadStep(Enum):
    TITLE = 0
    BUS_DATA = 1
    BRANCH_DATA = 2


def read_power_flow_from_ieee(path: str) -> PowerFlow:
    step = __ReadStep.TITLE
    powerFlow = PowerFlow(base=100.0)
    with open(path, "+r") as file:

        while True:
            line = file.readline()

            if step is __ReadStep.TITLE:
                line = file.readline()  # skip bus headers
                step = __ReadStep.BUS_DATA
                continue

            if step is __ReadStep.BUS_DATA and not line.startswith("-999"):
                powerFlow.add_bus(parse_bus(line))
                continue

            if step is __ReadStep.BUS_DATA:
                step = __ReadStep.BRANCH_DATA
                line = file.readline()  # skip branch headers
                continue

            if step is __ReadStep.BRANCH_DATA and not line.startswith("-999"):
                powerFlow.add_connection(parse_line(line))
                continue

            break
        return powerFlow


__degrees_to_radians = pi / 180.0


def parse_bus(line: str) -> Bus:
    return Bus(
        number=int(line[0:4]),  # Columns  1- 4   Bus number (I) *
        id=str(line[0:4]),  # Columns  1- 4   Bus number (I) *
        name=str(line[5:17]).strip(),  # Columns  7-17   Name (A) (left justify) *
        type=BusType(int(line[24:26])),  # Columns 25-26   Type (I) *
        v=float(line[27:33]),  # Columns 28-33   Final voltage, p.u. (F) *
        o=float(line[33:40]) * __degrees_to_radians,  # Columns 34-40   Final angle, degrees (F) *
        p_load=float(line[41:49]),  # Columns 41-49   Load MW (F) *
        q_load=float(line[49:59]),  # Columns 50-59   Load MVAR (F) *
        p_gen=float(line[59:67]),  # Columns 60-67   Generation MW (F) *
        q_gen=float(line[67:75]),  # Columns 68-75   Generation MVAR (F) *
        v_rated=float(line[76:83]),  # Columns 77-83   Base KV (F)
        q_max=float(line[90:98]),  # Columns 91-98   Maximum MVAR or voltage limit (F)
        q_min=float(line[98:106]),  # Columns 99-106  Minimum MVAR or voltage limit (F)
        g_shunt=float(line[106:114]),  # Columns 107-114 Shunt conductance G (per unit) (F) *
        b_shunt=float(line[114:122]),  # Columns 115-122 Shunt susceptance B (per unit) (F) *
    )


def parse_line(line: str) -> Line:
    tap = float(line[77:82])
    return Line.from_z(
        tap_bus_id=str(line[0:4]),
        z_bus_id=str(line[5:9]),
        z=complex(
            # Columns 20-29   Branch resistance R, per unit (F) *
            float(line[20:29]),
            # Columns 30-40   Branch reactance X, per unit (F) * No zero impedance lines
            float(line[30:40]),
        ),
        # Columns 41-50   Line charging B, per unit (F) * (total line charging, +B)
        bc=float(line[41:50]),
        tap=tap if tap != 0 else 1.0,  # Columns 77-82   Transformer final turns ratio (F)
    )
