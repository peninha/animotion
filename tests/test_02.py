# Exemplo de uso da biblioteca Animotion
from animotion import Animotion
import time
import matplotlib.pyplot as plt

# Listas para armazenar os valores interpolados para plotagem
tempo_pontos = []
mao_pontos = []
olho_pontos = []
sobran_dir_pontos = []
sobran_esq_pontos = []
boca_pontos = []
emocao_pontos = []

# Função de atualização que será chamada durante a animação
def update_function(mao, olho, sobran_dir, sobran_esq, boca, emocao):
    print(f"mao {mao:.2f}, olho {olho:.2f}, sobran_dir {sobran_dir:.2f}, sobran_esq {sobran_esq:.2f}, boca {boca:.2f}, emocao {emocao}")
    # Armazenar os valores para plotagem
    tempo_pontos.append(time.time())
    mao_pontos.append(mao)
    olho_pontos.append(olho)
    sobran_dir_pontos.append(sobran_dir)
    sobran_esq_pontos.append(sobran_esq)
    boca_pontos.append(boca)
    emocao_pontos.append(emocao)

# Criar uma instância da classe Animotion com duração de 10 segundos
animacao = Animotion(10, update_function, interpolator="linear")

# Adicionar keyframes para animar valores múltiplos, incluindo floats e strings
animacao.add_keyframe(0, (0, 50, 30, 40, 0, "bravo"))  # Tempo 0s, valores: 0.0 e "bravo"
animacao.add_keyframe(5, (100, 80, 0, 0, 50, "neutro"))  # Tempo 5s, valores: 100.0 e "neutro"
animacao.add_keyframe(10, (200, 100, 30, 0, 0, "feliz"))  # Tempo 10s, valores: 200.0 e "feliz"

# Executar a animação
animacao.run()

# Ajustar os tempos para iniciar em 0 (normalizar)
tempo_inicial = tempo_pontos[0]
tempo_pontos = [t - tempo_inicial for t in tempo_pontos]

# Plotar os gráficos dos valores interpolados
plt.figure(figsize=(10, 8))

plt.subplot(3, 2, 1)
plt.plot(tempo_pontos, mao_pontos, label='Mão')
plt.xlabel('Tempo (s)')
plt.ylabel('Mão')
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(tempo_pontos, olho_pontos, label='Olho')
plt.xlabel('Tempo (s)')
plt.ylabel('Olho')
plt.legend()

plt.subplot(3, 2, 3)
plt.plot(tempo_pontos, sobran_dir_pontos, label='Sobrancelha Direita')
plt.xlabel('Tempo (s)')
plt.ylabel('Sobrancelha Direita')
plt.legend()

plt.subplot(3, 2, 4)
plt.plot(tempo_pontos, sobran_esq_pontos, label='Sobrancelha Esquerda')
plt.xlabel('Tempo (s)')
plt.ylabel('Sobrancelha Esquerda')
plt.legend()

plt.subplot(3, 2, 5)
plt.plot(tempo_pontos, boca_pontos, label='Boca')
plt.xlabel('Tempo (s)')
plt.ylabel('Boca')
plt.legend()

plt.tight_layout()
plt.show()

print("Animação concluída.")