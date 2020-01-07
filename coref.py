import sys
import os
from dutchcoref.coref import readngdata, process


def coref(path):
    ngdata, gadata = readngdata()
    mentions, clusters = process(path, sys.stdout, ngdata, gadata, docname=os.path.basename(path.rstrip('/')))
    return mentions, clusters