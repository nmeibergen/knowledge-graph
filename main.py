import os
import spacy
from triplehandler import TriplesDoc, process_coref
import stanfordnlp
from spacy_stanfordnlp import StanfordNLPLanguage
from my_logging import logger
from text import text
from coref import coref

nlp_model = "stanford"

# Run coref resolution
# 1. Run Alpino -> write to folder
# 2. Run coref resolution

# 1.
# * At 'knowledge_graph' folder run:
#   > sh alpino-docker/alpino.bash $PWD/alpino-parses
# * Write the parsed output to the output folder:
#   > ~/data partok input/test.txt | Alpino number_analyses=1 end_hook=xml -parse -flag treebank output
# 2.
# * At 'knowledge_graph' folder run:
# > python3 dutchcoref/coref.py --verbose alpino-parses/output

mentions, clusters = coref(path=f"{os.getcwd()}/../alpino-parses/output")

nlp = None
if nlp_model == "spacy":
    nlp = spacy.load('nl_core_news_sm')
elif nlp_model == "stanford":
    snlp = stanfordnlp.Pipeline(lang="nl")
    nlp = StanfordNLPLanguage(snlp)
else:
    logger("Incorrect nlp model has been chosen. Either select 'stanford' or 'spacy'.")
    exit()


if nlp is not None:
    doc = nlp(text)

    # view_displacy(doc)
    triples = TriplesDoc(doc=doc)
    triples()

    process_coref(triples=triples, coref_mentions=mentions, coref_clusters=clusters)

    print(triples)

    # Postprocessor for coreference resolution
    # 1. Allow creating stand-alone chunks in case that a chunk is refered to but not used in a triple. -> We then need
    # to call the complete function of the triple item.. maybe call that chunkitem?
    # 2. Find a way to create a data model for coreference, that is creating reference between two chunks.


    x = 1  # Allow for breakpoint

# Todo:
#  Implementation of NER or date with Spacy model -> Good to recognize dates and apply these to relationships