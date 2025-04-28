from typing import Callable

# row major -> m[r][c]
# ie: [m00 m01 m02]
#     [m10 m11 m12]
#     [m20 m21 m22]
type Matrix = list[list[complex]]

type BusIndex = int

j: complex = complex(0, 1)


def decrease_matrix_order(matrix: Matrix) -> Matrix:
    size = len(matrix)
    new_size = size - 1

    def mapper(i: int, j: int) -> complex:
        return (
            matrix[i][j]
            - matrix[i][size - 1] * matrix[size - 1][j] / matrix[size - 1][size - 1]
        )

    return [[mapper(i, j) for i in range(new_size)] for j in range(new_size)]


def increate_matrix_order(
    matrix: Matrix,
    new_row: Callable[[int], complex],  # (c: int) -> complex,
    new_column: Callable[[int], complex],  # (r: int) -> complex,
    last_value: complex,
) -> Matrix:
    size = len(matrix)
    if size == 0:
        return [[last_value]]

    m: Matrix = [
        [matrix[r][c] for r in range(size)] for c in range(size)
    ]  # copia matriz

    for r in range(size):
        m[r].append(new_column(r))  # adiciona nova coluna no fim

    new_row: list[complex] = [new_row(c) for c in range(size)]  # copia ultima linha
    new_row.append(last_value)  # adiciona ultimo valor da matriz
    m.append(new_row)  # adiciona nova linha no fim
    return m

def format_matrix(matrix: Matrix) -> str:
     return (
            "\n".join([" ".join([f"{c:.2f}" for c in row]) for row in matrix]) + "\n"
        )

class ZBusMatrix:
    def __init__(self, log_print: bool = False):
        self.__m: list[list[complex]] = []
        self.__log_print: bool = log_print

    # Caso 1 - Adicionar um barramento e conecta a terra. Aumenta a ordem da matriz.
    def add_bus_and_connect_to_ground(self, z: complex) -> BusIndex:
        new_bus = len(self.__m)
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 1: adding bus {new_bus+1} to ground, with z = {z}\n")

        # Incrementa a ordem da matriz, zerando a nova linha e coluna.
        self.__m = increate_matrix_order(
            self.__m,
            new_row=lambda c: complex(0),
            new_column=lambda r: complex(0),
            last_value=z,
        )
       
        if self.__log_print:
            print(f"Z = \n{self}")

        return new_bus

    # Caso 2 - Adicionar um barramento e conecta a outro barramento. Aumenta a ordem da matriz.
    def add_bus_and_connect_to_bus(self, z: complex, target: BusIndex) -> BusIndex:
        new_bus = len(self.__m)
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 2: Adding bus {new_bus+1} to bus {target+1}, with z = {z}\n")


        self.__m = increate_matrix_order(
            self.__m,
            new_row=lambda c: self.__m[target][c],
            new_column=lambda r: self.__m[r][target],
            last_value=z + self.__m[target][target],
        )

        if self.__log_print:
            print(f"Z = \n{self}")

        return new_bus

    # Caso 3 - Conectar um barramento a terra. Não aumenta a ordem da matriz.
    def connect_bus_to_ground(self, z: complex, source: BusIndex) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 3: connecting bus {source+1} to ground, with z = {z}\n")

        m = increate_matrix_order(  # codigo do caso 2, apenas renomeando target para source
            self.__m,
            new_row=lambda c: self.__m[source][c],
            new_column=lambda r: self.__m[r][source],
            last_value=z + self.__m[source][source],
        )
        if self.__log_print:
            print(f"Z = \n{format_matrix(m)}")

        self.__m = decrease_matrix_order(m)  # reduz ordem

        if self.__log_print:
            print(f"Reducing order\nZ = \n{self}")

    # Caso 4 - Conectar um barramento a outro barramento. Não aumenta a ordem da matriz.
    # Considenrado o exemplo de aula, source = 2, target = 3
    def connect_bus_to_bus(
        self, z: complex, source: BusIndex, target: BusIndex
    ) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(f"Case 4: connecting bus {source+1} to bus {target+1}, with z = {z}\n")

        last = (
            self.__m[source][source]
            + self.__m[target][target]
            - 2 * self.__m[source][target]
            + z
        )

        def mapper(c: int) -> complex:
            return self.__m[source][c] - self.__m[target][c]

        m = increate_matrix_order(
            self.__m,
            new_row=mapper,
            new_column=mapper,
            last_value=last,
        )
        if self.__log_print:
            print(f"Z = \n{format_matrix(m)}")

        self.__m = decrease_matrix_order(m)

        if self.__log_print:
            print(f"Reducing order\nZ = \n{self}")

    def __str__(self) -> str:
        return format_matrix(self.__m)


def main():
    z = ZBusMatrix(log_print=True)

    bus1 = z.add_bus_and_connect_to_ground(j * 1.2)     # De 1 para 0, z(pu) = j1.2

    bus2 = z.add_bus_and_connect_to_bus(j * 0.2, bus1)  # De 1 para 2, z(pu) = j0.2 

    bus3 = z.add_bus_and_connect_to_bus(j * 0.3, bus1)  # De 1 para 3, z(pu) = j0.3

    z.connect_bus_to_ground(j * 1.5, bus3)              # De 3 para 0, z(pu) = j1.5

    z.connect_bus_to_bus(j * 0.15, bus2, bus3)          # De 2 para 3, z(pu) = j0.15


if __name__ == "__main__":
    main()
