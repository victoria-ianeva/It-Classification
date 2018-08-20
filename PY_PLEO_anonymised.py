'''
Feature extractor for a 6-way classification of it

Program assumes that it is presented with single sentences separated by blank
 lines. As a result, paragraph boundary information is lost and cannot be
 exploited.

Author learning Python
'''

import nltk as nltk
# nltk.download()

from nltk.tree import ParentedTree

from nltk.stem import WordNetLemmatizer


import os
from nltk.parse import stanford
from nltk.parse.stanford import StanfordDependencyParser
# from nltk.parse.dependencygraph import DependencyGraph

from nltk.tree import ParentedTree


import sys
from sys import argv


import re
import numbers
import math

import subprocess

import string

# from nltk.parse.stanford import StanfordDependencyParser


def count_tag(query, string):
    count = len(re.findall(query, string))
    return(count)

def get_prev_word(tag_starter, string):
    search_word = ')(*&^%$><~'
    if tag_starter in ['ANY']:
        search_word = '\(([^\(\)\s ]+) ([^\s\(\)]+)\)'
    else:
        search_word = '\(' + tag_starter + '([^\(\)\s ]+) ([^\)]+)\)'

    word = 'NA'
    matches = re.findall(search_word, string)
    for m in matches:
        word = m[1]
        word = re.sub('\(([A-Z]+) ','', word)
        word = re.sub('\\\\','', word)
#        print('[',word,']')
# Last word in list "matches"

    word = wordnet_lemmatizer.lemmatize(word)
    return word

def get_next_word(tag_starter, string):
    search_word = ')(*&^%$><~'
    if tag_starter in ['ANY']:
        search_word = '\(([^\(\)\s ]+) ([^\s\(\)]+)\)'
    else:
        search_word = '\(' + tag_starter + '([A-Z]+) ([^\(\)]+)\)'
        
    word = 'NA'
 
    matches = re.findall(search_word, string, re.MULTILINE)

    if len(matches) > 0:
#        print(matches)
        word = matches[0][1]
        word = wordnet_lemmatizer.lemmatize(word)
        return word
    else:
        return word

def get_prev_POS(word_position, sent):
    pos = 'NA'

    preceding_tags = []
    
    words = re.findall('\(([A-Z]+) ([^\(\)]+)\)', sent)
    for w in words:
        this_pos = w[0]
        preceding_tags.append(this_pos)

    word_position = -word_position
    try:
        pos = preceding_tags[word_position]
    except:
        pos = 'NA'
    return pos


def get_next_POS(word_position, sent):
    pos = 'NA'

    following_tags = []
    word_position = word_position - 1
    
    words = re.findall('\(([A-Z]+) ([^\(\)]+)\)', sent)
    for w in words:
        this_pos = w[0]
        following_tags.append(this_pos)

    try:
        pos = following_tags[word_position]
    except:
        pos = 'NA'
    return pos

def get_following_complementisers(sent):
    num_following_complementisers = 0

    matches = re.findall(' (that|which|who)', sent,re.IGNORECASE)
    num_following_complementisers = len(matches)
#    print(matches)
    return(num_following_complementisers)


def words_until_next_complementiser(sent):
    words_until_next_comp = -1
    num_words = 0
    
    matches = re.findall('\(([^\s\(\)]+) ([^\(\)]+)\)', sent)
    for m in matches:        
        word = m[1]

#        print('---------', m[1], '-------')
        if(re.match('^(which|who|that)$', word, re.IGNORECASE)):
            words_until_next_comp = num_words
            return(words_until_next_comp)
        
        num_words = num_words + 1
        
    return words_until_next_comp


def words_until_next_infinitive(sent):
    words_until_next_inf = -1
    num_words = 0
    
    matches = re.findall('\(([^\s\(\)]+) ([^\(\)]+)\)', sent)
    for m in matches:        
        word = m[0]

#        print('=========', m[0], '=======')
        if(re.match('^TO$', word)):
            words_until_next_inf = num_words
            return(words_until_next_inf)
        
        num_words = num_words + 1
        
    return words_until_next_inf

def words_until_next_POS(pos, sent):
    words_until_next_pos = -1
    num_words = 0

    pos = '^' + pos + '$'
    
    matches = re.findall('\(([^\s\(\)]+) ([^\(\)]+)\)', sent)
    for m in matches:        
        word = m[0]

#        print('=========', m[0], '=======')
        if(re.match(pos, word)):
            words_until_next_pos = num_words
            return(words_until_next_pos)
        
        num_words = num_words + 1
        
    return words_until_next_pos


def adj_follows_before_np(tag1, tag2, sent):
    check = 'no'
#    print('Checking', tag1, tag2, 'in', sent)

    tag1 = '\(' + tag1
    tag2 = '\(' + tag2

    found_jj = False
    
    following_POSs = []
    following_words = re.findall('\(([^\(\s]+)', sent)
    for w in following_words:
#        print(w)

        match1 = re.match('^J', w)
        match2 = re.match('^NP', w)
        if(match1 is not None):
            found_jj = True

        if(match2 is not None):
            if found_jj is True:
                check = 'yes'
            
    return(check)


