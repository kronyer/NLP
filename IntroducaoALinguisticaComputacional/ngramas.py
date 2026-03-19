import re
from collections import Counter

input_file = 'IntroducaoALinguisticaComputacional/chat.txt'
output_file = 'frases_treino.txt'

pattern = r"Brunounesp: (.*)"
mention_pattern = r"@[\u2068\u2069]*~?([\w\s]+)[\u2069]*"
termos_lixo = ["<Mídia oculta>", "<Mídia omitida>", "<Arquivo omitido>", "cartão de contato omitido"]

# Para capturar símbolos estranhos
caracteres_estranhos = Counter()

with open(input_file, 'r', encoding='utf-8') as f:
    conteudo = f.read()

mensagens = re.findall(pattern, conteudo)

with open(output_file, 'w', encoding='utf-8') as out:
    for frase in mensagens:
        frase = frase.strip()
        if any(termo.lower() in frase.lower() for termo in termos_lixo):
            continue
            
        frase_limpa = re.sub(mention_pattern, r"\1", frase)
        frase_limpa = frase_limpa.replace('\u2068', '').replace('\u2069', '').replace('~', '')
        
        # Encontra tudo que não é letra, número, espaço ou pontuação comum
        estranhos = re.findall(r'[^\w\s.,!?;:()\"\'\-]', frase_limpa)
        caracteres_estranhos.update(estranhos)
        
        frase_limpa = " ".join(frase_limpa.split())
        
        if frase_limpa:
            out.write(f"<s> {frase_limpa} </s>\n")

print(f"--- Relatório de Símbolos ---")
print(f"Total de frases: {len(mensagens)}")
print("\nTop 15 'Símbolos' encontrados (inclui emojis):")
for char, freq in caracteres_estranhos.most_common(15):
    print(f"Símbolo: {char} | Frequência: {freq}")