import nltk
from nltk.corpus import machado

def remove_nao_alfanumericos(texto):
    return ''.join(caractere for caractere in texto if caractere.isalnum() or caractere.isspace())


print(remove_nao_alfanumericos("Olá, mundo! Este é um teste. #NLP @2024"))


def contar_letras(texto):
    dicionario_letras = dict()
    for caractere in texto:
        if caractere.isalpha():
            letra = caractere.lower()
            if letra in dicionario_letras:
                dicionario_letras[letra] += 1
            else:
                dicionario_letras[letra] = 1
    return dicionario_letras

texto = "Olá, mundo! Este é um teste. #NLP @2024"
dicionario_letras = contar_letras(texto)
print(dicionario_letras)

def lista_ordenada_letras(dicionario_letras):
    resultado = [item[0] for item in sorted(dicionario_letras.items(), key=lambda x: x[1], reverse=True)]
    return resultado

letras_ordenadas = lista_ordenada_letras(dicionario_letras)
print(letras_ordenadas)


def hapex_letras(dicionario_letras):
    hapex = [letra for letra, contagem in dicionario_letras.items() if contagem == 1]
    return hapex



texto = machado.raw('romance/marm05.txt')

caracteres_no_texto = len(texto)
print(f"Total de caracteres no texto: {caracteres_no_texto}")


def limpar(text):
    lixo = '.,>.?!"`():[][]\/|#$^&*'
    quase_limpo = [x.strip(lixo).lower() for x in text]
    return [x for x in quase_limpo if x.isalpha() or '-' in x]


caracteres_no_texto_limpo = len(limpar(texto.split()))
print(f"Total de caracteres no texto limpo: {caracteres_no_texto_limpo}")

palavras_unicas_no_texto_limpo = len(set(limpar(texto.split())))
print(f"Total de palavras unicas no texto limpo: {palavras_unicas_no_texto_limpo}")

palavras_no_texto = len(limpar(texto.split()))
print(f"Total de palavras no texto limpo: {palavras_no_texto}")


# riqueza lexical = palavras unicas / total de palavras

riqueza_lexical = palavras_unicas_no_texto_limpo / palavras_no_texto
print(f"Riqueza lexical: {riqueza_lexical:.4f}")


vazias = nltk.corpus.stopwords.words('portuguese')

texto_sem_vazias = [palavra for palavra in limpar(texto.split()) if palavra not in vazias]
print(f"Total de palavras sem stopwords: {len(texto_sem_vazias)}")

texto_sem_vazias_unico = set(texto_sem_vazias)
print(f"Total de palavras unicas sem stopwords: {len(texto_sem_vazias_unico)}")

riqueza_lexical_sem_vazias = len(texto_sem_vazias_unico) / len(texto_sem_vazias)
print(f"Riqueza lexical sem stopwords: {riqueza_lexical_sem_vazias:.4f}")


def hapex_legomenon(palavras):
    hapex = [palavra for palavra in set(palavras) if palavras.count(palavra) == 1]
    return hapex

hapex = hapex_legomenon(limpar(texto.split()))
print(f"Total de hapex legomenon: {len(hapex)}")

print(f"Hapex legomenon: {hapex}")

