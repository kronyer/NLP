import time
import re
from collections import defaultdict


def limpar(text):
    lixo = '.,>.?!"`():[][]|#$^&*'
    quase_limpo = [x.strip(lixo).lower() for x in text]
    return [x for x in quase_limpo if x.isalpha() or '-' in x]

with open('corpus_bruto.txt', 'r', encoding='utf-8') as f:
    corpus_base = f.read()

corpus_pontuacao = re.sub(r'\.|\!|\?', '#', corpus_base)

sents = corpus_pontuacao.split('#')



sents = [['<s>'] + limpar(x.split()) + ['</s>'] for x in sents]

c_p = open('corpus_preparado.txt', 'w', encoding='utf-8')

for sentenca in sents:
    str = ' '.join(sentenca)
    c_p.write(str + '\n')
c_p.close()

# 80/20 -> treino/teste

corpus_tt = open('corpus_preparado.txt', 'r', encoding='utf-8')
c_tt = corpus_tt.readlines()

corte = int(len(c_tt) * 0.8 )
treino = c_tt[:corte]
teste = c_tt[corte:]

tr = open('corpus_treino.txt', 'w', encoding='utf-8')
for linha in treino:
    tr.write(linha)
tr.close()

ts = open('corpus_teste.txt', 'w', encoding='utf-8')
for linha in teste:
    ts.write(linha)
ts.close()

corpus_treino = open('corpus_treino.txt', 'r', encoding='utf-8')
c_t = corpus_treino.readlines()
corpus_treino.close()

vocab = set()
contagem = defaultdict(int)
for linha in c_t:
    palavras = linha.split()
    for palavra in palavras:
        vocab |= {palavra}
        contagem[palavra] += 1

#os hapex são descartados, pois não contribuem para o modelo de linguagem
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

    for i in range (len(sent)):
        if sent[i] in hapax:
            sent[i] = '<DES>'

    for x in ngramas(1, sent):
        unigramas[x] += 1

    for x in ngramas(2, sent):
        bigramas[x] += 1


def prob_uni(x):
    C = sum(unigramas.values())
    V = len(novo_vocab)
    return (unigramas[x] + 1) / (C + V)

def prob_bi(x):
    V = len(novo_vocab)
    return (bigramas[x] + 1) / (unigramas[(x[0],)] + V)


def prever(palavra):
    lista = [ch for ch in bigramas.keys() if ch[0] == palavra]
    if not lista:
        return '<s>'
    ordem = sorted(lista, key=prob_bi, reverse=True)
    topo = ordem[0][1]
    return topo


# Palavra de partida
palavra_atual = 'o'

# Imprime a primeira palavra sem pular linha
print(palavra_atual, end=' ', flush=True)

try:
    while True:
        # Prevê a próxima baseada na atual
        proxima_palavra = prever(palavra_atual)
        
        # Imprime a próxima na mesma linha
        print(proxima_palavra, end=' ', flush=True)
        
        # O pulo do gato: a próxima palavra vira a palavra atual para o próximo ciclo
        palavra_atual = proxima_palavra
        
        # Uma pequena pausa para você conseguir ler a geração no terminal
        time.sleep(0.3)
        
except KeyboardInterrupt:
    # Permite que você pare o texto infinito apertando Ctrl+C no terminal
    print("\n\nGeração interrompida!")