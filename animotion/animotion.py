import time
import threading
from typing import List, Tuple, Callable, Union
import matplotlib.pyplot as plt

# TODO: Implementar suporte a diferentes tipos de interpoladores fornecidos dinamicamente
# TODO: Permitir mudar o interpolador para pontos diferentes
# TODO: Modo visualize não demorar o tempo de animação para mostrar o gráfico
# TODO: Implementar o bake animation (pre-renderizar a animacao)
# TODO: Fazer arquivo com exemplos
# TODO: Fazer testes unitários

class Animotion:
    def __init__(self, duration: float, update_function: Callable, interpolator: str = "linear",
                 mode: str = "deploy", delta_t: float = 0.05, value_names: List[str] = None,
                 stop_event: threading.Event = None, *args, **kwargs):
        """
        Classe para animar valores com base em keyframes.

        :param duration: Duração total da animação em segundos.
        :param update_function: Função chamada em cada step da animação, recebendo os valores interpolados.
        :param interpolator: Nome da função de interpolação a ser usada ("linear", "ease_in", "ease_out", "ease_in_out").
        :param mode: Modo de execução, pode ser "deploy" ou "visualize".
        :param delta_t: Intervalo de tempo entre cada interpolação, em segundos.
        :param value_names: Lista de nomes dos valores para usar no gráfico de visualização.
        :param stop_event: Evento para sinalizar a parada da animação.
        """
        self.duration = duration
        self.update_function = update_function
        self.keyframes: List[Tuple[float, Union[float, str, Tuple[Union[float, str], ...]]]] = []  # Lista de keyframes (tempo, valores)
        self.interpolator = self.get_interpolator(interpolator)
        self.mode = mode
        self.delta_t = delta_t
        self.args = args
        self.kwargs = kwargs
        self.value_names = value_names
        self.tempo_pontos = []
        self.valores_pontos = []
        self.stop_event = stop_event

    def get_interpolator(self, interpolator_name: str) -> Callable[[float, float, float], float]:
        """
        Retorna a função de interpolação com base no nome fornecido.
        """
        interpolators = {
            "linear": self.linear_interpolation,
            "ease_in": self.ease_in,
            "ease_out": self.ease_out,
            "ease_in_out": self.ease_in_out
        }
        return interpolators.get(interpolator_name, self.linear_interpolation)

    def add_keyframe(self, time_point: float, values: Union[float, str, Tuple[Union[float, str], ...]]):
        """
        Adiciona um keyframe à animação.
        """
        if isinstance(values, (list, tuple)):
            values = tuple(values)
        self.keyframes.append((time_point, values))
        self.keyframes.sort()  # Ordenar os keyframes pelo tempo

    def add_keyframes(self, keyframes: List[Tuple[float, Union[float, str, Tuple[Union[float, str], ...]]]]):
        """
        Adiciona múltiplos keyframes à animação.
        """
        for time_point, values in keyframes:
            self.add_keyframe(time_point, values)

    def run(self):
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

            # Se o frame_duration for negativo ou zero, pular para o próximo keyframe
            if frame_duration <= 0:
                continue

            while True:
                # Verificar se o evento de parada foi sinalizado
                if self.stop_event and self.stop_event.is_set():
                    print("Animação interrompida.")
                    return

                current_time = time.time()
                total_elapsed = current_time - start_time

                # Interromper a animação se a duração for atingida
                if total_elapsed >= self.duration:
                    # Calcular t para o ponto exato da duração
                    overrun = total_elapsed - self.duration
                    elapsed_in_frame = (current_time - overrun) - (start_time + t0)
                    t = min(1, max(0, elapsed_in_frame / frame_duration))
                    interpolated_values = self.interpolate_values(v0, v1, t)
                    if self.mode == "deploy":
                        self.update_function(*interpolated_values, *self.args, **self.kwargs)
                    elif self.mode == "visualize":
                        self.tempo_pontos.append(self.duration)
                        self.valores_pontos.append(interpolated_values)
                    return

                elapsed_in_frame = current_time - (start_time + t0)

                if elapsed_in_frame > frame_duration:
                    break  # Passar para o próximo keyframe

                t = min(1, max(0, elapsed_in_frame / frame_duration))  # Garantir t entre 0 e 1
                interpolated_values = self.interpolate_values(v0, v1, t)
                if self.mode == "deploy":
                    self.update_function(*interpolated_values, *self.args, **self.kwargs)
                elif self.mode == "visualize":
                    self.tempo_pontos.append(total_elapsed)
                    self.valores_pontos.append(interpolated_values)
                time.sleep(self.delta_t)

        # Se ainda não atingiu a duração, aguardar ou atualizar até o fim
        while True:
            if self.stop_event and self.stop_event.is_set():
                print("Animação interrompida.")
                return

            total_elapsed = time.time() - start_time

            if total_elapsed >= self.duration:
                # Definir o último valor
                if self.mode == "deploy":
                    self.update_function(*self.keyframes[-1][1], *self.args, **self.kwargs)
                elif self.mode == "visualize":
                    self.tempo_pontos.append(self.duration)
                    self.valores_pontos.append(self.keyframes[-1][1])
                break

            if self.mode == "deploy":
                self.update_function(*self.keyframes[-1][1], *self.args, **self.kwargs)
            elif self.mode == "visualize":
                self.tempo_pontos.append(total_elapsed)
                self.valores_pontos.append(self.keyframes[-1][1])
            time.sleep(self.delta_t)

        # Gerar gráfico se estiver no modo "visualize"
        if self.mode == "visualize":
            self.plot_visualization()

    def interpolate_values(self, v0: Union[float, str, Tuple[Union[float, str], ...]],
                           v1: Union[float, str, Tuple[Union[float, str], ...]], t: float) -> Tuple:
        """
        Interpola valores entre v0 e v1.
        """
        if isinstance(v0, (float, int)) and isinstance(v1, (float, int)):
            return (self.interpolator(v0, v1, t),)
        elif isinstance(v0, str) and isinstance(v1, str):
            return (v0 if t < 1.0 else v1,)
        elif isinstance(v0, (tuple, list)) and isinstance(v1, (tuple, list)):
            interpolated = []
            for val0, val1 in zip(v0, v1):
                if isinstance(val0, (float, int)) and isinstance(val1, (float, int)):
                    interpolated.append(self.interpolator(val0, val1, t))
                elif isinstance(val0, str) and isinstance(val1, str):
                    interpolated.append(val0 if t < 1.0 else val1)
                else:
                    raise ValueError("Valores incompatíveis para interpolação.")
            return tuple(interpolated)
        else:
            raise ValueError("Valores incompatíveis para interpolação.")

    def run_in_thread(self):
        """
        Executa a animação em uma thread separada.
        """
        animation_thread = threading.Thread(target=self.run)
        animation_thread.start()
        return animation_thread

    def plot_visualization(self):
        """
        Gera um gráfico dos valores interpolados ao longo do tempo.
        """
        if not self.tempo_pontos or not self.valores_pontos:
            print("Nenhum dado disponível para visualização.")
            return

        plt.figure(figsize=(10, 6))
        num_values = len(self.valores_pontos[0])
        for i in range(num_values):
            valores = [val[i] if isinstance(val, tuple) else val for val in self.valores_pontos]
            label = self.value_names[i] if self.value_names and i < len(self.value_names) else f'Valor {i + 1}'
            plt.plot(self.tempo_pontos, valores, label=label)

        plt.xlabel('Tempo (s)')
        plt.ylabel('Valores Interpolados')
        plt.title('Visualização da Animação')
        plt.legend()
        plt.show()

    @staticmethod
    def linear_interpolation(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação linear entre dois valores.
        """
        return start_value + t * (end_value - start_value)

    @staticmethod
    def ease_in(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação ease-in.
        """
        return start_value + (end_value - start_value) * (t ** 2)

    @staticmethod
    def ease_out(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação ease-out.
        """
        return start_value + (end_value - start_value) * (1 - (1 - t) ** 2)

    @staticmethod
    def ease_in_out(start_value: float, end_value: float, t: float) -> float:
        """
        Interpolação ease-in-out.
        """
        if t < 0.5:
            return start_value + (end_value - start_value) * (2 * t ** 2)
        else:
            return start_value + (end_value - start_value) * (1 - (-2 * t + 2) ** 2 / 2)
