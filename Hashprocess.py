from Commons import *

#Global hash
hash2 = {}

def Hashprocess(synset):
    '''
    To Process each Hashentry one by one
    '''
    #Initialize wordnet object for property access
    wn_synset = wn.synset(synset.name())

    if synset.pos() == 'n':
        Nounhash(wn_synset, synset)
    elif synset.pos() == 'v':
        Verbhash(wn_synset, synset)
    elif synset.pos() == 'a':
        Adjhash(wn_synset, synset)
    elif synset.pos() == 'r':
        Advhash(wn_synset, synset)
    else:
        print 'Wrong POS tag !'

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
            print 'Match Found - ',name
            custom_synsets.append(hash2[name])

    return custom_synsets

def Error(error):
    '''
    To handle midway processing stop
    '''
    if error == 'Stop':
        print 'Processing done, closing Hash !'
    elif error == 'Key':
        print 'Key Interrupt, closing Hash !'
    else:
        print 'Some Other Exception !'

    Shelveclose(hash2)

def Nounhash(wn_synset, synset):
    '''
    Fixed property template for Noun_Synsets
    '''
    if wn_synset.hypernyms():
        #Filling Hypernyms
        custom_synsets = Synsets(wn_synset.hypernyms())
        synset.populate('hypernyms', custom_synsets)

    if wn_synset.hyponyms():
        #Filling Hyponyms
        custom_synsets = Synsets(wn_synset.hyponyms())
        synset.populate('hyponyms', custom_synsets)

    if wn_synset.meronyms():
        #Filling meronyms
        custom_synsets = Synsets(wn_synset.meronyms())
        synset.populate('meronyms', custom_synsets)

    if wn_synset.holonyms():
        #Filling holonyms
        custom_synsets = Synsets(wn_synset.holonyms())
        synset.populate('holonyms', custom_synsets)

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

def Hashaccess(data):
    '''
    Return hashed values for W_synsets
    '''
    return [hash2[x] for x in data]

if __name__ == '__main__':
    hash2 = Shelveopen('Hash#2.shelve')
    while True:
        try:
            for synset in hash2.values():
                Hashprocess(synset)
        except StopIteration:
            Error('Stop')
        except KeyboardInterrupt:
            Error('Key')
            sys.exit(0)
        except Exception:
            Error('Other')
