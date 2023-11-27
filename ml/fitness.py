import statistics
import numpy as np
import pandas as pd


class Fitness:
    def __init__(self):
        pass

    def fitness_function(self, solucao):

        dinheiro_total = 5000
        taxas_selic = [12.5, 9.25, 7.25, 7.75, 9.5, 14.25, 14.25, 14.25, 6.5, 5.25, 2.25, 7.75, 11.75, 12.5]

        valores = [dinheiro_total]

        for taxa in taxas_selic:
            novo_valor = valores[-1] + (valores[-1] * taxa / 100)
            valores.append(novo_valor)

        #valor_2023 = valores[-1]
        taxa_selic_historico = np.array(taxas_selic)
        #dataset_original = dataset.copy()
        sem_risco = taxa_selic_historico.mean() / 100
        #rf = sem_risco

        a = []
        for j in range(12, 24):
            dataset = pd.read_csv(f'excel/acoes20{j}.csv')
            pesos = solucao / solucao.sum()
            dataset.drop(columns=["BOVA11.SA"], inplace=True)

            for i in dataset.columns[1:]:
                dataset[i] = (dataset[i] / dataset[i][0])  # normalizador das colunas

            for i, acao in enumerate(dataset.columns[1:]):
                dataset[acao] = dataset[acao] * pesos[i] * dinheiro_total

            dataset.drop(labels=['Date'], axis=1, inplace=True)
            dataset['soma valor'] = dataset.sum(axis=1)

            dataset['taxa retorno'] = 0.0
            dataset["taxa retorno"] = dataset["soma valor"].pct_change()
            risk_free = sem_risco / 252
            dataset["retorno Calc"] = dataset["taxa retorno"] - risk_free
            sharpe_ratio = np.sqrt(252) * (dataset["retorno Calc"].mean() / dataset["retorno Calc"].std())
            a.append(sharpe_ratio)

        peso_valor = [1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5]
        a_weighted = np.multiply(a, peso_valor)
        sharpe_ratio = statistics.mean(a_weighted) / 25
        return sharpe_ratio
    def visualiza_alocacao(self, solucao):
        dataset_original = pd.read_csv('excel/acoes.csv')
        dataset_original.drop(columns=["BOVA11.SA"], inplace=True)
        colunas = dataset_original.columns[1:]
        for i in range(len(solucao)):
            print(colunas[i], solucao[i] * 100)
        
    def alocacao_ativos(self,dataset, dinheiro_total, seed = 0, melhores_pesos = []):
        if seed != 0:
            np.random.seed(seed)

        dataset = dataset.copy()

        if len(melhores_pesos) > 0:
            pesos = melhores_pesos
        else:  
            pesos = np.random.random(len(dataset.columns) - 1)
        #print(pesos, pesos.sum())
            pesos = pesos / pesos.sum()
        #print(pesos, pesos.sum())
        
    
        colunas = dataset.columns[1:]

        for i in colunas:
            dataset[i] = dataset[i] / dataset[i][0]

        for i, acao in enumerate(dataset.columns[1:]):
            dataset[acao] = dataset[acao] * pesos[i] * dinheiro_total

        dataset['SOMA VALOR'] = dataset[colunas].sum(axis=1)

        datas = dataset['Date']

        dataset.drop(columns=['Date'], inplace=True)
        dataset['taxa de retorno'] = 0.0

        for i in range(1, len(dataset)):
            dataset['taxa de retorno'][i] = ((dataset['SOMA VALOR'][i] / dataset['SOMA VALOR'][i-1]) - 1 )*100

        acoes_pesos = pd.DataFrame(data= {'Ações': colunas, 'Pesos': pesos*100})

        return dataset, datas, acoes_pesos , dataset.loc[len(dataset)-1]['SOMA VALOR']    