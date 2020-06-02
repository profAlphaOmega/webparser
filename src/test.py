

def dedup(l=list()):
    ''' Needs list of dicts
        Hashes their values
        finds all indicies of occurences of hashes and builds a list
        removes the indicies from original list
        returns deduped list
    '''
    if not l:
        return l 

    hash_list = [hash(tuple(v for k,v in x.items())) for x in l]

    # build list first, don't delete anything in this iteration to avoid conflict of list lengths
    remove_list = list()
    for hsh in hash_list:
        rm = [i for i,v in enumerate(hash_list) if hsh == v]
        rm.pop(0)
        remove_list = remove_list + rm
    remove_list = list(set(remove_list))
    # remove from original list
    for index in sorted(remove_list, reverse=True):
        del l[index]
    
    return l
