# /animotion/animotion.py
import time
import threading
from typing import List, Tuple, Callable
from .interpolators import linear_interpolation, ease_in, ease_out, ease_in_out

class Animotion:
    def __init__(self, duration: float, update_function: Callable[[float], None], interpolator: Callable = linear_interpolation):
        """
        Classe para animar valores com base em keyframes.

        :param duration: Duração total da animação em segundos.
        :param update_function: Função chamada em cada step da animação, recebendo o valor interpolado.
        :param interpolator: Função de interpolação a ser usada.
        """
        self.duration = duration
        self.update_function = update_function
        self.keyframes: List[Tuple[float, float]] = []  # Lista de keyframes (tempo, valor)
        self.interpolator = interpolator

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
                
                t = min(1, max(0, elapsed / frame_duration))  # Garantir t entre 0 e 1
                interpolated_value = self.interpolator(v0, v1, t)
                self.update_function(interpolated_value)
                time.sleep(0.05)  # Pequeno delay para suavizar a animação

        # Garantir que o último valor seja definido
        self.update_function(self.keyframes[-1][1])

    def run_in_thread(self):
        """
        Executa a animação em uma thread separada.
        """
        animation_thread = threading.Thread(target=self.run)
        animation_thread.start()