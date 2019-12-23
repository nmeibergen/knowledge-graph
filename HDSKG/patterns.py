from .constants import *

# Verbs (VVP)
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(TO*)+(VB)+
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*)+(VBG)+
verbs_open = [
    f"POS:{VB}:+ POS:{CD}:* POS:{JJ}:* POS:{RB}:* POS:{JJ}:* POS:{VB}:? POS:{DT}:? POS:{IN}:+",
    f"POS:{VB}:+ POS:{JJ}:* POS:{RB}:* POS:{JJ}:* POS:{VB}:? POS:{DT}:? POS:{IN}:+"
]

# Verbs (VP)
# (MD)*(VB.*)+(CD)*(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)?(DT)?(IN*|TO*)+
# (MD)*(VB.*)+(JJ)*(RB)*(JJ)*(VB.*)+(MD)*(VB.*)+

verbs_closed = [
    f"POS:{VB}:+ POS:{CD}:* POS:{JJ}:* POS:{RB}:* POS:{JJ}:* POS:{VB}:? POS:{DT}:? POS:{IN}:+",
    f"POS:{VB}:+ POS:{JJ}:* POS:{RB}:* POS:{JJ}:* POS:{VB}:? POS:{DT}:? POS:{IN}:+",
    f"POS:{VB}:+ POS:{JJ}:* POS:{RB}:* POS:{JJ}:* POS:{VB}:? POS:{IN}:+"
]

# Nouns
# (CD)*(DT)?(CD)*(JJ)*(CD)*(VBD|VBG)*(NN.*)*-
# (POS)*(CD)*(VBD|VBG)*(NN.*)*-
# (VBD|VBG)*(NN.*)*(POS)*(CD)*(NN.*)+

nouns = [
    f"POS:{CD}:* POS:{DT}:? POS:{CD}:* POS:{JJ}:* POS:{CD}:* POS:{NN}:* "
    f"POS:{POS}:* POS:{CD}:* POS:{NN}:* "
    f"POS:{NN}:* POS:{POS}:* POS:{CD}:* POS:{NN}:+",
    # f"POS:{DT}:* POS:{IN}:* POS:{NN}:+"
]
