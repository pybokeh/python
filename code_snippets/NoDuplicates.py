ls = ['part1','part1','part2','part3','part3','part4']

def nodupes_orig_order(seq):
    """ Removes duplicates while preserving order
        Otherwise, you can just do this: mylist = set(mylist)
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

print nodupes_orig_order(ls)
