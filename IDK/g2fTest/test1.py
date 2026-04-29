import epitran

# 'por-Latn' cobre o Português padrão
epi = epitran.Epitran('por-Latn')

texto = "O rato roeu a roupa"
fonemas = epi.transliterate(texto)

print(fonemas) 
# Resultado em IPA: o ɾatu ɾoew a ɾowpa