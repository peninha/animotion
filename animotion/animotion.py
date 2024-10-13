# /animotion/animotion.py
import time
import threading
from typing import List, Tuple, Callable

# TODO: Implementar suporte a diferentes tipos de interpoladores fornecidos dinamicamente
# TODO: Permitir interpolar mais de um valor por vez (listas, array, coordenadas)
# TODO: Permitir mudar o interpolador para momentos pontos diferentes, ou implementar um
#       jeito de unir uma animacao na outra de maneira lisa, e cada uma podendo usar um interpolador
# TODO: Fazer arquivo com exemplos
# TODO: Fazer testes unitários (o que acontece se a duracao não bate com os key-frames? e se o primeiro
#       key-frame não for 0?)

class Animotion:
    def __init__(self, duration: float, update_function: Callable, interpolator: str = "linear", *args, **kwargs):
        """
        Classe para animar valores com base em keyframes.

        :param duration: Duração total da animação em segundos.
        :param update_function: Função chamada em cada step da animação, recebendo o valor interpolado.
        :param interpolator: Nome da função de interpolação a ser usada ("linear", "ease_in", "ease_out", "ease_in_out").
        """
        self.duration = duration
        self.update_function = update_function
        self.keyframes: List[Tuple[float, float]] = []  # Lista de keyframes (tempo, valor)
        self.interpolator = self.get_interpolator(interpolator)
        self.args = args
        self.kwargs = kwargs

    def get_interpolator(self, interpolator_name: str) -> Callable[[float, float, float], float]:
        """
        Retorna a função de interpolação com base no nome fornecido.
        :param interpolator_name: Nome da função de interpolação.
        :return: Função de interpolação correspondente.
        """
        interpolators = {
            "linear": self.linear_interpolation,
            "ease_in": self.ease_in,
            "ease_out": self.ease_out,
            "ease_in_out": self.ease_in_out
        }
        return interpolators.get(interpolator_name, self.linear_interpolation)

    def add_keyframe(self, time_point: float, value: float):
        """
        Adiciona um keyframe à animação.
        :param time_point: Ponto no tempo (em segundos) para o keyframe.
        :param value: Valor desejado no keyframe.
        """
        self.keyframes.append((time_point, value))
        self.keyframes.sort()  # Ordenar os keyframes pelo tempo

    def run(self):
        """
        Executa a animação, interpolando os valores entre os keyframes.
        """
        if len(self.keyframes) < 2:
            print("É necessário ter pelo menos dois keyframes para uma animação.")
            return

        # Garantir que exista um keyframe no tempo 0
        if self.keyframes[0][0] != 0:
            self.keyframes.insert(0, (0, self.keyframes[0][1]))

        start_time = time.time()

        # Percorrer os keyframes
        for i in range(len(self.keyframes) - 1):
            t0, v0 = self.keyframes[i]
            t1, v1 = self.keyframes[i + 1]
            frame_duration = t1 - t0

            while True:
                elapsed = time.time() - (start_time + t0)
                if elapsed > frame_duration:
                    break
                if elapsed + t0 > self.duration:
                    time.sleep(self.duration - (elapsed + t0))  # Espera até o final da duração
                    return
                
                t = min(1, max(0, elapsed / frame_duration))  # Garantir t entre 0 e 1
                interpolated_value = self.interpolator(v0, v1, t)
                self.update_function(interpolated_value, *self.args, **self.kwargs)
                time.sleep(0.05)  # Pequeno delay para suavizar a animação

        # Garantir que o último valor seja definido, se dentro da duração
        if self.keyframes[-1][0] <= self.duration:
            self.update_function(self.keyframes[-1][1], *self.args, **self.kwargs)

        # Continuar até o final da duração se necessário
        if time.time() - start_time < self.duration:
            time.sleep(self.duration - (time.time() - start_time))

    def run_in_thread(self):
        """
        Executa a animação em uma thread separada.
        """
        animation_thread = threading.Thread(target=self.run)
        animation_thread.start()

    @staticmethod
    def linear_interpolation(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação linear entre dois valores.
        :param start_value: Valor inicial.
        :param end_value: Valor final.
        :param t: Proporção entre 0 e 1.
        :return: Valor interpolado.
        """
        return start_value + t * (end_value - start_value)

    @staticmethod
    def ease_in(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação ease-in, que começa lenta e acelera.
        :param start_value: Valor inicial.
        :param end_value: Valor final.
        :param t: Proporção entre 0 e 1.
        :return: Valor interpolado.
        """
        return start_value + (end_value - start_value) * (t ** 2)

    @staticmethod
    def ease_out(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação ease-out, que começa rápida e desacelera.
        :param start_value: Valor inicial.
        :param end_value: Valor final.
        :param t: Proporção entre 0 e 1.
        :return: Valor interpolado.
        """
        return start_value + (end_value - start_value) * (1 - (1 - t) ** 2)

    @staticmethod
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