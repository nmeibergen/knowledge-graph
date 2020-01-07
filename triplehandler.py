from helperfunctions import set_pos_exceptions, index_of, nested_list_copy
from copy import copy
from my_logging import logger
from spacy.tokens import Token


class Chunk:

    def __init__(self):
        self.value = None
        self.last = None

    def generic_set(self, token, sub_item_name):
        assert(type(token).__name__ == "Token" or isinstance(token, str))

        # before adding the item, we complete it
        if isinstance(token, str):
            completed_value = [token]
        else:
            completed_value = self.complete(token)
        logger.info(f"Set triple item value: {completed_value}")
        setattr(self, sub_item_name, [completed_value])

    def generic_add(self, token, sub_item_name):
        current_val = getattr(self, sub_item_name)
        if current_val is None:
            self.generic_set(token,sub_item_name)
        else:
            current_val.append(self.complete(token))

    def generic_extend(self, token, sub_item_name):
        # If the current value is a string or token, then it can only be extended with the same types
        assert (type(token).__name__ == "Token" or isinstance(token, str) or token is None)

        current_val = getattr(self, sub_item_name)
        if current_val is None:
            # get set method
            set_method = getattr(self, f"set_{sub_item_name}", None)
            if set_method is not None:
                set_method(token)
        else:
            if isinstance(token, str):
                if not isinstance(current_val[-1], str):
                    mess = "Trying to add a string token to a Chunk that contains tokens of other types"
                    logger.error(mess)
                    exit(mess)
                completed_value = token
                current_val[-1].append(completed_value)
            if type(token).__name__ == "Token":
                if type(current_val[0][0]).__name__ != "Token":
                    mess = "Trying to add a string token to a Chunk that contains tokens of other types"
                    logger.error(mess)
                    exit(mess)

                completed_value = self.complete(token)
                current_val[-1].extend(completed_value)

    def set(self, value):
        if value is not None:
            if type(value).__name__ == type(self).__name__:
                self.Chunk_copy(fr=value, to=self)
            elif isinstance(value, str) or type(value).__name__ == "Token":
                self.set_value(token=value)

    def set_value(self, token):
        # # before adding the item, we complete it
        # completed_value = self.complete(token)
        # logger.info(f"Set triple item value: {completed_value}")
        # self.value = [completed_value]

        self.generic_set(token, sub_item_name="value")

        # Todo: This could be a decorator:
        self.last = "value"

    def add_value(self, token):
        # Add a new token to the Chunk, e.g.:
        # Paul en Pieter vinden geel mooi
        # Here the first noun should be the Chunk [Paul, Pieter] so that we get the Triple:
        # ([Paul, Pieter], [vinden mooi], [geel]) -> (Paul, vinden mooi, geel) and (Pieter, vinden mooi, geel)
        self.generic_add(token, "value")

    def extend_value(self, token):
        self.generic_extend(token, sub_item_name="value")

    def complete(self, token):
        value = [token]
        print(f"\n\ncomplete: {token.text}\n")
        logger.info(f"Start completion for token: {value[0].text}")
        for token_child in token.children:
            dependency = token_child.dep_.split(":")[0]
            if dependency == "compound":
                logger.info(f"> Compound completion: {value}")
                # "Zij lopen en rennen precies in de maat"
                # compound(in, de), compound(in, maat) -> in de maat
                value.extend(self.complete(token_child))

            if dependency == "flat":
                logger.info(f"> Flat completion: {value}")
                # "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
                # flat(Intel, Open), flat(Intel, Source), etc.
                value.extend(self.complete(token_child))

            if dependency == "amod":
                if token_child.pos_ != "ADV" and token.dep_ != "appos":
                    logger.info(f"> Amod completion: {value}")
                    # adjective modifier = toevoeging van bijvoeglijk naamwoord
                    # "De langdurige zorg blijkt zeer goed te werken"
                    # amod(zorg, langdurige)
                    value.extend(self.complete(token_child))

            if dependency == "advmod":
                # adverb = bijwoord, this relation may not be highly important to include
                # however, in some cases it is very important, e.g. Dementie is echter nog niet verholpen, now:
                # advmod(verholpen, niet), advmod(verholpen, echter), advmod(niet, nog)
                # in this case, "niet verholpen" is very important to retrieve! However, echter and nog, seem redudant
                # Todo:
                #  We thus may need a removal of stopwords!

                # "De langdurige zorg blijkt zeer goed te werken"
                # advmod(zeer, goed)
                if token_child.pos_ == "ADV":
                    logger.info(f"> Advmod completion: {value}")
                    # We only include the adverb if it contains an important value, such as denials
                    adv_value = self.complete(token_child)
                    has_important_adv = adv_value in ["niet", "geen", "nooit"]
                    if has_important_adv:
                        value = value.extend(adv_value)

            if dependency == "aux":
                if token.pos_ == "VERB":
                    logger.info(f"> Aux completion: {value}")
                    # "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
                    # aux(ontwikkeld, is)
                    value.extend(self.complete(token_child))

            # if dependency == "mark":
            #     # "De langdurige zorg blijkt zeer goed te werken"
            #     # mark(werken, te)
            #     logger.info(f"> Mark completion: {value}")
            #     value.extend(self.complete(token_child))

            if dependency == "fixed":
                value.extend(self.complete(token_child))

            if dependency == "appos":
                if token_child.pos_ == "NUM":
                    # text = "Afwisselende democratische en autocratische regeringen volgden elkaar op tot in de jaren
                    # 80 van de twintigste eeuw"
                    # appos(jaren, 80)
                    value.extend(self.complete(token_child))

            if dependency == "nmod_obsolete":
                # The nmod is only used as completion if it the token doesn't have a case dependency.
                # Hij is president van zuid-amerika
                # nmod(president, zuid-amerika)
                # -> triples: (hij, is, president) and (hij, is president van, zuid-amerika)
                if not any([tok.dep_ == "case" for tok in token_child.children]):
                    value.extend(self.complete(token_child))

            if dependency == "nmod":
                print(f"NMOD: {token_child.text}")
                value.extend(self.complete(token_child))

            if dependency == "nummod":
                value.extend(self.complete(token_child))

            if dependency == "case":
                if token.dep_ == "nmod":
                    value.extend(self.complete(token_child))

        return value

    def is_empty(self):
        if self.value is None:
            return True
        else:
            return False

    def get_last_method(self, method_type="set"):
        if method_type is not "set" and method_type is not "add":
            logger.error("method_type must be 'set' or 'add'.")
            exit()

        if self.last is not None:
            assert(isinstance(self.last, str))
            last_method = getattr(self, method_type + "_" + self.last, None)
            return last_method

    def set_last(self, token):
        last_method = self.get_last_method(method_type="set")
        if last_method is not None:
            last_method(self, token)
        else:
            logger.info(f"Last method could not be identified: '{self.last}'")

    def add_last(self, token):
        last_method = self.get_last_method(method_type="add")
        if last_method is not None:
            last_method(token)
        else:
            logger.info(f"Last method could not be identified: '{self.last}'")

    @staticmethod
    def sorted_token_values(tokens):
        assert (isinstance(tokens, list) or tokens is None)
        if tokens is not None and len(tokens) > 0:
            if isinstance(tokens[0], str):
                return ' '.join(tokens)
            elif type(tokens[0]).__name__ == "Token":
                sorted_vals = sorted(tokens, key=lambda x: x.i)
                sorted_strings = [token.text.lower() for token in sorted_vals]
                return ' '.join(sorted_strings)
            else:
                mess = "The type of tokens is neither string nor Token"
                logger.error(mess)
                exit(mess)
        else:
            return ""

    @staticmethod
    def subitem_to_string(sub_item):
        if sub_item is not None:
            sorted_vals = [Chunk.sorted_token_values(tokens) for tokens in sub_item]
            if len(sorted_vals) > 1:
                sorted_vals = "[" + ', '.join(sorted_vals) + "]"
            else:
                sorted_vals = sorted_vals[0]
            return sorted_vals
        else:
            return ""

    @staticmethod
    def Chunk_copy(fr, to=None):
        """
        Copy the from Chunk to the to Chunk
        :param fr: Chunk
        :param to: Chunk or None
        :return: Chunk
        """
        if to is None:
            to = type(fr)()

        # both items must of the same type
        assert(type(to).__name__ == type(fr).__name__)

        to.__dict__ = fr.__dict__.copy()

        # Perform in between shallow and deep copy: extract content of (nested)lists
        for key, val in fr.__dict__.items():
            if isinstance(val, list):
                to.__dict__[key] = nested_list_copy(item=val)

        return to

    def __copy__(self):

        return self.Chunk_copy(self)


