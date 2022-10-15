import pandas as pd
import numpy as np
import spacy as sp
from spacy import displacy
from nltk import Tree
from node import Node

nlp = sp.load("ru_core_news_sm")
parser_lst = nlp.pipe_labels['parser']
parse_black_list = ['VB', 'C', ',', '.', '!', '?']

def text_to_dep(text):
    root = nlp(text)

    for token in root:
        if token.tag_ in ['NOUN', 'VERB']:
            token.tag_ = token.tag_[0] + token.tag_[-1]
        elif token.tag_ in ['ADJ', 'ADV']:
            token.tag_ = 'JJ'

    return root

def find_deps(root, deps, max_iter=1000, interrupt=[], interrupt_dep=[]):
    found = []

    if max_iter == 0:
        return found

    for token in root.children:
        if str(token.tag_) in interrupt:
            continue
        if str(token.dep_) in interrupt_dep or str(token.dep_) == 'conj':
            continue
        if str(token.dep_) in deps:
            found.append(token)
        elif deps[0] == '*':
            found.append(token)
        found = find_deps(token, deps, max_iter-1, interrupt, interrupt_dep) + found

    return found

def find_features(root, indent=''):
    nodes = []

    for token in root:
        if 'VB' in str(token.tag_):
            subj = " ".join([str(s.text) for s in find_deps(token, ['nsubj', 'nmod'], 2, ['VB'], ['obj', 'amod', 'punct'])])
            obj = " ".join([str(o.text) for o in find_deps(token, ['obj'], 2, ['VB'], ['subj', 'nmod', 'punct' ])])
            obj_details = " ".join([str(o.text) for o in find_deps(token, ['*'], 2, ['VB'], ['obj', 'nsubj', 'amod', 'nmod', 'punct'])])
            
            node = Node(subj, 'abstract', find_features(token.children, indent+'\t'))
            node.children.append(Node(str(token.text), obj + ' ' + obj_details))
            nodes.append(node)
    
    for token in root:
        if str(token.tag_) == 'NN' and str(token.dep_) == 'nsubj':
            node = Node(token.text, token.head.text)
            if node not in nodes:
                nodes.append(node)

    return nodes

def to_row(text):
    try:
        node = node = Node('Root', 'root', find_features(text_to_dep(text)))
        node.assign_parent()

        flattened_texts = node.str_flatten().split('\n')[:-1]
        
        ef = node.get_ef()
        structure = pd.DataFrame({
            'ef': [links.split(' — ')[0] + " ".join(links.split(' — ')[-1].split(': ')[::-1]) for links in flattened_texts],
            'entity': [e['e'] for e in ef],
            'sent_word': [e['f'] for e in ef]})
        return structure.to_json(orient='records').encode('utf-8').decode('unicode_escape') if structure.shape[0] > 0 else '{"ef": "Doesn\'t have an opinion"}'
    except Exception as e:
        print(e)
        return '{"ef": "Doesn\'t have an opinion"}'