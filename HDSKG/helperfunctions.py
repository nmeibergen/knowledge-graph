from spacy import displacy


def set_pos_exceptions(doc):
    for token in doc:
        verbform = "VerbForm=Inf"
        if verbform in token.tag_:
            #token.pos_ = "NOUN"
            pass
        if any([token_child.dep_ == "cop" for token_child in token.children]):
            # text = "Brazilië is medeoprichter van de Verenigde Naties."
            # Here cop(medeoprichter, is)
            # also, because medeoprichter is actually a Noun, the relation from medeoprichter to Verenigde Naties is an
            # nmod, i.e. nmod(medeoprichter, Verenigde). However, because medeoprichter functions as part of the larger
            # verb "is medeoprichter van" we need to identify that the nmod works as the obl relation. We will apply the
            # obl approach if the token_head is of the type VERB. Therefore we set to verb.
            token.pos_ = "VERB"

    return doc


def print_grammer(doc):
    for token in doc:
        print(f"{token.string} --> tag: {token.tag_} + pos: {token.pos_} + dep: {token.dep_}")


def view_displacy(doc, style='dep', port=8002):
    displacy.serve(doc, style=style, port=port)