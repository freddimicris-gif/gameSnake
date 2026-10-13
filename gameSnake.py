# gameSnake.py
import tkinter as tk
import sys
import copy

# Variável global oculta para armazenar o caractere ou nome da tecla pressionada
_tecla_atual = ""
_personagens = {}

def loadTexture(caminho_arquivo):
    """Carrega um arquivo PNG nativamente e o prepara como textura."""
    # O PhotoImage do Tkinter abre PNGs diretamente
    return tk.PhotoImage(file=caminho_arquivo)

def createNewWindow(largura, altura, titulo):
    """Cria a janela e liga o evento do teclado automaticamente."""
    janela = tk.Tk()
    janela.title(titulo)
    janela.resizable(False, False)
    
    canvas = tk.Canvas(janela, bg="black", width=largura, height=altura)
    canvas.pack()
    janela.canvas = canvas
    
    # Ativa a escuta do teclado na janela
    janela.bind("<Key>", KeyPressedIs)
    
    return janela

def KeyPressedIs(tecla_alvo, evento):
    global _tecla_atual
    # evento.char guarda letras (ex: 'k', 'w'). 
    # Se for uma tecla especial (setas, enter), usamos evento.keysym
    _tecla_atual = evento.char if evento.char else evento.keysym

    """
    Verifica se a tecla guardada corresponde à tecla que o utilizador passou.
    Retorna True ou False.
    """
    # .lower() garante que funciona quer o utilizador verifique "k" ou "K"
    return _tecla_atual.lower() == tecla_alvo.lower()

def drawBlock(jogo, posicao, textura_ou_cor, tamanho=20):
    """Desenha um bloco que pode ser uma cor string ("red") ou uma textura PNG."""
    x, y = posicao
    
    # Se for uma textura carregada pelo PhotoImage
    if isinstance(textura_ou_cor, tk.PhotoImage):
        # O create_image posiciona pelo centro por padrão, 
        # usar anchor="nw" faz alinhar pelo canto superior esquerdo (igual ao retângulo)
        jogo.canvas.create_image(x, y, image=textura_ou_cor, anchor="nw")
    else:
        # Se for apenas uma cor normal (ex: "green", "red")
        jogo.canvas.create_rectangle(x, y, x + tamanho, y + tamanho, fill=textura_ou_cor, outline="")

def lineText(jogo, texto, posicao, cor="white", tamanho=16):
    """
    Desenha uma linha de texto no ecrã de forma simples.
    Usa anchor="nw" para alinhar a partir do canto superior esquerdo da coordenada.
    """
    x, y = posicao
    # Criamos o texto usando a fonte padrão do sistema (Arial ou Helvetica)
    jogo.canvas.create_text(
        x, y, 
        text=texto, 
        fill=cor, 
        font=("Arial", tamanho, "bold"), 
        anchor="nw"
    )
def checkCollision(posicao1, posicao2):
    """Retorna True se duas posições (x, y) forem exatamente iguais."""
    return posicao1 == posicao2

def checkWallCollision(posicao, largura_max, altura_max):
    """Retorna True se uma posição (x, y) sair dos limites do ecrã."""
    x, y = posicao
    return x < 0 or x >= largura_max or y < 0 or y >= altura_max

def drawCircle(jogo, centro, raio, cor):
    """
    Desenha um círculo perfeito informando apenas o centro (x, y) e o raio.
    Resolve a matemática confusa do create_oval do Tkinter de forma invisível.
    """
    x, y = centro
    # Calcula os cantos superior esquerdo e inferior direito do quadrado que envolve o círculo
    x0 = x - raio
    y0 = y - raio
    x1 = x + raio
    y1 = y + raio
    
    # Desenha o círculo no canvas
    jogo.canvas.create_oval(x0, y0, x1, y1, fill=cor, outline="")
if sys.platform == "win32":
    import winsound
    def playSound(arquivo_wav):
        """Toca um ficheiro de som .wav em segundo plano (apenas Windows)."""
        winsound.PlaySound(arquivo_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
else:
    # Se estiver no Linux/Mac, usamos comandos nativos do sistema para não dar erro
    import os
    def playSound(arquivo_wav):
        """Toca um ficheiro de som em segundo plano no Linux/Mac."""
        if sys.platform == "darwin":  # Mac
            os.system(f"afplay {arquivo_wav} &")
        else:  # Linux
            os.system(f"aplay {arquivo_wav} &")

def createPerson(nome, posicao, textura_ou_cor):
    """Cria um personagem na memória com um nome único."""
    _personagens[nome] = {
        "posicao": list(posicao),
        "visual": textura_ou_cor
    }

def ClonePerson(nome_original, nome_novo):
    """
    Uma linha para clonar! Copia a posição e visual do original 
    para um novo personagem independente.
    """
    if nome_original in _personagens:
        _personagens[nome_novo] = copy.deepcopy(_personagens[nome_original])

def DeletPerson(nome):
    """Uma linha para deletar! Remove o personagem do jogo por completo."""
    if nome in _personagens:
        del _personagens[nome]

def movePerson(nome, dx, dy):
    """Move um personagem específico pelas coordenadas."""
    if nome in _personagens:
        _personagens[nome]["posicao"][0] += dx
        _personagens[nome]["posicao"][1] += dy

def drawAllPersons(jogo, tamanho=20):
    """Desenha automaticamente todos os personagens ativos no ecrã."""
    for nome, dados in _personagens.items():
        x, y = dados["posicao"]
        visual = dados["visual"]
        
        if isinstance(visual, tk.PhotoImage):
            jogo.canvas.create_image(x, y, image=visual, anchor="nw")
        else:
            jogo.canvas.create_rectangle(x, y, x + tamanho, y + tamanho, fill=visual, outline="")
