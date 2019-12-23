import test_spacy
from textacy.extract import matches
from scripting.knowledge_graph.HDSKG.helperfunctions import set_pos_exceptions, view_displacy
from scripting.knowledge_graph.HDSKG import patterns

nlp = test_spacy.load('nl_core_news_sm')

text = """Iedereen die in Nederland woont of werkt en die is verzekerd voor zorg vanuit de Wlz betaalt hiervoor premie. 
Hieruit wordt de zorg betaald. Bijna altijd betaalt u daarnaast een eigen bijdrage."""

doc = nlp(text)

doc = set_pos_exceptions(doc)

verb_closed_results = matches(doc, patterns.verbs_closed)
verbs_closed = [span for span in verb_closed_results]

verbs_open_results = matches(doc, patterns.verbs_open)
verbs_open = [span for span in verbs_open_results]

verbs = [verbs_open, verbs_closed]

noun_results = matches(doc, patterns.nouns)
nouns = [span for span in noun_results]

# dependency tree
words = []
for word in doc:
    if word.dep_ in 'nsubj':
        words.append(word)
        print(word.string)

nlp = test_spacy.load('en_core_web_sm')
text = "webkit is developed by Intel at the Intel Open Source Technology Center."
text = "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
text = "HSQLDB is supported by many Java frameworks"
text = "HSQLDB wordt ondersteund door menig Java frameworks"
text = "Pieter houdt van appels en bananen"
text = "Pieter houdt van appels en niet van bananen"
text = "In de toekomst gaan we naar de maan, Mars en de zon"
text = "PyTables is built on top of the HDF5 library, using the Python language and the NumPy package."
text = "PyTables is gebouwd op HDF5, met behulp van Python en het Numpy pakket."
text = "PyTables is gebouwd op HDF5, met behulp van Python en Numpy."
text = "PyTables is gebouwd in samenwerking met HDF5."
text = "Peter en Hendrik vinden geel mooi."  # cop
text = "Peter en Hendrik vinden geel heel mooi."  # cop
text = "Brood vind Peter erg lekker"
text = "De langdurige zorg blijkt zeer goed te werken"
text = "Pieter houdt niet altijd van appels"
text = "De langdurige zorg blijkt goed te werken voor ouderen"
text = "De kat werd gevolgd door de hond"
text = "De kat werd gevolgd door de hond en gezien door de rat"
text = "Peter en Iris blijken goed werk te verrichten"
text = "De auto is rood"
text = "Er is een geest in de kamer"
text = "Zij lopen en rennen precies in de maat"
text = "Ester is groot, maar Linda is klein"
text = "Bert en Ingrid zagen Ludo en Henk"
doc = nlp(text)
view_displacy(doc, port=8001)
