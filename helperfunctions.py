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

            #token.pos_ = "VERB"
            pass

    return doc


def print_grammer(doc):
    for token in doc:
        print(f"{token.string} --> tag: {token.tag_} + pos: {token.pos_} + dep: {token.dep_}")


def view_displacy(doc, style='dep', port=8002):
    displacy.serve(doc, style=style, port=port)


def index_of(val, in_list, value_if_not_exists=-1):
    try:
        return in_list.index(val)
    except ValueError:
        return value_if_not_exists


def nested_list_copy(item):
    """
    Requires that the item itself is of any of the proceed_on classes
    :param item:
    :return:
    """
    if isinstance(item, list):
        # Check if the list has sublists
        copied_list = []
        if any(isinstance(sub_item, list) for sub_item in item):
            sublist = []
            for sub_item in item:
                sublist.extend(nested_list_copy(sub_item))

            copied_list.extend(sublist.copy())

        else:
            copied_list.append(item.copy())

        return copied_list
    else:
        # Throw warning, no list provided and will not perform copying
        return item


def nested_copy(fr, to=None, proceed_on=None):
    """
    Copy the from MultiChunk to the to MultiChunk
    :param fr: MultiChunk
    :param to: MultiChunk or None
    :param proceed_on: list of classes on which to proceed the nested copy
    :return: MultiChunk
    """
    if to is None:
        to = type(fr)()

    if proceed_on is None:
        proceed_on = [list]

    # both items must of the same type
    assert(type(to).__name__ == type(fr).__name__)

    to.__dict__ = fr.__dict__.copy()

    # Perform in between shallow and deep copy: extract content of (nested)lists
    for key, val in fr.__dict__.items():
        if any(isinstance(val, proceed_class) for proceed_class in proceed_on):
            to.__dict__[key] = nested_list_copy(item=val)

    return to
