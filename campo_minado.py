import tkinter as tk
import numpy as np
from functools import partial
from random import randint

#Definimos a classe Campo, que é uma extensão da classe Button da biblioteca tkinter. Para criar a classe Campo, nós
#adicionamos três atributos booleanos: 'mina', que serve para dizer se o campo contem ou não uma mina, 'marcado' para
#dizer se o campo foi ou não marcado pelo usuario e vizinhos para dizer quantos vizinhos daquele campo contem uma minh.
#Além disso fixamos o tamanho do botão como sendo 14x15 para que nãohouvesse problemas de dimensionamento quando os
# botões virassem numeros
class Campo(tk.Button):
    def __init__(self, cavado=False, mina=False, marcado=False, vizinhos=0, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.cavado = cavado
        self.mina = mina
        self.marcado = marcado
        self.vizinhos = vizinhos
        self['width'] = 14
        self['height'] = 15


# Recebe o tamanho lateral N do jogo e cria uma janela (cujo tamanho depende de N) e um um tabuleiro (que é uma matriz
# de botões, inicialmente vazia). Além disso ele também cria um mostrador que indica quantas marcações ainda podem
# ser feitas
def montar_jogo(N):
    tabuleiro = np.empty(shape=(N, N), dtype=Campo)

    janela = tk.Tk()
    if N<8:
        janela.geometry(str(180) + 'x' + str(21 * N + 50))
    else:
        janela.geometry(str(20 * N + 40) + 'x' + str(21 * N + 50))
    janela.resizable(False, False)
    janela.title('Campo Minado')

    espaco1 = tk.Frame(janela, height=20, width=20)
    espaco1.grid(row=1, column=0, rowspan=N, sticky='ns')
    espaco2 = tk.Frame(janela, height=20, width=20)
    espaco2.grid(row=1, column=N + 1, rowspan=N, sticky='ns')

    mostrador = tk.Label(janela, text='Há '+str(n_minas)+' marcações disponíveis')
    mostrador.grid(row=0, column=1, columnspan=N, sticky='we')

    menu = tk.Button(janela, text='Mudar Tabuleiro')
    menu.bind('<Button-1>', partial(abrir_menu, janela))
    menu.grid(row=N + 1, column=1, columnspan=N, sticky='we')

    return tabuleiro, janela, mostrador


# Preenche o tabuleiro, criando botões em todas as casas do tabuleiro, alem disso, ele chama a função
# preencher_campo, que cria as minas
def inicializar():
    for i in range(N):
        for j in range(N):
            tabuleiro[i][j] = Campo(master=janela, bitmap="gray50")
            tabuleiro[i][j].bind('<Button-1>', partial(cavar, tabuleiro[i][j], i, j))
            tabuleiro[i][j].bind('<Button-3>', partial(marcar, tabuleiro[i][j]))
            tabuleiro[i][j].grid(row=i+1, column=j+1)
    return preencher_campo(tabuleiro, n_minas)


# transforma "n_minas" botões aleatorios em minas, atualiza o valor da propriedade "vizinhos" das casas adjacentes
# e retorna uma lista com as coordenadas de todas as minas(lista_de_minas)
def preencher_campo(tabuleiro, n_minas):
    contador = 0
    lista_de_minas = []
    while contador < n_minas:
        linha = randint(0, N-1)
        coluna = randint(0, N-1)
        if not tabuleiro[linha][coluna].mina:
            tabuleiro[linha][coluna].mina = True
            lista_de_minas.append((linha, coluna))
            contador += 1

    for linha,coluna in lista_de_minas:
        if linha == 0:  # borda superior do jogo
            if coluna == 0:  # canto superior esquerdo do jogo
                tabuleiro[linha, coluna + 1].vizinhos += 1
                tabuleiro[linha + 1, coluna + 1].vizinhos += 1
                tabuleiro[linha + 1, coluna].vizinhos += 1

            elif coluna == N - 1:  # canto superior direito do jogo
                tabuleiro[linha, coluna - 1].vizinhos += 1
                tabuleiro[linha + 1, coluna - 1].vizinhos += 1
                tabuleiro[linha + 1, coluna].vizinhos += 1

            else:
                tabuleiro[linha, coluna - 1].vizinhos += 1
                tabuleiro[linha + 1, coluna - 1].vizinhos += 1
                tabuleiro[linha + 1, coluna].vizinhos += 1
                tabuleiro[linha + 1, coluna + 1].vizinhos += 1
                tabuleiro[linha, coluna + 1].vizinhos += 1

        elif linha == N - 1:  # borda inferior do jogo
            if coluna == 0:  # canto inferior esquerdo do jogo
                tabuleiro[linha - 1, coluna].vizinhos += 1
                tabuleiro[linha - 1, coluna + 1].vizinhos += 1
                tabuleiro[linha, coluna + 1].vizinhos += 1

            elif coluna == N - 1:  # canto inferior direito do jogo
                tabuleiro[linha - 1, coluna].vizinhos += 1
                tabuleiro[linha - 1, coluna - 1].vizinhos += 1
                tabuleiro[linha, coluna - 1].vizinhos += 1

            else:
                tabuleiro[linha, coluna - 1].vizinhos += 1
                tabuleiro[linha - 1, coluna - 1].vizinhos += 1
                tabuleiro[linha - 1, coluna].vizinhos += 1
                tabuleiro[linha - 1, coluna + 1].vizinhos += 1
                tabuleiro[linha, coluna + 1].vizinhos += 1

        elif coluna == 0:  # borda esquerda do jogo
            tabuleiro[linha - 1, coluna].vizinhos += 1
            tabuleiro[linha - 1, coluna + 1].vizinhos += 1
            tabuleiro[linha, coluna + 1].vizinhos += 1
            tabuleiro[linha + 1, coluna + 1].vizinhos += 1
            tabuleiro[linha + 1, coluna].vizinhos += 1

        elif coluna == N - 1:  # borda direita do jogo
            tabuleiro[linha - 1, coluna].vizinhos += 1
            tabuleiro[linha - 1, coluna - 1].vizinhos += 1
            tabuleiro[linha, coluna - 1].vizinhos += 1
            tabuleiro[linha + 1, coluna - 1].vizinhos += 1
            tabuleiro[linha + 1, coluna].vizinhos += 1

        else:
            tabuleiro[linha + 1, coluna - 1].vizinhos += 1
            tabuleiro[linha + 1, coluna].vizinhos += 1
            tabuleiro[linha + 1, coluna + 1].vizinhos += 1
            tabuleiro[linha, coluna + 1].vizinhos += 1
            tabuleiro[linha - 1, coluna + 1].vizinhos += 1
            tabuleiro[linha - 1, coluna].vizinhos += 1
            tabuleiro[linha - 1, coluna - 1].vizinhos += 1
            tabuleiro[linha, coluna - 1].vizinhos += 1

    return lista_de_minas


# destrói o botao que foi cavado e, no lugar dele, põe uma Label com o numero de minas adjacentes. Caso o campo
# pressionado seja uma minha, ele chama a função destruição_total(). Além disso, ao final de cada "cavada" num campo
# que não seja uma mina, chama-se a função check_vitoria() para conferir se o jogador ganhou o jogo
def cavar(botao,linha,coluna, evento=None):
    if type(botao) is Campo: #checa se o botao passado é mesmo do tipo Campo, pois como ao cavar nós destruimos o botao e
                       # criamos uma Label e ao longo do programa é possivel cavar o mesmo campo varias vezes, essa
                       # verificação se faz necesaria
        if not botao.marcado:
            if not botao.mina:
                if botao.vizinhos != 0:
                    vizinhos = botao.vizinhos
                    botao.destroy()
                    n_campos.set(n_campos.get()-1)
                    tabuleiro[linha, coluna] = tk.Label(janela, text=str(vizinhos), width=2, height=1)
                    tabuleiro[linha, coluna].grid(row=linha+1, column=coluna+1)
                    check_vitoria()
                else:
                    botao.destroy()
                    n_campos.set(n_campos.get() - 1)
                    tabuleiro[linha, coluna] = tk.Label(janela, text=' ', width=2, height=1)
                    tabuleiro[linha, coluna].grid(row=linha + 1, column=coluna + 1)
                    check_vitoria()
                    if linha == 0: #borda superior do jogo
                        if coluna == 0: #canto superior esquerdo do jogo
                            cavar(tabuleiro[linha, coluna+1], linha, coluna+1)
                            cavar(tabuleiro[linha+1, coluna], linha+1, coluna)

                        elif coluna == N-1: #canto superior direito do jogo
                            cavar(tabuleiro[linha, coluna - 1], linha, coluna - 1)
                            cavar(tabuleiro[linha + 1, coluna], linha + 1, coluna)

                        else:
                            cavar(tabuleiro[linha, coluna - 1], linha, coluna - 1)
                            cavar(tabuleiro[linha + 1, coluna], linha + 1, coluna)
                            cavar(tabuleiro[linha, coluna + 1], linha, coluna + 1)

                    elif linha == N-1:#borda inferior do jogo
                        if coluna == 0: #canto inferior esquerdo do jogo
                            cavar(tabuleiro[linha - 1, coluna], linha - 1, coluna)
                            cavar(tabuleiro[linha, coluna + 1], linha, coluna + 1)

                        elif coluna == N-1: #canto inferior direito do jogo
                            cavar(tabuleiro[linha - 1, coluna], linha - 1, coluna)
                            cavar(tabuleiro[linha, coluna - 1], linha, coluna - 1)

                        else:
                            cavar(tabuleiro[linha, coluna - 1], linha, coluna - 1)
                            cavar(tabuleiro[linha - 1, coluna], linha - 1, coluna)
                            cavar(tabuleiro[linha, coluna + 1], linha, coluna + 1)

                    elif coluna == 0: #borda esquerda do jogo
                        cavar(tabuleiro[linha - 1, coluna], linha - 1, coluna)
                        cavar(tabuleiro[linha, coluna + 1], linha, coluna + 1)
                        cavar(tabuleiro[linha + 1, coluna], linha + 1, coluna)

                    elif coluna == N-1: #borda direita do jogo
                        cavar(tabuleiro[linha - 1, coluna], linha - 1, coluna)
                        cavar(tabuleiro[linha, coluna - 1], linha, coluna - 1)
                        cavar(tabuleiro[linha + 1, coluna], linha + 1, coluna)

                    else:
                        cavar(tabuleiro[linha + 1, coluna], linha + 1, coluna)
                        cavar(tabuleiro[linha, coluna + 1], linha, coluna + 1)
                        cavar(tabuleiro[linha - 1, coluna], linha - 1, coluna)
                        cavar(tabuleiro[linha, coluna - 1], linha, coluna - 1)

            else:
                botao.destroy()
                tabuleiro[linha, coluna] = tk.Label(janela, text='M', width=2, height=1)
                tabuleiro[linha, coluna].grid(row=linha + 1, column=coluna + 1)
                destruicao_total()


# destroi todos os campos, substituindo-os por Labels mostrando quantos vizinhos daquele campo eram minas, ou a letra
# M, caso o campo fosse uma minha
def destruicao_total():
    for i in range(N):
        for j in range(N):
            if type(tabuleiro[i][j]) is Campo:
                if tabuleiro[i][j].mina:
                    tabuleiro[i][j].destroy()
                    tabuleiro[i, j] = tk.Label(janela, text='M', width=2, height=1)
                    tabuleiro[i, j].grid(row=i + 1, column=j + 1)
                else:
                    vizinhos = tabuleiro[i][j].vizinhos
                    tabuleiro[i][j].destroy()
                    tabuleiro[i][j] = tk.Label(janela, text=str(vizinhos), width=2, height=1)
                    tabuleiro[i][j].grid(row=i + 1, column=j + 1)


# marca um campo como sendo uma possivel mina, ao marcar o campo, é atualizado o valor do contador de marcações,
# além disso, sempre que o marcador é zerado, chama-se a função check_vitoria() para conferir se o jogador venceu o jogo
def marcar(botao, evento):
    if botao.marcado:
        botao['bitmap'] = "gray50"
        botao.marcado = False
        n_marcadores.set(n_marcadores.get() + 1)
        mostrador['text'] = 'Há ' + str(n_marcadores.get()) + ' marcações disponíveis'
    elif n_marcadores.get() > 0:
        botao['bitmap'] = "questhead"
        botao.marcado = True
        n_marcadores.set(n_marcadores.get()-1)
        mostrador['text'] = 'Há '+str(n_marcadores.get())+' marcações disponíveis'
        if n_marcadores.get() == 0:
            check_vitoria()


# Confere se todas as condições de vitoria(todas as minas marcadas e todos os campos que não são minas cavados) foram
# atendidas, caso tenham sido, ela chama a função vitoria()
def check_vitoria():
    condicao1 = True
    condicao2 = n_campos.get() == n_minas
    if condicao2:
        for i, j in lista_de_minas:
            if not tabuleiro[i, j].marcado:
                condicao1 = False

    if condicao1 and condicao2:
        vitoria()


# Abre uma janela informando que o jogador venceu e lhe dá a opção de jogar novamente ou de sair do jogo
def vitoria():
    janela_vitoria = tk.Toplevel(janela)
    janela_vitoria.geometry('200x50')
    janela_vitoria.protocol('WM_DELETE_WINDOW', janela.destroy)
    mensagem_vitoria = tk.Label(janela_vitoria, text='Parabens, voce venceu!!')
    mensagem_vitoria.grid(row=0, column=0, columnspan=3)

    sair = tk.Button(janela_vitoria, text='sair', command=janela.destroy, width=10)
    sair.grid(row=1, column=0, columnspan=1, sticky='we')

    replay = tk.Button(janela_vitoria, text='jogar novamente', command=jogar_denovo)
    replay.grid(row=1, column=2, columnspan=2, sticky='we')

    janela_vitoria.mainloop()


# Defini a variavel menu_aberto como sendo True e destroi a janela do jogo, como a variavel menu_aberto foi definida
# como True, o programa vai chamar a função menu_inicial()
def abrir_menu(janela, evento):
    menu_aberto.set(True)
    janela.destroy()


# Cria a janela do menu inicial, nela tem dois métodos de criação de tabuleiros do jogo. Uma são três checkbox com 3
# tabuleiros predefinidos disponiveis, a outra são duas caixas de texto onde o jogador digita o tamanho do campo e a
# quantidade de minas que ele deseja no campo. Caso haja mais de uma checkbox marcada, ou algum dos valores digitados
# na caixa de texto seja invalido, o jogador não conseguirá criar o tabuleiro. Além disso, os valores digitados via
# texto recebem prioridade sobre os valores no checkbox, ou seja, se houver um tabuleiro marcado no checkbox, mas
# o jogador digitar valores validos na caixa de texto, o valor que será usado na criação do tabuleiro será o da
# caixa de texto
def menu_inicial():

    menu_inicial = tk.Tk()
    menu_inicial.geometry('250x150')
    menu_inicial.resizable(False, False)
    menu_inicial.title('titulo legal')

    tam = tk.StringVar()
    minas = tk.StringVar()

    var9x9 = tk.IntVar()
    tabuleiro9x9 = tk.Checkbutton(menu_inicial, text='Pequeno - Tabuleiro 9x9 (10 minas)', variable=var9x9)
    tabuleiro9x9.grid(row=0, column=0, sticky='W', columnspan=2)

    var16x16 = tk.IntVar()
    tabuleiro16x16 = tk.Checkbutton(menu_inicial, text='Medio - Tabuleiro 16x16 (40 minas)', variable=var16x16)
    tabuleiro16x16.grid(row=1, column=0, sticky='W', columnspan=2)

    var24x24 = tk.IntVar()
    tabuleiro24x24 = tk.Checkbutton(menu_inicial, text='Grande - Tabuleiro 24x24 (100 minas)', variable=var24x24)
    tabuleiro24x24.grid(row=2, column=0, sticky='W', columnspan=2)

    tamanho_custom_label = tk.Label(menu_inicial, text='Tamanho lateral:')
    tamanho_custom_label.grid(row=3, column=0, sticky='W')
    tamanho_custom = tk.Entry(menu_inicial, textvar=tam)
    tamanho_custom.grid(row=3, column=1, sticky='W')

    mina_custom_label = tk.Label(menu_inicial, text='Numero de Minas:')
    mina_custom_label.grid(row=4, column=0, sticky='W')
    mina_custom = tk.Entry(menu_inicial, textvar=minas)
    mina_custom.grid(row=4, column=1, sticky='W')

    okay = tk.Button(menu_inicial, text = 'confirmar')
    okay.bind('<Button-1>', partial(menu_check, [var9x9, var16x16, var24x24], menu_inicial, tamanho_custom, mina_custom, tam, minas))
    okay.grid(row=5, column=0, columnspan=2)

    menu_inicial.mainloop()

    if tam.get() != '' and minas.get() != '':
        if tam.get().isdigit() and minas.get().isdigit():
            return int(tam.get()), int(minas.get())

    if var9x9.get():
        return 9, 10

    if var16x16.get():
        return 16, 40

    if var24x24.get():
        return 24, 100


#checa se há apenas uma checkbox marcada e se os valores na caixa de texto são validos, caso sejam, a função destroi
# o menu e volta para a função menu_inicial, onde os valores para criação do novo tabuleiro são passados para
# a função montar_jogo()
def menu_check(variaveis, janela, tamanho_custom, mina_custom, tam, minas, evento):
    check = 0
    for var in variaveis:
        if var.get() == 1:
            check += 1

    if tam.get() != '' and minas.get() != '':
        if tam.get().isdigit() and minas.get().isdigit() and int(minas.get())<=int(tam.get())**2 and  int(minas.get())<=180 and int(tam.get())<=24 and int(tam.get())>=2:
            janela.destroy()

    if check == 1:
        janela.destroy()

    else:
        return


# dá ao jogador a opção de jogar novamente após ter vencido uma partida
def jogar_denovo():
    menu_aberto.set(True)
    janela.destroy()


#definição do tamanho lateral inicial e da quantidade inicial de minas
N = 9
n_minas = 10

while(True):
    tabuleiro, janela, mostrador = montar_jogo(N)

    # a variavel n_campos serve como uma variavel de controle para uma das condições de vitória, pois como ela armazena
    # o numero de campos existentes no tabuleiro (já que sempre que um campo é cavado o valor de n_campos é atualizado),
    # isso significa que quando n_minas = n_campos, todos os outros campos já foram cavados
    n_campos = tk.IntVar()
    n_campos.set(N**2)

    # a variavel n_marcadores armazena quantos marcadores o usuario ainda pode por no tabuleiro, e seu valor é
    # atualizado sempre que a função cavar() é chamada
    n_marcadores = tk.IntVar()
    n_marcadores.set(n_minas)

    # variavel que serve para dizer se o menu está ou não aberto e controlar as repetições do while em que o
    # programa está rodando
    menu_aberto = tk.BooleanVar()
    menu_aberto.set(False)

    #inicio do jogo
    lista_de_minas = inicializar()
    janela.mainloop()
    if menu_aberto.get():
        N, n_minas = menu_inicial()
        continue
    break
