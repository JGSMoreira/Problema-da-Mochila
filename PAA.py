import os
import re
import time

def programacao_dinamica(itens, capacidade_mochila):
    quant_itens = len(itens)
    tabela = [[0] * (capacidade_mochila + 1) for _ in range(quant_itens + 1)]

    for i in itens:
        for j in range(capacidade_mochila + 1):
            if i['peso'] <= j:
                tabela[i['id']][j] = max(tabela[i['id'] - 1][j], tabela[i['id'] - 1][j - i['peso']] + i['valor'])
            else:
                tabela[i['id']][j] = tabela[i['id'] - 1][j]

    itens_mochilados = []
    j, i = capacidade_mochila, quant_itens

    while i > 0 and j > 0:
        if tabela[i][j] != tabela[i - 1][j]:
            itens_mochilados.append(itens[i - 1])
            j -= itens[i - 1]['peso']
        i -= 1

    return tabela[quant_itens][capacidade_mochila], itens_mochilados

def heuristica_gulosa(itens, capacidade_mochila):
    valor_total = 0
    valor_atual = 0
    itens_mochilados = []

    quant_itens = len(itens)
    valor_por_peso = [item['valor'] / item['peso'] for item in itens]
    itens_ordenados = sorted(range(quant_itens), key=lambda i: valor_por_peso[i], reverse=True)

    for i in itens_ordenados:
        if valor_atual + itens[i]['peso'] <= capacidade_mochila:
            itens_mochilados.append(itens[i])
            valor_total += itens[i]['valor']
            valor_atual += itens[i]['peso']

    return valor_total, itens_mochilados

def ordenacao_natural(texto):
    return [int(c) if c.isdigit() else c for c in re.split('(\d+)', texto)]

def main():
    diretorio = os.getcwd() + '/instancias'

    print('PAA - Problema da Mochila')
    print('João Guilherme dos Santos Moreira')

    tempo_inicial_total = time.time()
    tempo_total_programacao_dinamica = 0
    tempo_total_heuristica_gulosa = 0
    for instancia in sorted(os.listdir(diretorio), key=ordenacao_natural):
        with open(os.path.join(diretorio, instancia), 'r') as f:
            linhas_instancia = f.readlines()
            numero_itens = int(linhas_instancia[0].split(' ')[0])
            capacidade_mochila = int(linhas_instancia[0].split(' ')[1])
            itens = []

            for i in range(1, numero_itens + 1):
                id, peso, valor = linhas_instancia[i].split(' ')
                itens.append({'id': int(id), 'peso': int(peso), 'valor': int(valor)})

            print('----------------------------------------')
            print('Instância: ' + instancia)
            # print(f'Numero de itens: {numero_itens}')
            # print(f'Capacidade da mochila: {capacidade_mochila}')
            
            tempo_inicial_programacao_dinamica = time.time()
            solucao_programacao_dinamica, itens_programacao_dinamica = programacao_dinamica(itens, capacidade_mochila)
            tempo_execucao_programacao_dinamica = time.time() - tempo_inicial_programacao_dinamica
            tempo_total_programacao_dinamica += tempo_execucao_programacao_dinamica

            print(f"Solução (Programação Dinâmica): {solucao_programacao_dinamica}")
            print(f"Tempo de execução (Programação Dinâmica): {tempo_execucao_programacao_dinamica} segundos")

            tempo_inicial_heuristica_gulosa = time.time()
            solucao_gulosa, itens_heuristica_gulosa = heuristica_gulosa(itens, capacidade_mochila)
            tempo_execucao_heuristica_gulosa = time.time() - tempo_inicial_heuristica_gulosa
            tempo_total_heuristica_gulosa += tempo_execucao_heuristica_gulosa

            print(f"Solução (Heurística Gulosa): {solucao_gulosa}")
            print(f"Tempo de execução (Heurística Gulosa): {tempo_execucao_heuristica_gulosa} segundos")
            # print(f"Itens selecionados: {itens_heuristica_gulosa}")
    print('----------------------------------------')
    print(f"Tempo total de execução (Programação Dinâmica): {tempo_total_programacao_dinamica} segundos")
    print(f"Tempo total de execução (Heurística Gulosa): {tempo_total_heuristica_gulosa} segundos")
    print(f"Tempo total de execução: {time.time() - tempo_inicial_total} segundos")

    # # ITENS DE TESTE
    # itens = [
    #     {'id': 1, 'peso': 10, 'valor': 60},
    #     {'id': 2, 'peso': 20, 'valor': 100},
    #     {'id': 3, 'peso': 30, 'valor': 120}
    # ]
    # numero_itens = len(itens)
    # capacidade_mochila = 50

    # print(f'Numero de itens: {numero_itens}')
    # print(f'Capacidade da mochila: {capacidade_mochila}')
    
    # print('----------------------------------------')
    # solucao_programacao_dinamica, itens_programacao_dinamica = programacao_dinamica(itens, capacidade_mochila)
    # print('Programação Dinâmica')
    # print(f"Solução: {solucao_programacao_dinamica}")
    # print(f"Itens selecionados: {itens_programacao_dinamica}")

    # print('----------------------------------------')
    # solucao_gulosa, itens_heuristica_gulosa = heuristica_gulosa(itens, capacidade_mochila)
    # print('Heurística Gulosa')
    # print(f"Solução: {solucao_gulosa}")
    # print(f"Itens selecionados: {itens_heuristica_gulosa}")
    # print('----------------------------------------')

if __name__ == "__main__":
    main()