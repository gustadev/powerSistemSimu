from bus_square_matrix import BusSquareMatrix


type BusIndex = int

j: complex = complex(0, 1)


class ZBusSquareMatrix:
    def __init__(self, log_print: bool = False):
        self.__m: BusSquareMatrix = BusSquareMatrix()
        self.__log_print: bool = log_print

    # Caso 1 - Adicionar um barramento e conecta a terra. Aumenta a ordem da matriz.
    def add_bus_and_connect_to_ground(self, z: complex) -> BusIndex:
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
    def add_bus_and_connect_to_bus(self, z: complex, target: BusIndex) -> BusIndex:
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
    def connect_bus_to_ground(self, z: complex, source: BusIndex) -> None:
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
    def connect_bus_to_bus(
        self, z: complex, source: BusIndex, target: BusIndex
    ) -> None:
        if self.__log_print:
            print(f"==========================================")
            print(
                f"Case 4: connecting bus {source+1} to bus {target+1}, with z = {z}\n"
            )

        last = (
            self.__m[source][source]
            + self.__m[target][target]
            - 2 * self.__m[source][target]
            + z
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
    def ybus(self) -> BusSquareMatrix:
        return self.__m.inverse


def main():
    z = ZBusSquareMatrix(log_print=True)

    bus1 = z.add_bus_and_connect_to_ground(j * 1.2)  # De 1 para 0, z(pu) = j1.2

    bus2 = z.add_bus_and_connect_to_bus(j * 0.2, bus1)  # De 1 para 2, z(pu) = j0.2

    bus3 = z.add_bus_and_connect_to_bus(j * 0.3, bus1)  # De 1 para 3, z(pu) = j0.3

    z.connect_bus_to_ground(j * 1.5, bus3)  # De 3 para 0, z(pu) = j1.5

    z.connect_bus_to_bus(j * 0.15, bus2, bus3)  # De 2 para 3, z(pu) = j0.15

    print(f"Y = \n{z.ybus}")

    # Z = FINAL
    # 0.00+0.70j 0.00+0.66j 0.00+0.63j
    # 0.00+0.66j 0.00+0.75j 0.00+0.68j
    # 0.00+0.63j 0.00+0.68j 0.00+0.71j

    # Y = 
    # 0.00-9.17j 0.00+5.00j -0.00+3.33j
    # 0.00+5.00j 0.00-11.67j -0.00+6.67j
    # 0.00+3.33j 0.00+6.67j 0.00-10.67j

    # z = ZBusMatrix(log_print=True)
    # bus1 = z.add_bus_and_connect_to_ground(100000000)
    # bus2 = z.add_bus_and_connect_to_bus(0.1 * j, bus1)
    # bus3 = z.add_bus_and_connect_to_bus(0.25 * j, bus1)
    # z.connect_bus_to_bus(0.2 * j, bus2, bus3)
    # print(z.ybus)


if __name__ == "__main__":
    main()