class Noun(Chunk):
    def __init__(self):
        super().__init__()
        self.nmod = None

    def set_nmod(self, token):
        self.generic_set(token, "nmod")
        self.last = "nmod"

    def add_nmod(self, token):
        self.generic_add(token, "nmod")
        self.last = "nmod"

    def __str__(self):

        sorted_values = self.subitem_to_string(self.value)
        sorted_nmod = self.subitem_to_string(self.nmod)

        if sorted_nmod != "":
            sorted_nmod = " " + sorted_nmod

        return f"{sorted_values}{sorted_nmod}"


class Verb(Chunk):

    def __init__(self):
        super().__init__()
        self.cop = None
        self.obj = None
        self.case = None
        self.xcomp = None

    def collect_to_value(self):
        # Todo:
        #  For now we refer only to the last element of the cop/obj, etc. however it may be such that we need to refer
        #  to multiple! Something to look into.
        #  e.g. Hij werkt in en bij het bedrijf van zijn vader.
        #  -> (hij, werkt in, bedrijf), (hij, werkt bij, bedrijf)
        #  -> (hij, werkt in bedrijf van, vader), (hij, werkt bij bedrijf, vader)
        if self.value is not None:
            if self.cop is not None:
                self.value[-1].extend(c for c in self.cop[-1])

            if self.obj is not None:
                self.value[-1].extend(c for c in self.obj[-1])

            if self.xcomp is not None:
                self.value[-1].extend(c for c in self.xcomp[-1])

            if self.case is not None:
                self.value[-1].extend(c for c in self.case[-1])

        self.cop = None
        self.case = None
        self.obj = None

    def set_cop(self, token):
        self.generic_set(token, "cop")
        self.last = "cop"

    def set_obj(self, token):
        self.generic_set(token, "obj")
        self.last = "obj"

    def set_case(self, token):
        self.generic_set(token, "case")
        self.last = "case"

    def set_xcomp(self, token):
        self.generic_set(token, "xcomp")
        self.last = "xcomp"

    def add_cop(self, token):
        self.generic_add(token, "cop")
        self.last = "cop"

    def add_obj(self, token):
        self.generic_add(token, "obj")
        self.last = "obj"

    def add_case(self, token):
        self.generic_add(token, "case")
        self.last = "case"

    def add_xcomp(self, token):
        self.generic_add(token, "xcomp")
        self.last = "xcomp"

    def __str__(self):
        sorted_values = self.subitem_to_string(self.value)
        sorted_case = self.subitem_to_string(self.case)
        sorted_cop = self.subitem_to_string(self.cop)
        sorted_obj = self.subitem_to_string(self.obj)

        if sorted_case != "":
            sorted_case = " " + sorted_case
        if sorted_cop != "":
            sorted_cop = " " + sorted_cop
        if sorted_obj != "":
            sorted_obj = " " + sorted_obj

        # order of words:
        # text = "Brazilië is met zijn 8,5 miljoen vierkante kilometer het grootste land van Zuid-Amerika, het beslaat
        # bijna de helft van dit continent."
        # cop(is, land), case(zuid-amerika, van)
        # For the verb Chunk: value = is, cop = grootste land, case = met/van

        return f"{sorted_values}{sorted_cop}{sorted_obj}{sorted_case}".lower()


