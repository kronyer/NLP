

checkPalindrome :: String -> Bool
checkPalindrome word = reverse word == word


word = ["The", "cat", "sat", "on", "the", "mat"]

-- to get the average tokens, sum the length of each token and divide by the number of tokens
averageTokens :: [String] -> Float
averageTokens prashe = fromIntegral (sum (map length prashe)) / fromIntegral (length prashe)


--lets consider the ' ' as a word separator, and \n as a sentence separator

phrase1 = "This is Jack .\nHe is a Haskeller ."

--we can use `lines` to split the phrase into sentences, and `words` to split the sentences into tokens