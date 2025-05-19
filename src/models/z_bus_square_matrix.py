from models.bus_square_matrix import BusSquareMatrix


class ZBusSquareMatrix:
    def __init__(self, log_print: bool = False):
        self.__m: BusSquareMatrix = BusSquareMatrix()
        self.__log_print: bool = log_print

    # Caso 1 - Adicionar um barramento e conecta a terra. Aumenta a ordem da matriz.
    def add_bus_and_connect_to_ground(self, z: complex) -> int:
        new_bus = self.__m.size
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 1: adding bus {new_bus+1} to ground, with z = {z}\n")

        # Incrementa a ordem da matriz, zerando a nova linha e coluna.
        self.__m = self.__m.increase_order(last_value=z)

        if self.__log_print:
            print(f"Z = \n{self}")

        return new_bus

    # Caso 2 - Adicionar um barramento e conecta a outro barramento. Aumenta a ordem da matriz.
    def add_bus_and_connect_to_bus(self, z: complex, target: int) -> int:
        new_bus = self.__m.size
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 2: Adding bus {new_bus+1} to bus {target+1}, with z = {z}\n")

        self.__m = self.__m.increase_order(
            new_row=lambda c: self.__m[target][c],
            new_column=lambda r: self.__m[r][target],
            last_value=z + self.__m[target][target],
        )

        if self.__log_print:
            print(f"Z = \n{self}")

        return new_bus

    # Caso 3 - Conectar um barramento a terra. Não aumenta a ordem da matriz.
    def connect_bus_to_ground(self, z: complex, source: int) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 3: connecting bus {source+1} to ground, with z = {z}\n")

        m = self.__m.increase_order(  # codigo do caso 2, apenas renomeando target para source
            new_row=lambda c: self.__m[source][c],
            new_column=lambda r: self.__m[r][source],
            last_value=z + self.__m[source][source],
        )
        if self.__log_print:
            print(f"Z = \n{m}")

        self.__m = m.decrease_order()  # reduz ordem

        if self.__log_print:
            print(f"Reducing order\nZ = \n{self}")

    # Caso 4 - Conectar um barramento a outro barramento. Não aumenta a ordem da matriz.
    # Considenrado o exemplo de aula, source = 2, target = 3
    def connect_bus_to_bus(self, z: complex, source: int, target: int) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 4: connecting bus {source+1} to bus {target+1}, with z = {z}\n")

        last = (
            self.__m[source][source] + self.__m[target][target] - 2 * self.__m[source][target] + z
        )

        def mapper(c: int) -> complex:
            return self.__m[source][c] - self.__m[target][c]

        m = self.__m.increase_order(
            new_row=mapper,
            new_column=mapper,
            last_value=last,
        )
        if self.__log_print:
            print(f"Z = \n{m}")

        self.__m = m.decrease_order()

        if self.__log_print:
            print(f"Reducing order\nZ = \n{self}")

    def __str__(self) -> str:
        return f"{self.__m}"

    @property
    def y_matrix(self) -> list[list[complex | float]]:
        return self.__m.inverse

    @property
    def z_matrix(self) -> list[list[complex | float]]:
        return self.__m.matrix
