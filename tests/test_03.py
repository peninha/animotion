# Exemplo de uso da biblioteca Animotion
from animotion import Animotion
import time
import matplotlib.pyplot as plt

# Função de atualização que será chamada durante a animação
def update_function(mao, olho, sobran_dir, sobran_esq, boca, emocao):
    #print(f"mao {mao:.2f}, olho {olho:.2f}, sobran_dir {sobran_dir:.2f}, sobran_esq {sobran_esq:.2f}, boca {boca:.2f}, emocao {emocao}")
    print(f"mao {mao}, olho {olho}, sobran_dir {sobran_dir}, sobran_esq {sobran_esq}, boca {boca}, emocao {emocao}")

# Criar uma instância da classe Animotion com duração de 10 segundos
animacao = Animotion(5, update_function, interpolator="ease_in_out", mode="visualize", delta_t=0.05)

# Adicionar keyframes para animar valores múltiplos, incluindo floats e strings
animacao.add_keyframe(0, (0, 50, 30, 40, 0, "bravo"))  # Tempo 0s, valores: 0.0 e "bravo"
animacao.add_keyframe(5, (100, 80, 0, 0, 50, "neutro"))  # Tempo 5s, valores: 100.0 e "neutro"
#animacao.add_keyframe(10, (200, 100, 30, 0, 0, "feliz"))  # Tempo 10s, valores: 200.0 e "feliz"

# Executar a animação
animacao.run()


print("Animação concluída.")