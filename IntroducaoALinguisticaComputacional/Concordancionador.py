def concordancionador (alvo, texto):
    texto = texto.replace('\n', ' ')
    texto = texto.replace('\t', ' , ')

    ocorrencias = list()
    encontrado_aqui = texto.find(alvo,0)

    while encontrado_aqui > 0:
        pos_inicio = encontrado_aqui - (40 - len(alvo)//2)
        ocorrencias.append(texto[pos_inicio:pos_inicio + 80])

        encontrado_aqui = texto.find(alvo,encontrado_aqui + 1)

    return ocorrencias