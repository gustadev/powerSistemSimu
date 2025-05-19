import cmath
from enum import Enum

from models.network_element import NetworkElement


class BusType(Enum):
    SLACK = 3
    PV = 2
    PQ = 0


class Bus(NetworkElement):
    __number: int = 0

    def __init__(
        self,
        name: str | None = None,
        v: float = 1,
        o: float = 0,
        load: complex | None = None,
        generator: complex | None = None,
        q_min: float | None = None,
        q_max: float | None = None,
        type: BusType = BusType.PQ,
        v_rated: float = 1,
        index: int = -1,  # to be used by power flow solver
        shunt: complex = complex(0),
        number: int | None = None,
        id: int | None = None,
    ):
        __load = load if load is not None else complex(0)
        __generator = generator if generator is not None else complex(0)

        self.v_sch: float = v
        self.o_sch: float = o
        self.p_sch: float = (__generator - __load).real
        self.q_sch: float = (__generator - __load).imag

        if number is not None:
            self.number: int = number
        else:
            self.number: int = Bus.__number
            Bus.__number += 1

        if name:
            self.name: str = name
        else:
            self.name: str = f"Bus {self.number:03d}"

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
        super().__init__(name=self.name, id=id)

    def copy_with(
        self,
        name: str | None = None,
        v: float | None = None,
        o: float | None = None,
        load: complex | None = None,
        generator: complex | None = None,
        q_min: float | None = None,
        q_max: float | None = None,
        type: BusType | None = None,
        v_rated: float | None = None,
        index: int | None = None,
        shunt: complex | None = None,
    ) -> "Bus":
        return Bus(
            name=name if name is not None else self.name,
            number=self.number,
            v=v if v is not None else self.v,
            o=o if o is not None else self.o,
            load=load if load is not None else self.load,
            generator=generator if generator is not None else self.generator,
            q_min=q_min if q_min is not None else self.q_min,
            q_max=q_max if q_max is not None else self.q_max,
            type=type if type is not None else self.type,
            v_rated=v_rated if v_rated is not None else self.v_rated,
            index=index if index is not None else self.index,
            shunt=shunt if shunt is not None else self.shunt,
            id=self.id,
        )

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
