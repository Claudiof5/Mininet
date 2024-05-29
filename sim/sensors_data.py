import csv

def lerArquivoCsv(arquivoCsv):
    dados = []
    with open(arquivoCsv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dados.append(dict(row))
    return dados
