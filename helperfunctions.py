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

    #
    #     for sub_item in item:
    #         if any(isinstance(subsub_item, list) for subsub_item in sub_item):
    #             copied_subsub = []
    #             for subsub_item in sub_item:
    #                 if isinstance(sub_item, list):
    #                     copied_list.append(nested_list_copy(sub_item))
    #             else:
    #             copied_sub = [value.copy() for value in sub_item]
    #         else:
    #             copied_list.append(sub_item.copy())
    #
    #     return copied_list
    # elif item is None:
    #     return None
    # else:


test = [[1, 2], [4, [5]]]
