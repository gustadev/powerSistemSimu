from typing import Tuple

from maths.power_flow import PowerFlow
from models.bus import Bus
from models.line import Line
from storage.read_tables_ieee import read_power_flow_from_ieee
from storage.read_write_json import read_json_file, save_json_file


class StorageFacade:

    @staticmethod
    def read_ieee_file(path: str) -> PowerFlow:
        return read_power_flow_from_ieee(path)

    @staticmethod
    def read_json_file(path: str) -> Tuple[list[Bus], list[Line], list[Tuple[float, float]]]:
        return read_json_file(path)

    @staticmethod
    def save_json_file(
        path: str,
        buses: list[Bus],
        lines: list[Line],
        positions: list[Tuple[float, float]],
    ) -> None:
        return save_json_file(path, buses, lines, positions)
