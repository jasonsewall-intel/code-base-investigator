# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

from .tree_walker import TreeWalker
from codebasin.preprocessor import CodeNode, DirectiveNode, FileNode, Lexer, MacroExpander

class SourcePrinter(TreeWalker):
    """
    TreeWalker that prints preprocessed source.
    """
    def __init__(self, _tree):
        super().__init__(_tree, None)

    def walk(self):
        """
        Walk the tree, printing each node.
        """
        self.__print_nodes(self.tree.root)

    def __print_nodes(self, node):
        """
        Print this specific node, then descend into its children nodes.
        """
        if not isinstance(node, FileNode):
            print(node.spelling())

        for child in node.children:
            self.__print_nodes(child)

class PreprocessedSourcePrinter(TreeWalker):
    """
    TreeWalker that prints preprocessed source code.
    """
    def __init__(self, _tree, _node_associations, _platform):
        super().__init__(_tree, _node_associations)
        self.platform = _platform
        self.expand_macros = True

    def walk(self):
        """
        Walk the tree, printing the result of each node after preprocessing.
        """
        self.__print_nodes(self.tree.root, self._node_associations)

    def __print_nodes(self, _node, _map):
        """
        Print this specific node, then descend into its children nodes.
        """
        if isinstance(_node, CodeNode):
            association = _map[_node]
            if association and not isinstance(_node, DirectiveNode):
                line = _node.spelling()
                if self.expand_macros:
                    tokens = Lexer(line).tokenize()
                    expansion = MacroExpander(tokens).expand(self.platform)
                    # TODO: revisit this after Jason's token-list fixes
                    line = "".join([str(token) for token in expansion])
                print(line)
            else:
                # Replace unused code with whitespace
                print()

        for child in _node.children:
            self.__print_nodes(child, _map)
