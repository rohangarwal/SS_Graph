from compute_graph import get_words
from compute_graph import remove_overlap_words
from random import randint
import shelve
from nltk.corpus import wordnet as wn
from Commons import Unicode
import collections

def get_words_test():
    definition = 'This is usually in the United States where we find it.'
    tokens_2 = get_words(definition, 2)
    print tokens_2
    print '******'
    tokens_1 = get_words(definition, 1)
    print tokens_1
    print '******'
    tokens_1 = remove_overlap_words(tokens_1, tokens_2)
    print tokens_1

def find_substring(string1, string2):
    if '_' in string1:
        str_list = string1.split('_')
        new_string = ' '.join(str_list)
        return new_string.lower() in string2.lower()
    else:
        return string1.lower() in string2.lower()

def word_data_d2s_test(wd_filename):
    word_data_hotfix = shelve.open(wd_filename)
    keys = word_data_hotfix.keys()
    max_rng = len(keys)
    for trials in range(0,100):
        index = randint(0,max_rng-1)
        #assert word_data_hotfix[keys[index]]['D2S'] ==
        print keys[index]
        synsets_dict = word_data_hotfix[keys[index]]['D2S']
        print synsets_dict
        for k in synsets_dict:
            assert find_substring(keys[index], wn.synset(k).definition())
        print '********PASS********'

def sense_processing_test(sd_filename):
    sense_data = shelve.open(sd_filename)
    #print len(sense_data.keys())
    keys = sense_data.keys()
    max_rng = len(keys)
    #print keys[:5]
    print sense_data['christian_holy_day.n.01']['S2W']
    '''
    for trials in range(0,10):
        index = randint(0,max_rng-1)
        #keys[index] -> string value - sense
        keys[index] = synset_name
        assert collections.Counter(sense_data[synset_name]['S2W']) == collections.Counter(wn.synset(synset_name).lemma_names())
    '''

if __name__ == "__main__":

    #get_words_test()
    #print 'united' in 'united_states'
    #word_data_d2s_test('Hash#3_hotfix.shelve')
    sense_processing_test('Shelves/Hash#4.shelve')