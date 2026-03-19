import math

import corpus

from collections import defaultdict

spams = 0
nao_spams = 0
em_spans = defaultdict(int)
em_nao_spams = defaultdict(int)

vocab = set()

def atributos(msg):
    palavras = msg.split()
    palavras = corpus.limpar(palavras)

    return set(palavras)



corpus_treino = open('corpus_treino_bayes.txt', 'r', encoding='utf-8')

for dado in corpus_treino:
    classe = dado[0]
    texto = dado[2:]
    palavras = atributos(texto)

    vocab |= palavras

    if classe == '1':
        spams += 1
        for palavra in palavras:
            em_spans[palavra] += 1
    elif classe == '0':
        nao_spams += 1
        for palavra in palavras:
            em_nao_spams[palavra] += 1

corpus_treino.close()


#suavização do calssificador

k =1 

p_spam = (spams + 2 * k) / (spams + nao_spams + 4 * k)

p_nao_spam = (nao_spams + 2 * k) / (spams + nao_spams + 4 * k)

def p_em_spam(palavra):
    return (em_spans[palavra] + k) / (spams + 2 * k)

def p_em_nao_spam(palavra):
    return (em_nao_spams[palavra] + k) / (nao_spams + 2 * k)


def classificar(msg):
    score_spam = math.log(p_spam)
    score_nao_spam = math.log(p_nao_spam)

    palavras_na_msg = atributos(msg)

    for palavra in vocab:
        prob_spam = p_em_spam(palavra)
        prob_nao_spam = p_em_nao_spam(palavra)
        
        if palavra in palavras_na_msg:
            # Em vez de *=, usamos += math.log()
            score_spam += math.log(prob_spam)
            score_nao_spam += math.log(prob_nao_spam)
        else:
            # Probabilidade de NÃO aparecer a palavra
            score_spam += math.log(1 - prob_spam)
            score_nao_spam += math.log(1 - prob_nao_spam)

    if score_spam > (math.log(2) + score_nao_spam):
        return 'SPAM'
    else:
        return 'NAO SPAM'
    

# testando
msg1 = "viagra com um bom preço: entregamos em seu consultório"
print(classificar(msg1))

msg2= "pesquisas sobre viagra mostram que o medicamento é eficaz no tratamento de disfunção erétil"
print(classificar(msg2))

msg3 = "pesquisas sobre viagra: reunião confirmada no consultório amanhã"
print(classificar(msg3))