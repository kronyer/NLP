import Data.List (isInfixOf)
import Data.List (nub)
import Data.Char (toLower)

textoTeste = "Este é um \n texto de teste. Este texto serve para testar o concordancionador. O concordancionador deve encontrar todas as ocorrências do termo teste."

-- Retorna trechos de 80 caracteres ao redor do termo buscado
concordancionador :: String -> String -> [String]
concordancionador termo texto = extrairOcorrencias termo textoLimpo
  where
    textoLimpo = replace "\n" " " texto
    extrairOcorrencias :: String -> String -> [String]
    extrairOcorrencias t txt = go txt
      where
        go [] = []
        go s =
          case busca t s of
            Nothing -> []
            Just idx ->
              let posInicio = max 0 (idx - (40 - length t `div` 2))
                  trecho = take 80 (drop posInicio s)
                  -- Avança 1 caractere após a ocorrência encontrada
                  nextStart = drop (idx + 1) s
              in trecho : go nextStart
        busca :: String -> String -> Maybe Int
        busca alvo s = findIndex' 0 s
          where
            findIndex' _ [] = Nothing
            findIndex' n xs
              | take (length alvo) xs == alvo = Just n
              | otherwise = findIndex' (n+1) (tail xs)

-- Função de substituição de string
replace :: String -> String -> String -> String
replace _ _ [] = []
replace antigo novo texto@(x:xs)
    | take (length antigo) texto == antigo = novo ++ replace antigo novo (drop (length antigo) texto)
    | otherwise = x : replace antigo novo xs


