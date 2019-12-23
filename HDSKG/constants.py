# VVP
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(TO*)+(VB)+
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*)+(VBG)+

# VP
# (MD)*(VB.*)+(CD)*(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)+(MD)*(VB.*)+

# NP
# (CD)*(DT)?(CD)*(JJ)*(CD)*(VBD|VBG)*(NN.*)*-
# (POS)*(CD)*(VBD|VBG)*(NN.*)*-
# (VBD|VBG)*(NN.*)*(POS)*(CD)*(NN.*)+

# definitions
# MD = modal
# VB. = different verb categories
# NN. = different noun categories (including proper noun)
# JJ = adjective
# RB = adverb
# DT = article
# IN = any preposition or subordinating conjunction
# CD = NUM

# setting the defintions
MD = "VERB"
CD = "NUM"
JJ = "ADJ"
RB = "ADV"
DT = "DET"
IN = "ADP"
TO = ""
POS = "PART"
NN = "NOUN"
VB = "VERB"
