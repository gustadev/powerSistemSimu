from bus_square_matrix import BusSquareMatrix


type BusIndex = int

j: complex = complex(0, 1)


class YBusSquareMatrix:
    def __init__(self, log_print: bool = False):
        self.__m: BusSquareMatrix = BusSquareMatrix()
        self.__log_print: bool = log_print

    # Caso 1 - Adicionar um barramento e conecta a terra. Aumenta a ordem da matriz.
    def add_bus(self, y: complex) -> BusIndex:
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
        self, y: complex, source: BusIndex, target: BusIndex
    ) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(
                f"Case 4: connecting bus {source+1} to bus {target+1}, with y = {y}\n"
            )

        # TODO fix
        def mapper(r: int, c: int) -> complex:
            if r == source and c == source:
                return self.__m[r][c] + y
            elif r == target and c == source:
                return self.__m[r][c] + y
            elif r == source or c == source:
                return self.__m[r][c] - self.__m[source][target]
            elif r == target or c == target:
                return self.__m[r][c] - self.__m[target][source]
            else:
                return self.__m[r][c]

        self.__m = BusSquareMatrix.generator(self.__m.size, builder=mapper)
        if self.__log_print:
            print(f"Y = \n{self.__m}")

    def __str__(self) -> str:
        return f"{self.__m}"

    @property
    def zBus(self) -> BusSquareMatrix:
        return self.__m.inverse


def main():
    y = YBusSquareMatrix(log_print=True)

    bus1 = y.add_bus(1 / (j * 1.2))  # De 1 para 0, z(pu) = j1.2

    bus2 = y.add_bus(0) # De 2 para 0, z(pu) = 0

    bus3 = y.add_bus(1 / (j * 1.5)) # De 3 para 0, z(pu) = j1.5

    y.connect_bus_to_bus(1 / (j * 0.2), bus1, bus2)  # De 1 para 2, z(pu) = j0.2

    y.connect_bus_to_bus(1 / (j * 0.3), bus1, bus3)  # De 1 para 3, z(pu) = j0.3

    y.connect_bus_to_bus(1 / (j * 0.15), bus2, bus3)  # De 2 para 3, z(pu) = j0.15

    print(y.zBus)   

    # Z = FINAL
    # 0.00+0.70j 0.00+0.66j 0.00+0.63j
    # 0.00+0.66j 0.00+0.75j 0.00+0.68j
    # 0.00+0.63j 0.00+0.68j 0.00+0.71j

    # Y = 
    # 0.00-9.17j 0.00+5.00j -0.00+3.33j
    # 0.00+5.00j 0.00-11.67j -0.00+6.67j
    # 0.00+3.33j 0.00+6.67j 0.00-10.67j

    # TODO make it work

if __name__ == "__main__":
    main()
