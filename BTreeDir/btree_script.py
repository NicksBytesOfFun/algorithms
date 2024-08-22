import math
import sys


def add(node, item, position=None):
    if node.items is None:
        node.items = [Element(item)]
        node.bare_items = [item]
    else:
        if position is None:
            insert_pos = word_binary_search(node.bare_items, 0, node.size - 1, item)
        else:
            insert_pos = position
        node.bare_items.insert(insert_pos, item)
        node.items.insert(insert_pos, Element(item))
    node.size += 1
    return node


def remove(node, item, position=None):
    if position is None:
        delete_pos = word_binary_search(node.bare_items, 0, node.size - 1, item)
    else:
        if position == node.size:
            position -= 1
        delete_pos = position
    node.items.pop(delete_pos)
    node.bare_items.pop(delete_pos)
    node.size -= 1

    return node


class Element:
    def __init__(self, value, left_link=None, right_link=None):
        self.left_link = left_link
        self.right_link = right_link
        self.value = value


class Node:
    def __init__(self, items=None, parent=None):
        self.items = items
        self.bare_items = None
        self.parent = parent
        self.is_root = False
        self.has_children = False
        if items is not None:
            self.size = len(items)
        else:
            self.size = 0


def get_inorder_pre(node):
    while node.items[-1].right_link is not None:
        node = node.items[-1].right_link

    element_value = node.items[-1].value
    return element_value


def get_inorder_post(node):
    while node.items[0].left_link is not None:
        node = node.items[0].left_link

    element_value = node.items[0].value
    return element_value


def merge_nodes(node1, node2):
    new_node = Node(node1.items + node2.items)
    new_node.bare_items = node1.bare_items + node2.bare_items
    new_node.has_children = node1.has_children or node2.has_children
    new_node.size = node1.size + node2.size
    new_node.parent = node1.parent

    # assign links to new item
    new_node.items[node1.size - 1].left_link = new_node.items[node1.size - 2].right_link
    new_node.items[node1.size - 1].right_link = new_node.items[node1.size].left_link

    return new_node


