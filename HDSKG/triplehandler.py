from .helperfunctions import set_pos_exceptions
from copy import copy
from my_logging import logger


def get_triple_first_nouns(sentence_dependencies):
    # asure not more than one nsubj relation
    return 1


def get_triple_verb(self):
    pass


def get_triple_second_nouns(self):
    pass


class TripleItem:
    value = ""
    cop = ""
    obj = ""
    case = ""

    def set(self, token):
        # before adding the item, we complete it
        completed_value = self.complete(token)
        logger.info(f"Set triple item value: {completed_value}")
        self.value = completed_value
    
    def set_cop(self, token):
        completed_value = self.complete(token)
        logger.info(f"Set triple item cop: {completed_value}")
        self.cop = completed_value

    def set_obj(self, token):
        completed_value = self.complete(token)
        logger.info(f"Set triple item obj: {completed_value}")
        self.obj = completed_value

    def set_case(self, token):
        completed_value = self.complete(token)
        logger.info(f"Set triple item case: {completed_value}")
        self.case = completed_value

    def prepend(self, token):
        # before prepending the item, we complete it
        completed_value = self.complete(token)
        logger.info(f"Prepend triple item value: {completed_value}")
        if self.value != "":
            self.value = " " + self.value
        self.value = f"{completed_value}{self.value}"

    def append(self, token):
        # before appending the item, we complete it
        completed_value = self.complete(token)
        logger.info(f"Append triple item value: {completed_value}")
        if self.value != "":
            self.value = self.value + " "
        self.value = f"{self.value}{completed_value}"

    def complete(self, token):
        value = token.text
        logger.info(f"Start completion for token: {value}")
        for token_child in token.children:
            dependency = token_child.dep_.split(":")[0]
            if dependency == "compound":
                logger.info(f"> Compound completion: {value}")
                # "Zij lopen en rennen precies in de maat"
                # compound(in, de), compound(in, maat) -> in de maat
                value = f"{value} {self.complete(token_child)}"

            if dependency == "flat":
                logger.info(f"> Flat completion: {value}")
                # "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
                # flat(Intel, Open), flat(Intel, Source), etc.
                value = f"{value} {self.complete(token_child)}"

            if dependency == "amod":
                logger.info(f"> Amod completion: {value}")
                # adjective modifier = toevoeging van bijvoeglijk naamwoord
                # "De langdurige zorg blijkt zeer goed te werken"
                # amod(zorg, langdurige)
                value = f"{self.complete(token_child)} {value}"

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
                    has_important_adv = adv_value in ["niet", "geen"]
                    if has_important_adv:
                        value = f"{adv_value} {value}"

            if dependency == "aux":
                if token.pos_ == "VERB":
                    logger.info(f"> Aux completion: {value}")
                    # "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
                    # aux(ontwikkeld, is)
                    value = f"{self.complete(token_child)} {value}"

            if dependency == "mark":
                # "De langdurige zorg blijkt zeer goed te werken"
                # mark(werken, te)
                logger.info(f"> Mark completion: {value}")
                value = f"{self.complete(token_child)} {value}"

            if dependency == "appos":
                if token_child.pos_ == "NUM":
                    # text = "Afwisselende democratische en autocratische regeringen volgden elkaar op tot in de jaren
                    # 80 van de twintigste eeuw"
                    # appos(jaren, 80)
                    value = f"{value} {self.complete(token_child)}"

            if dependency == "case":
                # We need to handle a special case here:
                # 1. text = "Brazilië is met zijn 8,5 miljoen vierkante kilometer het grootste land van Zuid-Amerika,
                # het beslaat bijna de helft van dit continent."
                # > Here a triple is (brazilie, grootste land van, zuid-amerika)
                # 2. text = "De oorspronkelijke bevolking van Brazilië bestond uit indianen die de tropische kuststrook,
                # het Paraná- en het Amazonebekken bewoonden."
                # > Here a triple is (oorspronkelijke bevolking van Brazilië, bestond uit, indianen)
                # In 1) we have nmod(land, zuid-amerika) and case(zuid-amerika, van)
                # In 2) we have nmod(bevolking, brazilie) and case(brazilie, van)
                # In the first we add the van to the 'verb' land (it is identified as verb) and in the second case we
                # need to complete bevlking van Brazilie, so 'van' should not be added to the verb, instead, here it is
                # a completion. We thus note that completion should be done if the head of the token we are looking at
                # is not a verb, for if it is, then case should be appending the verb
                if token.head.pos_ != "VERB":
                    value = f"{self.complete(token_child)} {value}"

        return value

    def is_empty(self):
        if self.value == "":
            return True
        else:
            return False

    def __str__(self):
        value = self.value
        case = self.case
        cop = self.cop
        obj = self.obj
        if case != "":
            case = f" {case}"
        if cop != "":
            cop = f" {cop}"
        if obj != "":
            obj = f" {obj}"

        # order of words:
        # text = "Brazilië is met zijn 8,5 miljoen vierkante kilometer het grootste land van Zuid-Amerika, het beslaat
        # bijna de helft van dit continent."
        # cop(is, land), case(zuid-amerika, van)
        # For the verb tripleitem: value = is, cop = grootste land, case = met/van

        return f"{value}{cop}{obj}{case}"


