def limpar(text):
    lixo = '.,>.?!"`():[][]\/|#$^&*'
    quase_limpo = [x.strip(lixo).lower() for x in text]
    return [x for x in quase_limpo if x.isalpha() or '-' in x]