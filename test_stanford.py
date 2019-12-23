# > pipenv shell
# > stanfordnlp.download('nl')

VB = "VERB"
NN = "NOUN|PROPN|ADJ"

import stanfordnlp

nlp = stanfordnlp.Pipeline(lang="nl")
text = "Het op vakantie gaan is leuk."
nlp_text = nlp(text)

for sentence in nlp_text.sentences:
    for dependency in sentence.dependencies:
        word1 = dependency[0].text
        pos1 = dependency[0].upos

        if not pos1:
            pos1 = ""
        dependency_tag = dependency[1]
        word2 = dependency[2].text
        pos2 = dependency[2].upos

        if not pos2:
            pos2 = ""
        print(word1 + " (" + pos1 + ") " + " -| " + dependency_tag + " |-> " + word2 + " (" + pos2 + ") ")