class Triple:

    last_noun = None
    last_verb = None

    # at initialization you may provide strings
    def __init__(self, noun1=None, verb=None, noun2=None):
        logger.info(f"Initiate new triple")
        assert(type(noun1).__name__ == "TripleItem" or noun1 is None)
        assert(type(verb).__name__ == "TripleItem" or verb is None)
        assert(type(noun2).__name__ == "TripleItem" or noun2 is None)

        self.noun1 = TripleItem()
        self.verb = TripleItem()
        self.noun2 = TripleItem()

        if noun1 is not None:
            logger.info(f"> init with noun1: {noun1.value}")
            self.noun1 = copy(noun1)
        if verb is not None:
            logger.info(f"> init with verb (case): {verb.value} ({verb.case})")
            self.verb = copy(verb)
        if noun2 is not None:
            logger.info(f"> init with noun2: {noun2.value}")
            self.noun2 = copy(noun2)

    def set_noun1(self, token):
        self.noun1.set(token)
        self.last_noun = self.noun1

    def set_verb(self, token):
        self.verb.set(token)
        self.last_verb = self.verb

    def set_noun2(self, token):
        self.noun2.set(token)
        self.last_noun = self.noun2

    def add_to_last_noun(self, token, add_type="append"):
        if add_type == "append":
            self.last_noun.append(token)
        elif add_type == "prepend":
            self.last_noun.prepend(token)

    def add_to_last_verb(self, token, add_type="append"):
        if add_type == "append":
            self.last_verb.append(token)
        elif add_type == "prepend":
            self.last_verb.prepend(token)
    
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
            for next_child in kwargs["token"].children:
                next_dependency = next_child.dep_.split(":")[0]
                proceed_method = getattr(cls, next_dependency, None)
                if proceed_method is not None:
                    logger.info(f"> Next method: {next_dependency}")
                    kwargs["token"] = next_child
                    proceed_method(**kwargs)

    return wrapper_f


