# Adapted from Python-master/maths/special_numbers/proth_number.py::proth

import math

def proth(number: int) -> int:
    """
    :param number: nth number to calculate in the sequence
    :return: the nth number in Proth number
    Note: indexing starts at 1 i.e. proth(1) gives the first Proth number of 3
    >>> proth(6)
    25
    >>> proth(0)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=0] must be > 0
    >>> proth(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=-1] must be > 0
    >>> proth(6.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=6.0] must be an integer
    """

    if not isinstance(number, int):
        msg = f"Input value of [number={number}] must be an integer"
        raise TypeError(msg)

    if number < 1:
        msg = f"Input value of [number={number}] must be > 0"
        raise ValueError(msg)
    elif number == 1:
        return 3
    elif number == 2:
        return 5
    else:
        """
        +1 for binary starting at 0 i.e. 2^0, 2^1, etc.
        +1 to start the sequence at the 3rd Proth number
        Hence, we have a +2 in the below statement
        """
        block_index = int(math.log(number // 3, 2)) + 2

        proth_list = [3, 5]
        proth_index = 2
        increment = 3
        for block in range(1, block_index):
            for _ in range(increment):
                proth_list.append(2 ** (block + 1) + proth_list[proth_index - 1])
                proth_index += 1
            increment *= 2

    return proth_list[number - 1]

def is_proth_number(number: int) -> bool:
    """
    :param number: positive integer number
    :return: true if number is a Proth number, false otherwise
    >>> is_proth_number(1)
    False
    >>> is_proth_number(2)
    False
    >>> is_proth_number(3)
    True
    >>> is_proth_number(4)
    False
    >>> is_proth_number(5)
    True
    >>> is_proth_number(34)
    False
    >>> is_proth_number(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input value of [number=-1] must be > 0
    >>> is_proth_number(6.0)
    Traceback (most recent call last):
        ...
    TypeError: Input value of [number=6.0] must be an integer
    """
    if not isinstance(number, int):
        message = f"Input value of [{number=}] must be an integer"
        raise TypeError(message)

    if number <= 0:
        message = f"Input value of [{number=}] must be > 0"
        raise ValueError(message)

    if number == 1:
        return False

    number -= 1
    n = 0
    while number % 2 == 0:
        n += 1
        number //= 2
    return number < 2**n