class Triple:

    # at initialization you may provide strings
    def __init__(self, noun1=None, verb=None, noun2=None):
        logger.info(f"Initiate new triple")
        self.noun1 = Noun()
        self.verb = Verb()
        self.noun2 = Noun()

        # test approach
        if noun1 is not None:
            self.noun1.set(noun1)

        if verb is not None:
            self.verb.set(verb)

        if noun2 is not None:
            self.noun2.set(noun2)

    def set_noun1(self, token):
        self.noun1.set_value(token)
        self.last_noun = self.noun1
        self.last = self.noun1

    def set_verb(self, token):
        self.verb.set_value(token)
        self.last_verb = self.verb
        self.last = self.verb

    def set_noun2(self, token):
        self.noun2.set_value(token)
        self.last_noun = self.noun2
        self.last = self.noun2

    def add_to_last_noun(self, token):
        self.last_noun.extend_value(token)

    def add_to_last_verb(self, token):
        self.last_verb.extend_value(token)

    def set_to_last(self, token):
        # self.last
        pass

    def is_valid(self):
        if self.noun1.is_empty() or self.verb.is_empty() or self.noun2.is_empty():
            return False

        return True

    def __str__(self):
        # perfom combining of the triples and return list of triples
        if self.is_valid():
            return f"({self.noun1.__str__()}, {self.verb.__str__()}, {self.noun2.__str__()})"

        return ""


