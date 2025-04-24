from nltk.corpus import BracketParseCorpusReader
from nltk import Tree
from nltk.tree import ParentedTree
from collections import Counter
import re

### helper functions ###
def find_rem_traces(parented_tree):
    """
    Find positions of '-NONE-A-PASS-' nodes or -NONE-A-RAISE- in the tree.
    Also find ABAR-OTHER traces for fronted embedded clauses.
    """
    matches = []
    for subtree in parented_tree:
        if isinstance(subtree, Tree):
            if (subtree.label() in ["-NONE-A-PASS-","-NONE-A-RAISE-"] or 
                (subtree.label() == "-NONE-ABAR-OTHER-" and 
                 subtree.parent().label() == "SBAR")):
                matches.append(subtree.parent().treeposition())
            matches.extend(find_rem_traces(subtree))
    return matches


def del_nodes_treepos(tree, list_pos):
    if not list_pos:
        return
    else: 
        for pos in reversed(list_pos): # reversed to prevent index shifting
            del tree[pos]

def strip_tree(tree):
    """
    Recursively traverse and removes numbering and trace type from nodes.
    """
    for i, subtree in enumerate(tree):
        if isinstance(subtree, Tree):
            # Process the node label
            node = subtree.label()
            if node.startswith('-NONE-'):
                new_label = "-NONE-"
                subtree.set_label(new_label)
            elif "-" in node:
                new_label = node.split('-')[0]
                subtree.set_label(new_label)
            # Recur for the subtree
            strip_tree(subtree)
        elif isinstance(subtree, str) and '-' in subtree:
            # Process the leaf
            tree[i] = subtree.split('-')[0]  # Modify the leaf in the parent tree

def remove_names(parented_tree):
    pos_leaves = parented_tree.treepositions('leaves')
    for pos in pos_leaves:
        if parented_tree[pos[:-1]].label() == 'NNP': # check if the leaf is a proper noun
            parented_tree[pos[:-1]][0] = 'Name'
        if parented_tree[pos[:-1]].label() == 'NNPS': # check if the leaf is a proper noun
            parented_tree[pos[:-1]][0] = 'Names'

class MyTree(ParentedTree):
    def has_proper_noun(self):
        return 'NNP' in str(self) or 'NNPS' in str(self)

### loading in trees from the corpus ###
corpus_root = "../FG_project/CHILDESTreebank-curr/"
corpus_file = "brown_adam.parsed"

corpus = BracketParseCorpusReader(corpus_root, corpus_file)
parsed_sents = corpus.parsed_sents() 

p_tree_list = [MyTree.convert(tree) for tree in parsed_sents 
               if "sinking" not in str(tree)] # added this because there was one tree that the FG could not parse 

### processing trees ###
# looping through all the trees and performing 3 actions:
#   removing unwanted traces
#   removing numbering and trace type from the nodes 
#   replacing proper nouns with special "Name" or "Names" token
target_strings = ["-NONE-A-PASS-", "-NONE-A-RAISE-", "-NONE-ABAR-OTHER-"]
for p_tree in p_tree_list:
    if any(substring in str(p_tree) for substring in target_strings):
        rem_trace_pos = find_rem_traces(p_tree)
        del_nodes_treepos(p_tree, rem_trace_pos)
    strip_tree(p_tree)
    if p_tree.has_proper_noun():
        remove_names(p_tree)


### pulling out unique nodes as a check ###
unique_nodes = []
for tree in p_tree_list:
    for subtree in tree.subtrees():
        node = subtree.label()
        if node not in unique_nodes:
            unique_nodes.append(node)



### converting trees to strings ###
tree_strs = []
for tree in p_tree_list:
    tree_str = str(tree)
    cleaned = re.sub(r'\n\s*', ' ', tree_str)
    tree_strs.append(cleaned)


### writing to form and counts files ###
tree_counts = Counter(tree_strs)

unique_trees = list(tree_counts.keys())
counts = list(tree_counts.values())

with open("forms.txt", 'w') as file:
    for tree in unique_trees:
        file.write("(" + tree + ")\n")

with open("counts.txt", 'w') as file:
    for num in counts:
        file.write(str(num) + "\n")
















## Did some checks and made some edits to the local file for the corpus whenever there was an error loading in a tree
## dealing with "Bad tree detected" and getting strings for the trees
# heights = [tree.height() for tree in parsed_sents]
# min_tree_indices = [i for i,num in enumerate(heights) if num == 2]

# tree_strs = [str(tree) for tree in parsed_sents if tree.height()>2]
# height of 2 are the bad trees that were flattened 
# I'm ignoring these now but should figure out why they are not being parsed


## I think it's all the times where the final punctuation isn't indented 
# Fixed these but still running into some issues
# Just some typos where trees weren't indented 


## now I want to strip all the unnecessary information ##
# lowercase 's' is just a typo?
# fix "AUX're" typo in the trees
# 'feather' shouldn't be a node
# 'WHNP=1' should be "-1"
## all fixed 




#### old code editing nodes with a dictionary look-up
# # Dictionary specifying edits
# edits = {'NONE-ABAR-WH-': '-NONE-ABAR-WH-', 'NONE-A-RAISE-':'-NONE-A-RAISE-', 
#          'NONE-ABAR-RC-': '-NONE-ABAR-RC-', 'NONE-A-PASS-': '-NONE-A-PASS-'}


# def modify_tree(tree, edits):
#     """
#     Recursively traverse and modify the tree based on the edits dictionary.
#     """
#     for i, subtree in enumerate(tree):
#         print(i, subtree)
#         if isinstance(subtree, Tree):
#             node = subtree.label()
#             # If the label of the subtree matches a key in edits, modify it
#             if node in edits: # start with the typos
#                 subtree.set_label(edits[node])
#             elif "-" in subtree.label():
#                 new_label = "" # use regular expressions to strip off info after dash
#                 subtree.set_label(new_label)
#             # Recur for the subtree
#             modify_tree(subtree, edits)

#     return str(tree)
# # this should also work with looping through subtrees as opposed to this recursive setup

# # Modify the tree
# modify_tree(parsed_sents[0], edits)