def comp_follows_before_next_NP(sent):
    check = 'no'

    found_comp = False

    match = re.findall('(.*)\(NP', sent)

    try:
        preceding_text = match[0]
    except:
        preceding_text = ''

#    print('************', preceding_text)
    if(re.search(' (that|which|who)\)', preceding_text) is not None):
        check = 'yes'
#        print(check)
#        exit()
            
    return(check)


def immediately_preceding_preposition(sent):
    check = 'no'

    words = re.findall('\(([^\(\s]+) ([^\)]+)\)', sent)


    if(len(words) > 0):
        preceding_word = words[-1]
        pos = preceding_word[0]
        if preceding_word == 'IN':
            check = 'yes'
            return check
    
    return check


def get_preceding_NPs(sent):
    num_preceding_nps = 0

    matches = re.findall('\(NP', sent)
    num_preceding_nps = len(matches)
    return(num_preceding_nps)


program_name, textFile = sys.argv
with open(textFile, 'r',encoding="latin-1") as myfile: # maybe try encoding="latin-1"
    text=myfile.read()

text = re.split('\n\n', text)


os.environ['STANFORD_PARSER'] = '/home/USER/stanford-parser-full-2017-06-09/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '/home/USER/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'

parser = stanford.StanfordParser(model_path="/home/USER/stanford-parser-full-2017-06-09/englishPCFG.ser.gz")

wordnet_lemmatizer = WordNetLemmatizer()




para_num = 0
pron_number = 0
for line in text:
    if re.search('(\.|\!|\?)(\s|\'|\"|\`)*$', line):
#        print(line,' ####LooksLikeATextParagraph####')
#        print('Parsing text')

        paragraph = re.split('(\.|\?|\!)\s+',line)
#        print('########>',paragraph)

# Condition set because this parser runs out of memory.
        new_paragraph = []
        for sent in paragraph:
#            print('SENT', sent, str(len(sent)))
            if len(sent) < 200:
                new_paragraph.append(sent)
            else:
                new_paragraph.append('The original version of this sentence was too long.')
        paragraph = new_paragraph

        first_parsed_paragraph = parser.raw_parse_sents(paragraph)

        parsed_paragraph = ParentedTree.convert(first_parsed_paragraph)

        paragraph_pronouns = []
        paragraph_nps = [] # All NPs
        paragraph_candidates = [] # Suitable candidates
        para_num = para_num + 1


#        print('START OF PARAGRAPH')

        parsed_paragraph_string = ''





        
        for line in parsed_paragraph:
            for parse in line:
#                print(parse)
                for sentence in parse:
#                    print('SENTENCESENTENCESENTENCESENTENCESENTENCESENTENCESENTENCESENTENCE')
#                    print(sentence)

                    for word in sentence:
                        parsed_paragraph_string = parsed_paragraph_string + str(word)

#        print('PARAGRAPHPARAGRAPHPARAGRAPHPARAGRAPHPARAGRAPHPARAGRAPHPARAGRAPHPARAGRAPH')
#        print(parsed_paragraph_string)


                        
        para_sent_number = 0
        para_num_nps = 0
        sent_word_number = 0

        para_lines = parsed_paragraph_string.split('\n')

        para_np_positions = []

        words_so_far = 0
        for phrase in para_lines:
#            print(phrase)

            if(re.search('\(NP',phrase,)):
                np_start_pos = words_so_far + 1

                matches = len(re.findall('\(([^ ]+) ([^\)\s]+)\)',phrase))
                np_end_pos = np_start_pos + matches - 1
                para_np_position_entry = str(para_num) + ' ' + str(para_sent_number) + ' ' + str(np_start_pos) + ' ' + str(np_end_pos)                
                para_np_positions.append(para_np_position_entry)
#                print(para_np_position_entry)


            else:
               matches = len(re.findall('\(([^ ]+) ([^\)\s]+)\)',phrase))
               words_so_far += matches

        



        matches = re.findall('\(PRP it\)', parsed_paragraph_string, re.IGNORECASE)
        for m in matches:
            built_m = r'(.*)' + m + '(.*)'


            
            regex = re.search(built_m, parsed_paragraph_string, re.S)


            
            try:
                num_preceding_nps = len(re.findall('\(NP', regex.group(1))) - 1
                
                preceding_paragraph = regex.group(1)
                this_it = regex.group(2)
                following_paragraph = regex.group(3)



                
                word_position = 0
                sent_preceding_nps = 0
                para_preceding_nps = 0
                para_preceding_nps = 0
                sent_following_adjs = 0
                sent_following_nps = 0
                sent_nps = 0
                para_nps = 0







                
                replacement_it = re.sub(' it$', ' _IT_', this_it)

                it = re.search(' (it)', this_it, re.IGNORECASE).group(1)

                parsed_paragraph_string = re.sub(m, replacement_it, parsed_paragraph_string)



                
