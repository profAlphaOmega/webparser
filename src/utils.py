import re

url_extensions = [
    '.com',
    '.co',
    '.org',
    '.net',
    '.io',
    '.org',
    'cdn',
    '.gov',
    '.edu',
    '.int',
    '.jp',
]

def relative_path_check(url=''):
    ''' IF extension(from list) found in path -> RETURN False, If NOT RETURN True
    '''
    return not any(ext in url for ext in url_extensions)

def string_striper(string=''):
    ''' Trims the ends first. Anything left is in between words, so add a space
    '''
    return re.sub('\n',' ',string.strip())


def add_header_args(options, headers):
    for header, v in headers.items():
        options.add_argument(f"{header}={v}")
    return options

def dedup(l=list()):
        ''' 
        Deduplicates a list of dicts, while preserving order
        Accpepts list of dicts
            Hashes their values
            Finds all indicies of occurences of hashes and builds a list
            Removes the indicies from original list
        returns deduped list

        '''
        if not l:
            return l 

        # Hash All contents by its keys and their values
        hash_list = [hash(tuple(v for k, v in x.items())) for x in l]

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