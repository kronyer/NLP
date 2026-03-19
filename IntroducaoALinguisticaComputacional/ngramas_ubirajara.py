import nltk
import re
from collections import defaultdict
from nltk.corpus import machado


def limpar(text):
    lixo = '.,>.?!"`():[][]|#$^&*'
    quase_limpo = [x.strip(lixo).lower() for x in text]
    return [x for x in quase_limpo if x.isalpha() or '-' in x]

with open('ubirajara.txt', 'r', encoding='utf-8') as f:
    corpus_base = f.read()

corpus_pontuacao = re.sub(r'\.|\!|\?', '#', corpus_base)

sents = corpus_pontuacao.split('#')
sents = [['<s>'] + limpar(x.split()) + ['</s>'] for x in sents]

c_p = open('ubirajara_preparado.txt', 'w', encoding='utf-8')


for sentenca in sents:
    str = ' '.join(sentenca)
    c_p.write(str + '\n')
c_p.close()

# 80/20 -> treino/teste

corpus_tt = open('ubirajara_preparado.txt', 'r', encoding='utf-8')
c_tt = corpus_tt.readlines()

corte = int(len(c_tt) * 0.8 )
treino = c_tt[:corte]
teste = c_tt[corte:]

tr = open('ubi_corpus_treino.txt', 'w', encoding='utf-8')
for linha in treino:
    tr.write(linha)
tr.close()

ts = open('ubi_corpus_teste.txt', 'w', encoding='utf-8')
for linha in teste:
    ts.write(linha)
ts.close()

corpus_treino = open('ubi_corpus_treino.txt', 'r', encoding='utf-8')
c_t = corpus_treino.readlines()
corpus_treino.close()

vocab = set()
contagem = defaultdict(int)
for linha in c_t:
    palavras = linha.split()
    for palavra in palavras:
        vocab |= {palavra}
        contagem[palavra] += 1


hapax = [palavra for palavra in contagem.keys() if contagem[palavra] == 1]
hapax = set(hapax)

novo_vocab = vocab - hapax
novo_vocab |= {'<DES>'}

def ngramas(n, sent):
    return [tuple(sent[i:i+n]) for i in range(len(sent)-n+1)]

unigramas = defaultdict(int)
bigramas = defaultdict(int)

for linha in c_t:
    sent = linha.split()

    for i in range(len(sent)):
        if sent[i] in hapax:
            sent[i] = '<DES>'

    for x in ngramas(1, sent):
        unigramas[x] += 1

    for x in ngramas(2, sent):
        bigramas[x] += 1


def prob_unigrama(palavra):
    C = sum(unigramas.values())
    V = len(novo_vocab)
    return (unigramas[(palavra,)] + 1) / (C + V)

def prob_bigramas(palavra1, palavra2):
    C = sum(unigramas.values())
    V = len(novo_vocab)
    return (bigramas[(palavra1, palavra2)] + 1) / (unigramas[(palavra1,)] + V)


calculaProbabilidadeUnigrama = lambda x: prob_unigrama(x)
calculaProbabilidadeBigramas = lambda x, y: prob_bigramas(x, y)


print(calculaProbabilidadeUnigrama('Pela'))

print(calculaProbabilidadeBigramas('Pela', 'Margem'))

print(calculaProbabilidadeBigramas('Margem', 'do'))


def extrair_frase_aleatoria():
    import random
    return random.choice(c_t).split()[1:-1]

frase_aleatoria = extrair_frase_aleatoria()

def probabilidade_frase(frase):
    prob = 1
    for i in range(len(frase)-1):
        prob *= calculaProbabilidadeBigramas(frase[i], frase[i+1])
    return prob

print(probabilidade_frase(frase_aleatoria))