def proceed(f):
    def wrapper_f(*args, **kwargs):
        logger.info(f"Execute: {f.__name__}")

        # class that is requesting
        cls = args[0]

        dependency_trace = ()
        if "dependency_trace" in kwargs:
            dependency_trace = kwargs['dependency_trace']

        if "token_head" in kwargs:
            logger.info(f"> token_head: {kwargs['token_head']}")
            kwargs['dependency_trace'] = dependency_trace + (kwargs['token_head'].dep_,)

        logger.info(f"> token: {kwargs['token']}")

        proceed_requested = f(*args, **kwargs)
        if proceed_requested:
            # proceed to call dependency functions on next children
            kwargs["token_head"] = kwargs["token"]

            # Todo:
            #  Catch multiple occurrences of nsubj and cop

            # The compound is included at the 'start' for it may need to complete verbs before going on to setting the
            # nouns, e.g.
            # text = "In 1968 sloot hij zich officieel bij zijn vaders bedrijf aan", verb = "sloot aan", then we can set
            # noun2 as 1968, where the case "in" is added to "sloot aan", creating: (hij, sloot aan in, 1968)

            # The obj needs to come before the obl, because the obj induces two triples, one where it is simply the
            # second noun and another were it is added as obj to the verb.

            # aux before cop: hij bleek populair te zijn -> aux(populair, bleek), cop(populair, zijn)
            # If the cop comes before auc: the cop will create triple (hij, zijn, populair) and then set populair as
            # cop to make the next triples: (hij, zijn populair, ..)
            # here we actually want to have (hij, bleek zijn, populair) and (hijm bleek zijn populair, ..)

            dependency_order = ["nsubj", "aux", "cop", "compound", "case", "obj", "nmod", "xcomp", "obl", "conj"]
            children = [next_child for next_child in kwargs["token"].children]
            sorted_children = sorted(children, key=lambda x: index_of(val=x.dep_, in_list=dependency_order, value_if_not_exists=1e4))

            for next_child in sorted_children:
                next_dependency = next_child.dep_.split(":")[0]
                proceed_method = getattr(cls, next_dependency, None)
                if proceed_method is not None:
                    logger.info(f"> Next method: {next_dependency}")
                    kwargs["token"] = next_child
                    proceed_method(**kwargs)

    return wrapper_f


