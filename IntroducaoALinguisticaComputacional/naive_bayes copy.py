import math

import corpus

from collections import defaultdict

lt = 0
la = 0
em_lt = defaultdict(int)
em_la = defaultdict(int)

vocab = set()

def atributos(msg):
    palavras = msg.split()
    palavras = corpus.limpar(palavras)

    return set(palavras)



corpus_treino = open('corpus_treino_bayes1.txt', 'r', encoding='utf-8')

for dado in corpus_treino:
    classe = dado[0]
    texto = dado[2:]
    palavras = atributos(texto)

    vocab |= palavras

    if classe == '1':
        la += 1
        for palavra in palavras:
            em_la[palavra] += 1
    elif classe == '0':
        lt += 1
        for palavra in palavras:
            em_lt[palavra] += 1

corpus_treino.close()


#suavização do calssificador

k =1 

p_lt = (lt + 2 * k) / (lt + la + 4 * k)

p_la = (la + 2 * k) / (lt + la + 4 * k)

def p_em_lt(palavra):
    return (em_lt[palavra] + k) / (lt + 2 * k)

def p_em_la(palavra):
    return (em_la[palavra] + k) / (la + 2 * k)


def classificar(msg):
    score_lt = math.log(p_lt)
    score_la = math.log(p_la)

    palavras_na_msg = atributos(msg)

    for palavra in vocab:
        prob_lt = p_em_lt(palavra)
        prob_la = p_em_la(palavra)
        
        if palavra in palavras_na_msg:
            # Em vez de *=, usamos += math.log()
            score_lt += math.log(prob_lt)
            score_la += math.log(prob_la)
        else:
            # Probabilidade de NÃO aparecer a palavra
            score_lt += math.log(1 - prob_lt)
            score_la += math.log(1 - prob_la)

    if score_lt > score_la:
        return 'LT'
    else:
        return 'LA'
    

# testando
teste1 = "sentido, sentença, sujeito, gramática"
print(classificar(teste1))