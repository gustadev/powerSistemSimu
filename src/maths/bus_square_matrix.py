from typing import Callable

from scipy import linalg

# row major -> m[r][c]
# ie: [m00 m01 m02]
#     [m10 m11 m12]
#     [m20 m21 m22]

zero = complex(0)


class BusSquareMatrix:
    def __init__(self, m: list[list[complex | float]] = []) -> None:
        self.__m: list[list[complex | float]] = m
        self.__size = len(m)

    @classmethod
    def generator(
        self, size: int, builder: Callable[[int, int], complex] = lambda r, c: zero
    ) -> "BusSquareMatrix":
        m: list[list[complex | float]] = [
            [builder(r, c) for c in range(size)] for r in range(size)
        ]
        return BusSquareMatrix(m)

    @property
    def size(self) -> int:
        return self.__size

    def decrease_order(self) -> "BusSquareMatrix":
        size = self.__size
        new_size = size - 1

        def mapper(i: int, j: int) -> complex:
            return (
                self.__m[i][j]
                - self.__m[i][size - 1]
                * self.__m[size - 1][j]
                / self.__m[size - 1][size - 1]
            )

        return BusSquareMatrix(
            [[mapper(i, j) for i in range(new_size)] for j in range(new_size)]
        )

    def increase_order(
        self,
        new_row: Callable[[int], complex] = lambda c: zero,  # (c: int) -> complex,
        new_column: Callable[[int], complex] = lambda r: zero,  # (r: int) -> complex,
        last_value: complex = zero,  # complex,
    ) -> "BusSquareMatrix":
        size = self.__size
        if size == 0:
            return BusSquareMatrix([[last_value]])

        m: list[list[complex | float]] = [
            [self.__m[r][c] for r in range(size)] for c in range(size)
        ]  # copia matriz

        for r in range(size):
            m[r].append(new_column(r))  # adiciona nova coluna no fim

        new_row: list[complex] = [new_row(c) for c in range(size)]  # copia ultima linha
        new_row.append(last_value)  # adiciona ultimo valor da matriz
        m.append(new_row)  # adiciona nova linha no fim
        return BusSquareMatrix(m)

    def __str__(self) -> str:
        return (
            "\n".join([" ".join([f"{c:.2f}" for c in row]) for row in self.__m]) + "\n"
        )

    @property
    def inverse(self) -> "BusSquareMatrix":
        return BusSquareMatrix(linalg.inv(self.__m))

    def __getitem__(self, row: int) -> list[complex | float]:
        return self.__m[row]