class TriplesDoc:

    def __init__(self, doc=None):

        doc = set_pos_exceptions(doc=doc)

        Token.set_extension("sent_id", default=None)
        Token.set_extension("token_id", default=None)

        for sent_id, sent in enumerate(doc.sents):
            for token_id, token in enumerate(sent):
                token._.sent_id = sent_id
                token._.token_id = token_id

        self.doc = doc
        self.sentences = None
        self.dependencies_per_sentence = None
        self.triples = []
        self.triple = None  # refers to the current triple in use

    def __call__(self, *args, **kwargs):
        # triple builder
        for token in self.doc:
            if token.dep_.lower() == "root":
                self.root(token=token)

    def _start_new_triple(self, noun1=None, verb=None, noun2=None, set_as_current=True):
        triple = Triple(noun1=noun1, verb=verb, noun2=noun2)
        self.triples.append(triple)

        # We start a new triple which we want to set as the current such that it can be used in the next stages
        if set_as_current:
            self.triple = self.triples[-1]

    def root_method(self, token, *args, **kwargs):
        # we do not need to split for sentences if we initialize for each root,
        # which is - I expect - defined for each sentence
        if token.pos_ == "VERB":
            self._start_new_triple()
            self.triple.set_verb(token)
        else:
            self._start_new_triple()
            self.triple.set_noun2(token)

        return True

    @proceed
    def root(self, token, *args, **kwargs):
        return self.root_method(token, args, kwargs)

    @proceed
    def nsubj(self, token, *args, **kwargs):
        # returns the noun
        # Look into starting a new triple when noun1 is not empty.
        # The below code uses the nsubj to also set noun2 if noun1 is empty, however, I am not sure in what case that
        # makes sense
        if self.triple.noun1.is_empty():
            self.triple.set_noun1(token)
            return True
        elif self.triple.noun2.is_empty():
            self.triple.set_noun2(token)
            return True
        return False

    def generic_obl(self, token_head, token, *args, **kwargs):
        # Applying the obl relation only makes sense if the value we are pointing at is a NOUN or NUM
        # if token.pos_ == "NOUN" or token.pos_ == "NUM":
        #     if self.triple.noun2.is_empty():
        #         self.triple.set_noun2(token)
        #     elif token_head.pos_ == "NOUN":
        #         # text = "Van beroep was hij ondernemer, voornamelijk in het vastgoed"
        #         # cop(ondernemer, was), nsubj(ondernemer, hij) -> (hij, was, ondernemer)
        #         # but also: (hij, was ondernemer van, beroep)
        #         # --> obl(ondernemer, beroep), therefore
        #         self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
        #         self.triple.verb.set_cop(token_head)
        #         self.triple.set_noun2(token)
        #     else:
        #         self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
        #         self.triple.set_noun2(token)
        #     return True
        # return False
        if self.triple.noun2.is_empty():
            self.triple.set_noun2(token)
        elif token_head.pos_ == "NOUN":
            # text = "Van beroep was hij ondernemer, voornamelijk in het vastgoed"
            # cop(ondernemer, was), nsubj(ondernemer, hij) -> (hij, was, ondernemer)
            # but also: (hij, was ondernemer van, beroep)
            # --> obl(ondernemer, beroep), therefore
            self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
            # Todo
            #  fix bug where copying of properties in triples also occurs on previous triples..
            self.triple.verb.set_cop(token_head)
            self.triple.set_noun2(token)
        else:
            self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
            self.triple.set_noun2(token)
        return True

    @proceed
    def obl(self, token_head, token, *args, **kwargs):
        return self.generic_obl(token_head, token, *args, **kwargs)

    @proceed
    def obj(self, token_head, token, *args, **kwargs):
        # return self.generic_obl(token_head, token, *args, **kwargs)
        # example:
        # she gave me a raise.
        # obj(gave, raise) -> the verb is 'gave raise'

        # Here we see two triples:
        # 1. (she, gave, raise)
        # 2. (she, gave raise, me)
        self.triple.set_noun2(token)
        self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)

        # 2.
        self.triple.verb.set_obj(token)
        return True

    @proceed
    def xcomp(self, token_head, token, *args, **kwargs):
        return self.generic_obl(token_head, token, *args, **kwargs)

    @proceed
    def conj(self, token_head, token, *args, **kwargs):

        child_deps = [token_child.dep_.split(":")[0] for token_child in token.children]
        head_deps = [token_child.dep_.split(":")[0] for token_child in token_head.children]
        if (any([dep == "nsubj" or
                 dep == "aux" or
                 dep == "obl" or
                 dep == "obj"
                 for dep in child_deps])):
            # We identify the start of a new root, and therefore we follow the same approach as the root does:
            return self.root_method(token, args, kwargs)

            # This conj functions like the start of a new triple, more like a parataxis
            # self._start_new_triple(noun1=self.triple.noun1)
            # self.triple.set_verb(token)
        elif token_head.pos_ == "VERB":
            self.triple.verb.add_last(token)
        elif any([dep == "nsubj" for dep in head_deps]):
            self.triple.noun1.add_last(token)
        else:
            if self.triple.noun1 == self.triple.last_noun:
                self.triple.noun1.add_last(token)
            if self.triple.noun2 == self.triple.last_noun:
                self.triple.noun2.add_last(token)
        return True

    @proceed
    def cop(self, token_head, token, *args, **kwargs):

        if token.pos_ == "VERB" or token.pos_ == "AUX":
            # Todo:
            #  Catch the case in which we have no noun1 set yet at this point.. should be the case! Furthemore we have
            #  set to always first perform nsubj followed by cop, and the nsubj should set noun1.

            # "Peter en Hendrik vinden geel mooi, en blauw lelijk"
            # cop(mooi, vinden) -> verb1 = vinden mooi
            # conj(mooi, lelijk) -> verb2 = vinden lelijk
            # thus, in the conjoint we need to remember vinden from the cop relation and make the second part, that is,
            # mooi and lelijk, the flexible part of the verb, i.e. the case part
            # self.triple.set_verb(token)
            # verbform = "VerbForm=Fin"  # indicator of VERB used as VERB (if the form is Inf then it is actually a
            # noun)
            # if verbform in token_head.tag_:
            #     self.triple.verb.set_cop(token_head)
            # else:
            #     self.triple.set_noun2(token_head)
            # return True
            if token_head.pos_ == "VERB":
                self.triple.set_verb(token)
                self.triple.verb.set_cop(token_head)
            else:
                # for example:
                # text = "Van beroep was hij ondernemer"
                # cop(ondernemer, was)
                # obl(ondernemer, beroep)

                # triple(hij, was, ondernemer)
                self.triple.verb.extend_value(token)

                # Note that noun2 has already been set at this stage for it is the token we are coming from, which is
                # already handled and set as noun2
                for_cop = self.triple.noun2.value
                self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
                self.triple.verb.cop = copy(for_cop)
                # self.triple.verb.set_cop(for_cop)


                # self.triple.set_verb(token)
                # self.triple.set_noun2(token_head)
                #
                # # triple(hij, was ondernemer van, beroep)
                # self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
                # self.triple.verb.set_cop(token_head)

                # Todo:
                #  Check whether it is generically true that we are more interested in the triple
                #  (hij, was van beroep, ondernemer). If so, we need to find a way to incorporate this approach..
                #  It would mean that the obl relation in this case adds something to the verb instead of to the noun.
            return True
        else:
            # If we are pointing with cop to a word that is not a VERB, than clearly something has gone wrong in the NLP
            # model, as this should always be a VERB and we stop the process here.
            return False

    @proceed
    def nmod_obsolete(self, token_head, token, *args, **kwargs):
        # If there is a case dependency on this nmod token, then we identify this token as obl
        if any([tok.dep_ == "case" for tok in token.children]):
            case_token = [tok for tok in token.children if tok.dep_ == "case"][0]
            if token_head.pos_ == "NOUN":
                if self.triple.noun1 is self.triple.last_noun:
                    self.triple.noun1.extend_value(token)
                    self.triple.noun1.extend_value(case_token)
                elif self.triple.noun2 is self.triple.last_noun:
                    # Todo:
                    #  Use last_noun!!
                    # self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
                    #
                    # self.triple.verb.collect_to_value()
                    # # self.triple.verb.set_cop(token_head)
                    # self.triple.set_noun2(token)

                    noun2 = copy(self.triple.noun2)
                    self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb, noun2=noun2)

                    # We can get at this point either because of a nmod before this point, an obj or an obl.
                    # In case of an nmod, we have set the previous token as obj and we proceed
                    # Same for obj
                    # When we come from obl, the end point of obl is setting the noun, therefore we check if the noun2
                    # element is empty, if it is not, we set that as obj
                    if not noun2.is_empty():
                        for noun in noun2.value:
                            self.triple.verb.add_obj(noun[0])
                        # self.triple.verb.set_obj(noun2.value)

                    self.triple.verb.collect_to_value()
                    self.triple.set_noun2(token)
                    self.case_method(token=case_token)

                    self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
                    self.triple.verb.collect_to_value()
                    self.triple.verb.set_obj(token)
                    # else:
                    #     self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
                    #     self.triple.set_noun2(token)
                else:
                    pass
            return True
        else:
            return False

    def case_method(self, token, *args, **kwargs):
        self.triple.verb.set_case(token)

    @proceed
    def case(self, token_head, token, *args, **kwargs):
        # Do not perform this proceed case approach if token_head has the nmod dependency, for this is handled in the
        # nmod dependency procceed function... bleh, time for code cleaning!
        if token_head.dep_ != "nmod":
            self.case_method(token=token)
        return False

    @proceed
    def xcomp_obsolete(self, token_head, token, *args, **kwargs):
        # text = "Langdurige zorg blijkt zeer goed te werken"
        # Here blijkt is a verb with Verbform=Inf, thus it functions as a Noun, and we have set it as a Noun with the
        # exceptions. In this case we thus need to refer to the tag, and in particular the first item when splitting on
        # the |. This indicates V, for verb.
        if token_head.pos_ == "VERB":# and token.pos_ == "VERB":
            self.triple.verb.extend_value(token)
            return True

    @proceed
    def aux(self, token_head, token, *args, **kwargs):
        if token_head.pos_ is not "VERB":
            # the aux may also function as a verb completer, if so the verb previously added should already have been
            # completed with the aux
            self.triple.verb.extend_value(token)

    @proceed
    def appos(self, token_head, token, *args, **kwargs):
        if token_head.pos_ == "NOUN" and token.pos_ == "NOUN":
            self._start_new_triple(noun1=self.triple.noun1, verb="synoniem", noun2=token, set_as_current=False)
        return False

    @proceed
    def parataxis(self, token_head, token, *args, **kwargs):
        # Start new triple
        return self.root_method(token)

        # if token_head.pos_ == "VERB":
        #     # text = "Brazilië is met zijn 8,5 miljoen vierkante kilometer het grootste land van Zuid-Amerika, het
        #     # beslaat bijna de helft van dit continent."
        #     # parataxis(land, beslaat)
        #     # -> land fuctions as a verb.
        #     # 1. Brazilie is grootste land (we have cop(land, is))
        #     # 2. Brazilie beslaat .., thus remain noun1 and set new verb
        #     self._start_new_triple(noun1=self.triple.noun1)
        #     self.triple.set_verb(token)
        #     return True

    def __str__(self):
        striples = []
        for triple in self.triples:
            striple = triple.__str__()
            if striple != "":
                striples.append(striple)

        return "\n".join(striples)


def process_coref(triples, coref_mentions, coref_clusters):
    # Filter on relevant mentions
    # These are
    # - pronoun resolutions
    # - strict head match 5
    sieves = ["pronounresolution", "strictheadmatch:5", None]
    coref_mentions = [mention for mention in coref_mentions if mention.sieve in sieves]