#                print(parsed_paragraph_string)
                sent_num1 = count_tag('(\. \.)', preceding_paragraph)
                sent_num2 = count_tag('(\. ?)', preceding_paragraph)
                sent_num3 = count_tag('(\. !)', preceding_paragraph)
                sent_num = sent_num1 + sent_num2 + sent_num3 + 1


                
                preceding_sentence = preceding_paragraph
                temp_preceding_sentence = preceding_sentence
                preceding_sentence = re.sub("\'", "-APOS-", temp_preceding_sentence)



#                print('PrecedingParagraph:' + preceding_paragraph)
                sentence_matches = re.findall(' (\.|\!|\?)\)(.*)',preceding_paragraph)


#                print('2>>>>>>' + it + '\n')
#                print(':::>',sentence_matches)

                for sm in sentence_matches:
  #                  print('sm --->', sm.group(2))
                    preceding_sentence = sm.group(2)
 #                   print('!!!!!>',preceding_sentence)



#                print('3>>>>>>' + preceding_sentence + '\n')
                
                if re.search(' [\.?!]\)', preceding_paragraph,):
                    ps_matches = re.findall('(.*)\(([^\s]+) ([\.?!])\)(.*)', preceding_paragraph,re.S)
                    for psm in ps_matches:
                        preceding_sentence = psm[3]
                    
                    word_position = len(re.findall('\(([^\s]+) ([^)]+)\)',preceding_sentence,re.S)) + 1
                    sent_preceding_nps = len(re.findall('\(NP',preceding_sentence,re.S)) - 1
                    para_preceding_nps = len(re.findall('\(NP',preceding_paragraph,re.S)) - 1



                    
#                print('Looking for fullstop in following paragraph\n======================Following paragraph============', following_paragraph, '===================================\n')
                next_sent_match = re.match('(.*) ([\.?!])\)', following_paragraph, re.S)
                following_sent = next_sent_match.group(1)
                temp_following_sent = following_sent
                following_sent = re.sub("\'", "-APOS-", temp_following_sent)

#                print('following sent is ', following_sent)
                
                sent_following_adjs = len((re.findall('\(JJ',following_sent,re.S)))
                sent_following_nps = len(re.findall('\(NP',following_sent,re.S))
#                print(sent_following_adjs, 'following adjs')
#                print(sent_following_nps, 'following nps in ', following_sent)


                para_following_nps = len(re.findall('\(NP',following_paragraph,re.S))
                
                prev_verb = 'NA'

                temp_preceding_sentence = re.sub("\'", "\-APOS\-", preceding_sentence)


                
                prev_verb = get_prev_word('V', temp_preceding_sentence)
                if prev_verb in ['-APOS-s', '-APOS-re']:
                    prev_verb = 'be'

                    
                next_adj = get_next_word('J', following_sent)
                next_verb = get_next_word('V', following_sent)
                if next_verb in ['-APOS-s', '-APOS-re']:
                    next_verb = 'be'

                prev_word = get_prev_word('ANY', temp_preceding_sentence)
                next_word = get_next_word('ANY', following_sent)


                get_preceding_nps = get_preceding_NPs(temp_preceding_sentence)


                
                pos_l4 = get_prev_POS(4, temp_preceding_sentence)
                pos_l3 = get_prev_POS(3, temp_preceding_sentence)
                pos_l2 = get_prev_POS(2, temp_preceding_sentence)
                pos_l1 = get_prev_POS(1, temp_preceding_sentence)

                
                pos_r1 = get_next_POS(1, following_sent)
                pos_r2 = get_next_POS(2, following_sent)
                pos_r3 = get_next_POS(3, following_sent)
                pos_r4 = get_next_POS(4, following_sent)


                
                num_following_complementisers = get_following_complementisers(following_sent)
                adj_follows_before_next_NP = adj_follows_before_np('J', 'NP', following_sent)
                
                words_until_next_comp = words_until_next_complementiser(following_sent)
                words_until_next_inf = words_until_next_POS('TO', following_sent)
                words_until_next_prep = words_until_next_POS('IN', following_sent)
                words_until_next_ing = words_until_next_POS('VBG', following_sent)
                comp_follows_before_np = comp_follows_before_next_NP(following_sent)
                preceding_preposition = immediately_preceding_preposition(temp_preceding_sentence)


                
                sent_nps = sent_preceding_nps + sent_following_nps
                para_nps = para_preceding_nps + para_following_nps
#                print('Here')


                
                print(it, para_num, 'SN', str(sent_num), 'SPF', word_position, 'SPT', word_position, sent_preceding_nps, para_preceding_nps, sent_following_nps, sent_nps, para_nps, sent_following_adjs, prev_verb, next_adj, next_verb, pos_l4, pos_l3, pos_l2, pos_l1, pos_r1, pos_r2, pos_r3, pos_r4, num_following_complementisers, adj_follows_before_next_NP, words_until_next_comp, words_until_next_inf, words_until_next_prep, words_until_next_ing, comp_follows_before_np, preceding_preposition, prev_word, next_word)


                

            except:
                num_preceding_nps = 0
#                print('FAILED TO GET FEATURES:' + m + '\n---->')
                print('FAILED TO GET FEATURES:' + m + '---->')
 #               for l in line:
 #                   print(l)
