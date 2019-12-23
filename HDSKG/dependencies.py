
# scenarios

# 1.
# nsubj(n1,v) & dobj(v, n2)

# 2.
# nsubj(n1,v) & nmod(v, n2) (include case(a. n2) to extend the verb with _a ?)
# similar:
# text = "HSQLDB wordt ondersteund door menig Java frameworks":
# nsubj(n1, v) & advmod(v, n2) (include case(a. n2) to extend the verb with _a)

# 3.
#

# 4.
#

# 5.
#

# 6.
#

# a.
# text = "webkit is ontwikkeld door Intel"
# nsubj(n1,v) & obl(v, n2) (& case(a, n2))
# then create triple: (n1, v_a, n2)
# i.e. n1 = webkit, v = is_ontwikkeld, n2= Intel, a = door

# b.
# text = "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
# nsubj(n1, v) & obj(v, n2) (& case(a, n2))

# c.
# text = "webkit is ontwikkeld door Intel, aan de Intel Open Source Technology Center."
# apply the flat dependency to find multiword expressions
# i.e. flat(Intel, Open), flat(Intel, Source), etc.

# d.
# text = "Pieter houd van appels en bananen."
# nsubj(n1, v) & (nmod(v, n2) & case(a, n2)) & conj(n2, n3)
# with n1 = Pieter, v = houd, n2 = appels, n3 = bananen, a = van.
# then (n1, a_v, n2) and (n1, v_a, n3)

# e.
# text = "In de toekomst gaan we naar de maan en Mars."
# nsubj(n1, v) & (obl(v, n2) & case(a, n2)) & conj(n2, n3)
# with n1 = we, v = gaan, n2 = maan, n3 = Mars, a = naar.
# then (n1, a_v, n2) and (n1, v_a, n3)

# e.
# text = "In de toekomst gaan we naar de maan, Mars en de zon."
# nsubj(n1, v) & (obl/conj(v, n2) & case(a, n2)) & obl/conj(n2, n3) & conj(n2, n4)
# with n1 = we, v = gaan, n2 = maan, n3 = Mars, n4 = zon.
# then (n1, a_v, n2) and (n1, v_a, n3) and (n1, a_v, n4)

# f.
# text = "PyTables is gebouwd op HDF5, met behulp van Python en het Numpy pakket."
# nsubj(n1, v) & (advmod(v, x) & obj/obl(x, n2))
# with n1 = PyTables, v = gebouwd, x = (non-noun) met, n2 = Python
# then (n1, v_x, n2)
