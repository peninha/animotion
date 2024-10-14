from animotion import Animotion
import numpy as np
import time

# Função de atualização que será chamada durante a animação
def update_function(x, y, emotion):
    print(f"x: {x}, y: {y}, emotion: {emotion}")

# Criar uma instância da classe Animotion
animacao = Animotion(
    duration=5,
    update_function=update_function,
    interpolator="ease_in_out",
    mode="visualize",
    delta_t=0.1,
    value_names=["Posição X", "Posição Y", "Emoção"]
)

# Adicionar keyframes para a animação
animacao.add_keyframe(0, ((0, 0), "neutro"))
animacao.add_keyframe(5, ((100, 50), "feliz"))

# Executar a animação
animacao.run()
