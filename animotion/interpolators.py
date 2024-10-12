#/animotion/interpolators.py

def linear_interpolation(start_value: float, end_value: float, t: float) -> float:
    """
    Interpolação linear entre dois valores.
    :param start_value: Valor inicial.
    :param end_value: Valor final.
    :param t: Proporção entre 0 e 1.
    :return: Valor interpolado.
    """
    return start_value + t * (end_value - start_value)

def ease_in(start_value: float, end_value: float, t: float) -> float:
    """
    Interpolação ease-in, que começa lenta e acelera.
    :param start_value: Valor inicial.
    :param end_value: Valor final.
    :param t: Proporção entre 0 e 1.
    :return: Valor interpolado.
    """
    return start_value + (end_value - start_value) * (t ** 2)

def ease_out(start_value: float, end_value: float, t: float) -> float:
    """
    Interpolação ease-out, que começa rápida e desacelera.
    :param start_value: Valor inicial.
    :param end_value: Valor final.
    :param t: Proporção entre 0 e 1.
    :return: Valor interpolado.
    """
    return start_value + (end_value - start_value) * (1 - (1 - t) ** 2)

def ease_in_out(start_value: float, end_value: float, t: float) -> float:
    """
    Interpolação ease-in-out, que começa lenta, acelera e depois desacelera.
    :param start_value: Valor inicial.
    :param end_value: Valor final.
    :param t: Proporção entre 0 e 1.
    :return: Valor interpolado.
    """
    if t < 0.5:
        return start_value + (end_value - start_value) * (2 * t) ** 2 / 2
    else:
        return start_value + (end_value - start_value) * (1 - (-2 * t + 2) ** 2 / 2)
