from Commons import *

#Global hash
hash2 = {}

def Hashprocess(synset):
    '''
    To Process each Hashentry one by one
    '''
    #Initialize wordnet object for property access
    wn_synset = wn.synset(synset.name())
    pos = synset.pos()
    if pos == 'n':
        Nounhash(wn_synset, synset)
    elif pos == 'v':
        Verbhash(wn_synset, synset)
    elif pos == 'a':
        Adjhash(wn_synset, synset)
    elif pos == 'r':
        Advhash(wn_synset, synset)
    else:
        print 'Wrong POS tag - ',pos

def Synsets(data):
    '''
    Returns custom synset objects from hash
    '''
    global hash2
    custom_synsets = list()
    for wn_synset in data:
        name = Unicode(wn_synset.name())

        #Filling only properties which exist in hash
        if name in hash2:
            custom_synsets.append(name)

    return custom_synsets

def Error(error):
    '''
    To handle midway processing stop
    '''
    print 'Error - ',error
    Shelveclose(hash2)

def Nounhash(wn_synset, synset):
    '''
    Fixed property template for Noun_Synsets
    '''
    #Filling Hypernyms
    custom_synsets = Synsets(wn_synset.hypernyms())
    synset.populate('hypernyms', custom_synsets)

    #Filling Hyponyms
    custom_synsets = Synsets(wn_synset.hyponyms())
    synset.populate('hyponyms', custom_synsets)

def Verbhash(wn_synset, synset):
    '''
    Fixed property template for Verb_Synsets
    '''
    pass

def Adjhash(wn_synset, synset):
    '''
    Fixed property template for Adjective_Synsets
    '''
    pass

def Advhash(wn_synset, synset):
    '''
    Fixed property template for Adverb_Synsets
    '''
    pass

if __name__ == '__main__':
    hash2 = Shelveopen('Hash#2.shelve')
    try:
        for synset in hash2.values():
            Hashprocess(synset)

            #Replace in Hash
            hash2[synset.name()] = synset
        raise StopIteration('Stop Iteration')
    except StopIteration as s:
        Error(s)
    except KeyboardInterrupt as k:
        Error(k)
        sys.exit(0)
    except Exception as e:
        Error(e)