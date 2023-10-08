# Trabalho de Projeto e Análise de Algoritmos
# Aluno: João Guilherme dos Santos Moreira

import os, re, time, csv

def programacao_dinamica(itens, capacidade_mochila):
    quant_itens = len(itens)
    tabela = [[0] * (capacidade_mochila + 1) for _ in range(quant_itens + 1)]

    for i in itens:
        for j in range(capacidade_mochila + 1):
            if i['peso'] <= j:
                tabela[i['id']][j] = max(
                    tabela[i['id'] - 1][j], tabela[i['id'] - 1][j - i['peso']] + i['valor'])
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
    itens_ordenados = sorted(
        range(quant_itens), key=lambda i: valor_por_peso[i], reverse=True)

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
    tempo_inicial_total = time.time()
    tempo_total_programacao_dinamica = 0
    tempo_total_heuristica_gulosa = 0

    print('PAA - Problema da Mochila')
    print('João Guilherme dos Santos Moreira')

    if (os.path.exists('resultados.csv')):
        os.remove('resultados.csv')

    with open('resultados.csv', 'w', newline='') as csvfile:
        colunas = ['instancia', 'numero_itens', 'capacidade_mochila', 'solucao_programacao_dinamica', 
                   'solucao_heuristica_gulosa', 'diferenca_solucoes', 'tempo_execucao_programacao_dinamica', 
                   'tempo_execucao_heuristica_gulosa', 'diferenca_tempo_execucao', 'tempo_total_execucao', 
                   'itens_selecionados_programacao_dinamica', 'itens_selecionados_heuristica_gulosa']
        writer = csv.DictWriter(csvfile, fieldnames=colunas, delimiter=';')
        csvfile.write('sep=;\n')
        writer.writeheader()
        
        for instancia in sorted(os.listdir(diretorio), key=ordenacao_natural):
            with open(os.path.join(diretorio, instancia), 'r') as f:
                linhas_instancia = f.readlines()
                numero_itens = int(linhas_instancia[0].split(' ')[0])
                capacidade_mochila = int(linhas_instancia[0].split(' ')[1])
                itens = []

                for i in range(1, numero_itens + 1):
                    id, peso, valor = linhas_instancia[i].split(' ')
                    itens.append(
                        {'id': int(id), 'peso': int(peso), 'valor': int(valor)})

                print('----------------------------------------')
                print(f'Instância: {instancia} | {numero_itens} itens | Mochila com {capacidade_mochila} de capacidade')

                tempo_inicial_programacao_dinamica = time.time()

                solucao_programacao_dinamica, itens_programacao_dinamica = programacao_dinamica(
                    itens, capacidade_mochila)
                
                tempo_execucao_programacao_dinamica = time.time() - tempo_inicial_programacao_dinamica
                tempo_total_programacao_dinamica += tempo_execucao_programacao_dinamica

                print(
                    f"- Solução (Programação Dinâmica): {solucao_programacao_dinamica}")
                print(
                    f"- Tempo de execução (Programação Dinâmica): {tempo_execucao_programacao_dinamica} segundo(s)")

                tempo_inicial_heuristica_gulosa = time.time()

                solucao_gulosa, itens_heuristica_gulosa = heuristica_gulosa(
                    itens, capacidade_mochila)
                
                tempo_execucao_heuristica_gulosa = time.time() - tempo_inicial_heuristica_gulosa
                tempo_total_heuristica_gulosa += tempo_execucao_heuristica_gulosa

                print(f"- Solução (Heurística Gulosa): {solucao_gulosa}")
                print(
                    f"- Tempo de execução (Heurística Gulosa): {tempo_execucao_heuristica_gulosa} segundo(s)")
                
                print(f"- Diferença entre as soluções: {solucao_programacao_dinamica - solucao_gulosa}")
                print(f"- Diferença entre os tempos de execução: {tempo_execucao_programacao_dinamica - tempo_execucao_heuristica_gulosa} segundo(s)")
                
                diferenca_solucoes = solucao_programacao_dinamica - solucao_gulosa
                diferenca_tempo_execucao = tempo_execucao_programacao_dinamica - tempo_execucao_heuristica_gulosa

                writer.writerow({'instancia': instancia, 'numero_itens': numero_itens, 'capacidade_mochila': capacidade_mochila, 
                                 'solucao_programacao_dinamica': solucao_programacao_dinamica, 'solucao_heuristica_gulosa': solucao_gulosa,
                                 'diferenca_solucoes': diferenca_solucoes, 
                                 'tempo_execucao_programacao_dinamica': tempo_execucao_programacao_dinamica, 
                                 'tempo_execucao_heuristica_gulosa': tempo_execucao_heuristica_gulosa,
                                 'diferenca_tempo_execucao': diferenca_tempo_execucao,
                                 'itens_selecionados_programacao_dinamica': itens_programacao_dinamica, 
                                 'itens_selecionados_heuristica_gulosa': itens_heuristica_gulosa, 
                                 'tempo_total_execucao': tempo_execucao_programacao_dinamica + tempo_execucao_heuristica_gulosa})
        
        print('----------------------------------------')
        print(
            f"Tempo total de execução (Programação Dinâmica): {tempo_total_programacao_dinamica} segundo(s)")
        print(
            f"Tempo total de execução (Heurística Gulosa): {tempo_total_heuristica_gulosa} segundo(s)")
        print(
            f"Tempo total de execução: {tempo_total_programacao_dinamica + tempo_total_heuristica_gulosa} ({time.time() - tempo_inicial_total}) segundo(s) ")

        writer.writerow({'tempo_execucao_programacao_dinamica': tempo_total_programacao_dinamica,
                        'tempo_execucao_heuristica_gulosa': tempo_total_heuristica_gulosa, 
                        'diferenca_tempo_execucao': tempo_total_programacao_dinamica - tempo_total_heuristica_gulosa,
                        'tempo_total_execucao': tempo_total_programacao_dinamica + tempo_total_heuristica_gulosa})


if __name__ == "__main__":
    main()
