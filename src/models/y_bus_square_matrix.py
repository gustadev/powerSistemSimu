from models.bus_square_matrix import BusSquareMatrix


class YBusSquareMatrix:
    def __init__(self, log_print: bool = False):
        self.__m: BusSquareMatrix = BusSquareMatrix()
        self.__log_print: bool = log_print
        self.__bc: dict[str, float] = {}

    def __getIndex(self, i: int, j: int) -> str:
        if i > j:
            return f"{i}_{j}"
        else:
            return f"{j}_{i}"

    def getBc(self, i: int, j: int) -> float:
        index = self.__getIndex(i, j)
        return self.__bc[index] if index in self.__bc else 0.0

    # Caso 1 - Adicionar um barramento e conecta a terra. Aumenta a ordem da matriz.
    def add_bus(self, y: complex) -> int:
        new_bus = self.__m.size
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 1: adding bus {new_bus+1} to ground, with y = {y}\n")

        # Incrementa a ordem da matriz, zerando a nova linha e coluna.
        self.__m = self.__m.increase_order(last_value=y)

        if self.__log_print:
            print(f"Y = \n{self}")

        return new_bus

    # Caso 4 - Conectar um barramento a outro barramento. Não aumenta a ordem da matriz.
    def connect_bus_to_bus(
        self,
        y: complex,
        source: int,
        target: int,
        bc: float = 0.0,
        tap: complex = complex(1.0),
    ) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(
                f"Case 4: connecting bus {source+1} to bus {target+1}, with y = {y}, tap={tap}:1, bc={bc}\n"
            )

        def mapper(r: int, c: int) -> complex:
            self.__bc[self.__getIndex(source, target)] = bc
            if r == c and r == source:
                return self.__m[r][r] + y / tap / tap
            elif r == c and r == target:
                return self.__m[r][r] + y
            elif r == source and c == target:
                return -y / tap
            elif r == target and c == source:
                return -y / tap
            else:
                return self.__m[r][c]

        self.__m = BusSquareMatrix.generator(self.__m.size, builder=mapper)
        if self.__log_print:
            print(f"Y = \n{self.__m}")

    def __str__(self) -> str:
        return f"{self.__m}"

    @property
    def y_matrix(self) -> list[list[complex | float]]:
        return self.__m.matrix

    @property
    def z_matrix(self) -> list[list[complex | float]]:
        return self.__m.inverse
