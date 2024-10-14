# Exemplo de uso da biblioteca Animotion
from animotion import Animotion
import time

# Função de atualização que será chamada durante a animação
def update_function(*values):
    print(f"Valores interpolados: {values}")

# Criar uma instância da classe Animotion com duração de 10 segundos
animacao = Animotion(10, update_function, interpolator="linear")

# Adicionar keyframes para animar valores múltiplos, incluindo floats e strings
animacao.add_keyframe(0, (0.0, "bravo"))  # Tempo 0s, valores: 0.0 e "bravo"
animacao.add_keyframe(5, (100.0, "neutro"))  # Tempo 5s, valores: 100.0 e "neutro"
animacao.add_keyframe(10, (200.0, "feliz"))  # Tempo 10s, valores: 200.0 e "feliz"

# Executar a animação
animacao.run()

print("Animação concluída.")