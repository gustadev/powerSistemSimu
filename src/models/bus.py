import cmath
from enum import Enum


class BusType(Enum):
    SLACK = 3
    PV = 2
    PQ = 0


class Bus:
    def __init__(
        self,
        name: str,
        v: float = 1,
        o: float = 0,
        load: complex = complex(0),
        generator: complex = complex(0),
        q_min: float | None = None,
        q_max: float | None = None,
        type: BusType = BusType.PQ,
        v_rated: float = 1,
        index: int = -1,  # to be used by power flow solver
        shunt: complex = complex(0),
    ):
        self.v_sch: float = v
        self.o_sch: float = o
        self.p_sch: float = (generator - load).real
        self.q_sch: float = (generator - load).imag

        self.name: str = name
        self.v: float = v
        self.o: float = o
        self.p: float = self.p_sch
        self.q: float = self.q_sch
        self.load: complex | None = load if load != complex(0) else None
        self.generator: complex | None = generator if generator != complex(0) else None
        self.q_min: float | None = q_min
        self.q_max: float | None = q_max
        self.index: int = index
        self.type: BusType = type
        self.v_rated: float = v_rated
        self.shunt: complex = shunt

    def __str__(self) -> str:
        q_min: str = "        "
        if self.q_min:
            q_min = f"{self.q_min:+8.2f}"
        q_max: str = "        "
        if self.q_max:
            q_max = f"{self.q_max:+8.2f}"
        return (
            f"#{self.index:3d} | Type: {self.type.value} | V: {self.v:+4.3f}/_ {(self.o*180/cmath.pi):+8.4f}o |"
            + f" P: {self.p:+8.2f} | Q: {self.q:+8.2f} |"
            + f" P_sch: {self.p_sch:+8.2f} | Q_sch: {self.q_sch:+8.2f} |"
            + f" Q_min: {q_min} | Q_max: {q_max} | shunt: {self.shunt.real:+4.2f}  {self.shunt.imag:+4.2f}j |"
        )
