from nltk.corpus import BracketParseCorpusReader
from nltk import Tree
from collections import Counter
import re


## pulling out trees from corpus
corpus_root = "../FG_project/CHILDESTreebank-curr/"
corpus_file = "brown_adam.parsed"

corpus = BracketParseCorpusReader(corpus_root, corpus_file)
parsed_sents = corpus.parsed_sents() 


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


# removing info from nodes: removing numbering and trace type 
def strip_tree(tree):
    """
    Recursively traverse and modify the tree.
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

    return tree

print(strip_tree(parsed_sents[0]))


stripped_trees = [strip_tree(tree) for tree in parsed_sents]



## pulling out unique nodes
unique_nodes = []
for tree in stripped_trees:
    for subtree in tree.subtrees():
        node = subtree.label()
        if node not in unique_nodes:
            unique_nodes.append(node)

## converting trees to strings 
tree_strs = []
for tree in stripped_trees:
    tree_str = str(tree)
    cleaned = re.sub(r'\n\s*', ' ', tree_str)
    tree_strs.append(cleaned)







### counter
tree_counts = Counter(tree_strs)

unique_trees = list(tree_counts.keys())
counts = list(tree_counts.values())

# with open("forms.txt", 'w') as file:
#     for tree in unique_trees:
#         file.write("(" + tree + ")\n")

# with open("counts.txt", 'w') as file:
#     for num in counts:
#         file.write(str(num) + "\n")










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