class BTree():
    def __init__(self, root, min_deg):
        self.root = root
        self.min_deg = min_deg

    def search(self, element):
        if not self.root.items:
            return False

        current_node = self.root

        while current_node.has_children:
            insert_pos = word_binary_search(current_node.bare_items, 0, current_node.size - 1, element)

            if insert_pos == current_node.size:
                current_node = current_node.items[-1].right_link

                if current_node.items[-1].value == element:
                    return True
            else:
                node_element = current_node.items[insert_pos]
                if node_element.value > element:
                    current_node = node_element.left_link
                elif node_element.value < element:
                    current_node = node_element.right_link
                else:
                    return True

        insert_pos = word_binary_search(current_node.bare_items, 0, current_node.size - 1, element)
        if insert_pos == current_node.size:
            return False

        if current_node.bare_items[insert_pos] == element:
            return True
        return False

    def case3(self, current_node, insert_pos, element):
        # get the value of the position in parent node where this node stems from
        if insert_pos >= current_node.parent.size:
            parent_val = current_node.parent.bare_items[-1]
        else:
            parent_val = current_node.parent.bare_items[insert_pos]

        # find out which child the node is of the parent
        if current_node.parent.size == insert_pos:
            neighbour = current_node.parent.items[-1].left_link
            neighbour_side = 0
        else:
            if current_node.parent.bare_items[insert_pos] > element:
                neighbour = current_node.parent.items[insert_pos].right_link
                neighbour_side = 1
            else:
                neighbour = current_node.parent.items[insert_pos].left_link
                neighbour_side = 0

        # case 3a
        if neighbour.size >= self.min_deg:
            if neighbour_side == 0:
                # perform rotation clockwise
                switch_child = neighbour.items[-1].right_link
                neighbour_val = neighbour.bare_items[-1]

                # remove nodes
                current_node.parent = remove(current_node.parent, parent_val, insert_pos)
                neighbour = remove(neighbour, neighbour_val, neighbour.size - 1)

                # add them back in
                current_node.parent = add(current_node.parent, neighbour_val, insert_pos)
                current_node = add(current_node, parent_val, 0)

                # adjust children
                if insert_pos == current_node.parent.size:
                    insert_pos -= 1
                current_node.parent.items[insert_pos].left_link = neighbour
                current_node.parent.items[insert_pos].right_link = current_node
                if switch_child is not None:
                    current_node.items[0].left_link = switch_child
                    current_node.items[0].right_link = current_node.items[1].left_link
                    switch_child.parent = current_node
                if insert_pos == current_node.parent.size:
                    insert_pos += 1

                return current_node


            else:
                switch_child = neighbour.items[0].left_link
                neighbour_val = neighbour.bare_items[0]

                # remove nodes
                current_node.parent = remove(current_node.parent, parent_val, insert_pos)
                neighbour = remove(neighbour, neighbour_val, 0)

                # add them back in
                current_node.parent = add(current_node.parent, neighbour_val, insert_pos)
                current_node = add(current_node, parent_val)

                # adjust children
                if insert_pos == current_node.parent.size:
                    insert_pos -= 1
                current_node.parent.items[insert_pos].right_link = neighbour
                current_node.parent.items[insert_pos].left_link = current_node
                if switch_child is not None:
                    current_node.items[-1].right_link = switch_child
                    current_node.items[-1].left_link = current_node.items[
                        -2].right_link
                    switch_child.parent = current_node
                if insert_pos == current_node.parent.size:
                    insert_pos += 1

                return current_node




        # case 3b
        elif neighbour.size == self.min_deg - 1:

            if neighbour_side == 0:
                neighbour = add(neighbour, parent_val)
                new_node = merge_nodes(neighbour, current_node)
            else:
                current_node = add(current_node, parent_val)
                new_node = merge_nodes(current_node, neighbour)

            if current_node.parent is not None:
                remove(current_node.parent, parent_val)

            if current_node.parent.size == 0:
                if current_node.parent.is_root:
                    new_node.is_root = True
                    self.root = new_node
                    new_node.parent = None

                else:
                    new_node.parent = current_node.parent.parent

            else:
                if insert_pos >= current_node.parent.size:
                    current_node.parent.items[- 1].right_link = new_node
                elif insert_pos == 0:
                    current_node.parent.items[0].left_link = new_node
                else:
                    current_node.parent.items[insert_pos - 1].right_link = new_node
                    current_node.parent.items[insert_pos].left_link = new_node

            for item in new_node.items:
                if item.left_link is not None:
                    item.left_link.parent = new_node
                else:
                    break
            if new_node.items[-1].right_link is not None:
                new_node.items[-1].right_link.parent = new_node

            return new_node

    def get_position(self, element):
        current_node = self.root

        while current_node.has_children:

            # check to see if it is a minimal node (root cannot be minimal node)
            if not current_node.is_root and current_node.size == self.min_deg - 1:
                current_node = self.case3(current_node, insert_pos, element)

            insert_pos = word_binary_search(current_node.bare_items, 0, current_node.size - 1, element)

            if insert_pos >= current_node.size:
                current_node = current_node.items[-1].right_link

                if current_node.items[-1].value == element:
                    return current_node, insert_pos
            else:
                node_element = current_node.items[insert_pos]
                if node_element.value > element:
                    current_node = node_element.left_link
                elif node_element.value < element:
                    current_node = node_element.right_link
                else:
                    return current_node, insert_pos

        if not current_node.is_root and current_node.size == self.min_deg - 1:
            current_node = self.case3(current_node, insert_pos, element)

        insert_pos = word_binary_search(current_node.bare_items, 0, current_node.size - 1, element)
        if insert_pos == current_node.size:
            return None

        if current_node.bare_items[insert_pos] == element:
            return current_node, insert_pos
        return None

    def insert_element(self, element):
        current_node = self.root

        while current_node.has_children:
            if current_node.size == 2 * self.min_deg - 1:
                self.balance_tree(current_node)
            insert_pos = word_binary_search(current_node.bare_items, 0, current_node.size - 1, element)

            # check for edge case of end of list
            if insert_pos == current_node.size:
                current_node = current_node.items[-1].right_link

                if current_node.items[-1].value == element:
                    return self
            else:
                node_element = current_node.items[insert_pos]
                if node_element.value > element:
                    current_node = node_element.left_link
                elif node_element.value < element:
                    current_node = node_element.right_link
                else:
                    return self
        current_node = add(current_node, element)
        if current_node.size == 2 * self.min_deg - 1:
            self.balance_tree(current_node)

        return self

    def balance_tree(self, current_node):

        if current_node.size < 2 * self.min_deg - 1:
            return self


        else:
            # split and return operation on parent
            split_pos = int(current_node.size // 2)

            split_val = current_node.bare_items[split_pos]

            # CASE root node
            if current_node.is_root:
                self.root = Node([Element(split_val)])
                self.root.bare_items = [split_val]
                self.root.is_root = True
                self.root.has_children = True
                current_node.parent = self.root

                new_left_items = current_node.items[:split_pos]
                new_right_items = current_node.items[split_pos + 1:]
                new_left_node = Node(new_left_items, current_node.parent)
                new_right_node = Node(new_right_items, current_node.parent)

                new_left_node.bare_items = [item.value for item in new_left_node.items]

                for item in new_left_node.items:
                    if (item.left_link is not None) or (item.right_link is not None):
                        new_left_node.has_children = True
                        break

                new_right_node.bare_items = [item.value for item in new_right_node.items]

                for item in new_right_node.items:
                    if (item.left_link is not None) or (item.right_link is not None):
                        new_right_node.has_children = True
                        break

                self.root.items[0].left_link = new_left_node
                self.root.items[0].right_link = new_right_node





            # Case internal node
            else:
                parent_insert = word_binary_search(current_node.parent.bare_items, 0, current_node.parent.size - 1,
                                                   split_val)
                current_node.parent = add(current_node.parent, split_val)

                new_left_items = current_node.items[:split_pos]
                new_right_items = current_node.items[split_pos + 1:]
                new_left_node = Node(new_left_items, current_node.parent)
                new_right_node = Node(new_right_items, current_node.parent)

                new_left_node.bare_items = [item.value for item in new_left_node.items]

                for item in new_left_node.items:
                    if (item.left_link is not None) or (item.right_link is not None):
                        new_left_node.has_children = True
                        break

                new_right_node.bare_items = [item.value for item in new_right_node.items]

                for item in new_right_node.items:
                    if (item.left_link is not None) or (item.right_link is not None):
                        new_right_node.has_children = True
                        break

                # assign children
                if parent_insert == current_node.parent.size - 1:
                    current_node.parent.items[parent_insert].left_link = new_left_node
                    current_node.parent.items[parent_insert].right_link = new_right_node
                    current_node.parent.items[parent_insert - 1].right_link = new_left_node
                    # assign parents to left and right nodes from previous recursion

                elif parent_insert == 0:
                    current_node.parent.items[parent_insert].left_link = new_left_node
                    current_node.parent.items[parent_insert].right_link = new_right_node
                    current_node.parent.items[parent_insert + 1].left_link = new_right_node

                else:
                    current_node.parent.items[parent_insert].left_link = new_left_node
                    current_node.parent.items[parent_insert].right_link = new_right_node
                    current_node.parent.items[parent_insert - 1].right_link = new_left_node
                    current_node.parent.items[parent_insert + 1].left_link = new_right_node

            if current_node.has_children:
                index = 0
                for i in range(new_left_node.size):
                    current_node.items[i].left_link.parent = new_left_node
                    index += 1
                current_node.items[len(new_left_items) - 1].right_link.parent = new_left_node

                for i in range(index + 1, current_node.size):
                    current_node.items[i].left_link.parent = new_right_node
                current_node.items[-1].right_link.parent = new_right_node

            return self.balance_tree(current_node.parent)

    def delete(self, element):
        element_location = self.get_position(element)
        if element_location is None:
            return "Element not in tree"

        node = element_location[0]  # houses case 3 adjustments
        position = element_location[1]

        # Case 2:
        if node.has_children:
            # 2a
            if node.items[position].left_link.size >= self.min_deg:
                # Get the inorder predecessor to element
                new_val = get_inorder_pre(node.items[position].left_link)

                # delete the new value element from the tree
                self.delete(new_val)

                # swap it to new value thereby deleting element
                node.items[position].value = new_val
                node.bare_items[position] = new_val

            # 2b
            elif node.items[position].right_link.size >= self.min_deg:
                # Get the inorder successor to element
                new_val = get_inorder_post(node.items[position].right_link)

                # delete the new value element from the tree
                self.delete(new_val)

                # swap it to new value thereby properly deleting element
                node.items[position].value = new_val
                node.bare_items[position] = new_val

            # 2c
            elif node.items[position].right_link.size == node.items[position].left_link.size == self.min_deg - 1:

                # assign new node to current node and remove element from current node
                node1 = node.items[position].left_link
                node2 = node.items[position].right_link
                node1 = add(node1, element)
                new_node = merge_nodes(node1, node2)
                node = remove(node, element)
                if node.size > 1:
                    if position == 0:
                        node.items[position + 1].left_link = new_node
                    # don't bother adding in the next element's left link if we deleted the last element
                    elif position >= node.size:
                        node.items[-1].right_link = new_node
                    else:
                        node.items[position - 1].right_link = new_node
                        node.items[position].left_link = new_node
                else:
                    if element < node.bare_items[0]:
                        node.items[0].left_link = new_node
                    else:
                        node.items[0].right_link = new_node

                # recursively delete
                self.delete(element)

        # Case 1: trivial delete
        if node.size > self.min_deg - 1 and not node.has_children:
            remove(node, element)
            return self

        # deleting final node
        elif not node.has_children and node.is_root:
            if node.size > 1:
                node = remove(node, element)
            else:
                self.root = Node([])
            return self

        # Case for deleting an entire node
        elif node.size == 1 and not node.has_children:
            insert_pos = word_binary_search(node.parent.bare_items, 0, node.parent.size - 1, element)
            if insert_pos == node.parent.size:
                if element > node.parent.bare_items[-1]:
                    node.parent.items[-1].right_link = None
                    add(node.parent.items[-1].left_link, node.parent.bare_items[-1])
                    link_left = node.parent.items[-1].left_link
                    remove(node.parent, node.parent.bare_items[-1])
                    if node.parent.is_root and node.parent.size == 0:
                        link_left.is_root = True
                        self.root = link_left
                        self.root.parent = None



            elif insert_pos == 0:
                node.parent.items[0].left_link = None
                add(node.parent.items[0].right_link, node.parent.bare_items[0])  # TODO: add indicies explicit
                link_right = node.parent.items[0].right_link
                remove(node.parent, node.parent.bare_items[0])
                if node.parent.is_root and node.parent.size == 0:
                    link_right.is_root = True
                    self.root = link_right
                    self.root.parent = None


            else:
                node.parent.items[insert_pos].left_link = None
                node.parent.items[insert_pos - 1].right_link = None

                add(node.parent.items[insert_pos - 1].left_link, node.parent.bare_items[insert_pos - 1])
                node.parent.items[insert_pos].left_link = node.parent.items[insert_pos - 1].left_link
                link_left = node.parent.items[insert_pos - 1].left_link
                remove(node.parent, node.parent.bare_items[insert_pos - 1])
                if node.parent.is_root and node.parent.size == 0:
                    link_left.is_root = True
                    self.root = link_left
                    self.root.parent = None

        return self


def is_even(n):
    return not n % 2


def create_Btree(min_deg):
    # initialise the tree
    root = Node()
    root.is_root = True
    my_tree = BTree(root, min_deg)
    return my_tree


def word_binary_search(words, start, end, word):
    while start < end:

        mid = (start + end) // 2

        if words[mid] == word:
            return mid

        if words[mid] > word:
            end = mid - 1

        else:
            start = mid + 1

    if word > words[start]:
        return start + 1
    if words[start] == word:
        return start
    else:
        return start


def output_ordered_Btree_aux(tree):
    root = tree.root
    return output_ordered_Btree(root, [])


def output_ordered_Btree(node, elements=[]):
    if not node.has_children:
        for item in node.items:
            elements.append(item.value)
        return elements

    for item in node.items:
        if item.left_link is not None:
            elements += output_ordered_Btree(item.left_link, [])
            elements.append(item.value)
    elements += output_ordered_Btree(node.items[-1].right_link, [])
    return elements


if __name__ == '__main__':

    # _, t, filename1, filename2 = sys

    t = 2
    filename1 = "dictionary.txt"
    filename2 = "commands.txt"

    tree = create_Btree(t)

    # read in dictionary words

    dict_file = open(filename1, 'r')
    Lines = dict_file.readlines()
    for line in Lines:
        tree.insert_element(line.strip())
    dict_file.close()

    # read in commands
    comm_file = open(filename2, 'r')
    Lines2 = comm_file.readlines()
    for line in Lines2:
        line_array = line.split(" ")
        if line_array[0] == "delete":
            tree.delete(str(line_array[1].strip()))
        elif line_array[0] == "insert":
            tree.insert_element(str(line_array[1].strip()))

    inorder_output = output_ordered_Btree_aux(tree)

    comm_file.close()

    with open('output_btree.txt', 'w') as f:
        for item in inorder_output:
            f.write(str(item))
            f.write('\n')

    f.close()