class TriplesDoc:
    doc = None
    sentences = None
    dependencies_per_sentence = None
    triples = []
    triple = None # refers to the current triple in use

    def __init__(self, doc):

        doc = set_pos_exceptions(doc=doc)
        self.doc = doc

    def __call__(self, *args, **kwargs):
        # triple builder
        for token in self.doc:
            if token.dep_ == "ROOT":
                self.root(token=token)

    def _start_new_triple(self, noun1=None, verb=None, noun2=None):
        triple = Triple(noun1=noun1, verb=verb, noun2=noun2)
        self.triples.append(triple)
        self.triple = triple # set new triple in current use

    @proceed
    def root(self, token, *args, **kwargs):
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
    def nsubj(self, token, *args, **kwargs):
        # returns the noun
        if self.triple.noun1.is_empty():
            self.triple.set_noun1(token)
            return True
        elif self.triple.noun2.is_empty():
            self.triple.set_noun2(token)
            return True
        return False

    def generic_obl(self, token_head, token, *args, **kwargs):
        # if token_head.pos_ == "VERB":
        #     # if the second noun already has data, then clearly this is another noun, and we should initiate such
        #     if self.triple.noun2.is_empty():
        #         self.triple.set_noun2(token)
        #     else:
        #         self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
        #         self.triple.set_noun2(token)
        #     return True
        # else:
        #     # this indicates that we have another triple with this particular noun
        #     self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
        #     self.triple.set_noun2(token)
        #     return True

        # text = "Brazilië is met zijn 8,5 miljoen vierkante kilometer het grootste land van Zuid-Amerika, het beslaat
        # bijna de helft van dit continent."
        # obl(is, miljoen) -> triple(Brazilie, is grootste land met, 8,5 miljoen vierkante kilometer)
        # nmod(land, zuid-amerika) -> triple(Brazilie, is grootste land van, zuid-amerika)
        # thus clearly the obl indicator can create new triples, in this case if the nmod would have come first.
        if self.triple.noun2.is_empty():
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
        # However we see that the model does not accurately predicts the obj, instead it very often should be the obl
        # e.g. text = "De oorspronkelijke bevolking van Brazilië bestond uit indianen die de tropische kuststrook, het
        # Paraná- en het Amazonebekken bewoonden."
        # Here: obj(bestond, indianen), clearly we need
        #   the triple (oorspronkelijke bevolking brazilie, bestond uit, indianen)
        # self.triple.noun2.set_obj(token)
        # return True
        return self.generic_obl(token_head, token, *args, **kwargs)

    @proceed
    def nmod(self, token_head, token, *args, **kwargs):
        # We will not include PRON
        if token.pos_ != "PRON":
            if token_head.pos_ == "VERB":
                self.triple.set_noun2(token)
                return True  # we need to be able to add the case
            elif token_head.pos_ == "NOUN":
                self.triple.add_to_last_noun(token)
                # the noun has been modified, now proceeding is stopped
                return False
        # if token_head.pos_ == "VERB":
        #     return self.generic_obl(token_head, token, *args, **kwargs)

    @proceed
    def conj(self, token_head, token, *args, **kwargs):

        if token_head.pos_ == "VERB" and token.pos_ == "VERB":
            # This means that we start some new relationship for the first noun, e.g.
            # text = "De Portugese Kroon breidde haar heerschappij echter niet uit en in 1808 verhuisde de Portugese
            # hofhouding van Lissabon naar Rio de Janeiro"
            # > Here "De Portugese KLroon" did two things: 1. they "breide uit" and 2. they "verhuisde"
            self._start_new_triple(noun1=self.triple.noun1)
            self.triple.set_verb(token)
            return True
        elif any([token_child.dep_ == "cop" for token_child in token_head.children]):
            # "Peter en Hendrik vinden geel mooi, en blauw lelijk"
            # cop(mooi, vinden)
            # conj(mooi, lelijk)
            # we already have the triple (Peter, vinden mooi, geel), now we pass onto the next triple
            # (Peter, vinden mooi, ..). noting that mooi and lelijk are the case part, we immediately replace the case
            # with lelijk
            self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
            self.triple.verb.set_cop(token)
            return True
        elif any([token_child.dep_ == "nsubj" for token_child in token.children]):
            # First we note that if there is a nsubj dependency from this token, then this is not a conjoint but the
            # start of a new triple, e.g. Ester is groot en Linda is klein. Here groot and klein are connected with
            # conj, but from both groot and klein we have an nsubj relation indicating two subjects

            # start new triple
            self._start_new_triple()
            self.triple.set_noun2(token)
            return True
        elif "dependency_trace" in kwargs:
            trace = kwargs["dependency_trace"]
            if "nsubj" in trace:
                self._start_new_triple(verb=self.triple.verb, noun2=self.triple.noun2)
                self.triple.set_noun1(token)
            else:
                self._start_new_triple(noun1=self.triple.noun1, verb=self.triple.verb)
                self.triple.set_noun2(token)
            return True

        return False

    @proceed
    def cop(self, token_head, token, *args, **kwargs):
        if token.pos_ == "VERB":
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
                self.triple.set_noun2(token_head)
            return True

    @proceed
    def advmod(self, token_head, token, *args, **kwargs):
        #self.triple.verb.append(token)
        return False

    @proceed
    def case(self, token_head, token, *args, **kwargs):
        self.triple.verb.set_case(token)

    @proceed
    def xcomp(self, token_head, token, *args, **kwargs):
        # text = "Langdurige zorg blijkt zeer goed te werken"
        # Here blijkt is a verb with Verbform=Inf, thus it functions as a Noun, and we have set it as a Noun with the
        # exceptions. In this case we thus need to refer to the tag, and in particular the first item when splitting on
        # the |. This indicates V, for verb.
        if token_head.pos_ == "VERB" and token.pos_ == "VERB":
            self.triple.verb.append(token)
            return True

    @proceed
    def aux(self, token_head, token, *args, **kwargs):
        if token_head.pos_ is not "VERB":
            # the aux may also function as a verb completer, if so the verb previously added should already have been
            # completed with the aux
            self.triple.verb.prepend(token)

    @proceed
    def parataxis(self, token_head, token, *args, **kwargs):
        if token_head.pos_ == "VERB":
            # text = "Brazilië is met zijn 8,5 miljoen vierkante kilometer het grootste land van Zuid-Amerika, het
            # beslaat bijna de helft van dit continent."
            # parataxis(land, beslaat)
            # -> land fuctions as a verb.
            # 1. Brazilie is grootste land (we have cop(land, is))
            # 2. Brazilie beslaat .., thus remain noun1 and set new verb
            self._start_new_triple(noun1=self.triple.noun1)
            self.triple.set_verb(token)
            return True

    def __str__(self):
        striples = []
        for triple in self.triples:
            striple = triple.__str__()
            if striple != "":
                striples.append(striple)

        return "\n".join(striples)
