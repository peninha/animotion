from animotion import Animotion
import time

# Função de atualização que será chamada durante a animação
def update_function(x, y, emotion):
    print(f"x: {x}, y: {y}, emotion: {emotion}")

# Criar uma instância da classe Animotion
animacao = Animotion(
    update_function=update_function,
    interpolator="ease_in_out",
    mode="visualize",
    delta_t=0.1,
    value_names=["Posição X", "Posição Y", "Emoção"],
    start_time=1
)

# Adicionar keyframes para a animação
animacao.add_keyframe(0, (0, 0, "neutro"))
animacao.add_keyframe(2, (100, 50, "feliz"))
animacao.add_keyframe(4, (200, 100, "triste"))

# Executar a animação
animacao.run()
