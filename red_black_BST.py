"""
You can do it either with networkx ('cause tree is a graph)
or with dicts (smth like {'key': 0, value: 123, 'left': {...}, 'right':{...}})
"""

import random
import time
from typing import Any, Optional, Tuple

_root = {}


def insert(key: int, value: Any) -> None:
    """
    Insert (key, value) pair to binary search tree

    :param key: key from pair (key is used for positioning node in the tree)
    :param value: value associated with key
    :return: None
    """
    if not _root:
        _root['key'] = key
        _root['value'] = value
        _root['left'] = {}
        _root['right'] = {}
    else:
        found, node = _find(key)
        if found:
            node['value'] = value
        else:
            if key < node['key']:
                node['left'] = {'key': key, 'value': value, 'left': {}, 'right': {}}
            else:
                node['right'] = {'key': key, 'value': value, 'left': {}, 'right': {}}
    return None


def _find(key: int) -> Tuple[bool, dict]:
    """
    Find key in tree

    :param key: key to find
    :return: tuple of search success and found key
    """
    current_node = _root
    while current_node:
        if key == current_node['key']:
            return True, current_node
        elif key < current_node['key']:
            if not current_node['left']:
                return False, current_node
            else:
                current_node = current_node['left']
        else:
            if not current_node['right']:
                return False, current_node
            else:
                current_node = current_node['right']


def remove(key: int) -> Optional[Tuple[int, Any]]:
    """
    Remove key and associated value from the BST if exists

    :param key: key to be removed
    :return: deleted (key, value) pair or None
    """
    if not _root:
        return None
    else:
        found, the_node = _find(key)
        if not found:
            return None
        else:
            remove_if_found(the_node)


def copy_node(node1, node2: dict):
    """
    Copy all pairs of key: value from one node to another

    :param node1: target node
    :param node2: source node
    :return:
    """
    node1['key'] = node2['key']
    node1['value'] = node2['value']
    node1['left'] = node2['left']
    node1['right'] = node2['right']


def remove_if_found(node: dict):
    """
    Remove of found node from tree

    :param node: found mode
    :return: None
    """
    if not node['left'] and not node['right']:
        node.clear()
    elif not node['left']:
        next_node = node['right']
        copy_node(node, next_node)
    elif not node['right']:
        next_node = node['left']
        copy_node(node, next_node)
    else:
        current_node = node['right']
        if not current_node['left']:
            node['key'] = current_node['key']
            node['value'] = current_node['value']
            remove_if_found(current_node)
        else:
            min_in_branch = current_node['left']
            while min_in_branch['left']:
                min_in_branch = min_in_branch['left']
            node['key'] = min_in_branch['key']
            node['value'] = min_in_branch['value']
            remove_if_found(min_in_branch)


def find(key: int) -> Optional[Any]:
    """
    Find value by given key in the BST

    :param key: key for search in the BST
    :return: value associated with the corresponding key
    """
    found, node = _find(key)
    if not found:
        raise KeyError
    else:
        return node['value']


def clear() -> None:
    """
    Clear the tree

    :return: None
    """
    _root.clear()


def test_all_nodes():
    """
    Test all nodes in random order

    :return:
    """
    clear()
    insert(50, "Num1")
    insert(25, "Num2")
    insert(75, "Num3")
    insert(62, "Num4")
    insert(87, "Num5")
    insert(56, "Num6")
    insert(68, "Num7")
    insert(81, "Num8")
    insert(93, "Num9")
    insert(20, "Num10")
    insert(30, "Num11")
    print('Initial: ', _root)
    start = time.time()
    i, j = 0, 0
    # order = [i for i in random.randrange(0, 100, 1)]
    while len(_root) != 0:
        j += 1
        random.seed()
        item = random.randrange(0, 100, 1)
        found, node = _find(item)
        if found:
            i += 1
            remove(item)
            print(f'{i})', f'After deletinf of {item}: {_root}')
    print(time.time() - start, "Number of iterations: ", j)


def test_some_nodes():
    """
    Test some special cases

    :return:
    """
    clear()
    insert(75, "Num1")
    insert(68, "Num2")
    insert(93, "Num2")
    # insert(83, "Num2")
    print(_root)
    remove(75)
    print(_root)


if __name__ == '__main__':
    test_all_nodes()
    test_some_nodes()
