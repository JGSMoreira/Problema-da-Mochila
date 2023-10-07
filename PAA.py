import os

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
    quant_itens = len(itens)
    valor_por_peso = [item['valor'] / item['peso'] for item in itens]
    itens_ordenados = sorted(range(quant_itens), key=lambda i: valor_por_peso[i], reverse=True)

    itens_mochilados = []
    valor_total = 0
    valor_atual = 0

    for i in itens_ordenados:
        if valor_atual + itens[i]['peso'] <= capacidade_mochila:
            itens_mochilados.append(itens[i])
            valor_total += itens[i]['valor']
            valor_atual += itens[i]['peso']

    return valor_total, itens_mochilados

def main():
    print('PAA - Problema da Mochila')
    print('João Guilherme dos Santos Moreira')

    diretorio_atual = os.path.abspath(os.path.dirname(__file__))
    caminho_instancias = os.path.join(diretorio_atual, 'instancias')

    with open(os.path.join(caminho_instancias, 'instancia1.txt'), 'r') as f:
        linhas_instancia = f.readlines()
        numero_itens = int(linhas_instancia[0].split(' ')[0])
        capacidade_mochila = int(linhas_instancia[0].split(' ')[1])
        itens = []

        # for i in range(1, numero_itens + 1):
        #     id, peso, valor = linhas_instancia[i].split(' ')
        #     # print(f'{id}: {peso}, {valor}')
        #     itens.append({'id': int(id), 'peso': int(peso), 'valor': int(valor)})

        # ITENS DE TESTE
        itens = [
            {'id': 1, 'peso': 10, 'valor': 60},
            {'id': 2, 'peso': 20, 'valor': 100},
            {'id': 3, 'peso': 30, 'valor': 120}
        ]
        numero_itens = len(itens)
        capacidade_mochila = 50
        
        print(f'Numero de itens: {numero_itens}')
        print(f'Capacidade da mochila: {capacidade_mochila}')
        
        print('----------------------------------------')
        solucao_programacao_dinamica, itens_programacao_dinamica = programacao_dinamica(itens, capacidade_mochila)
        print('Programação Dinâmica')
        print(f"Solução: {solucao_programacao_dinamica}")
        print(f"Itens selecionados: {itens_programacao_dinamica}")

        print('----------------------------------------')
        solucao_gulosa, itens_heuristica_gulosa = heuristica_gulosa(itens, capacidade_mochila)
        print('Heurística Gulosa')
        print(f"Solução: {solucao_gulosa}")
        print(f"Itens selecionados: {itens_heuristica_gulosa}")
        print('----------------------------------------')

if __name__ == "__main__":
    main()