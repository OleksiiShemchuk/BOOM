class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    return root

def build_bst(blocks):
    root = None
    for block in blocks:
        if 'value' in block:
            root = insert(root, block['value'])
    return root

def is_complete(root, index, num_nodes):
    if root is None:
        return True
    if index >= num_nodes:
        return False
    return is_complete(root.left, 2 * index + 1, num_nodes) and \
           is_complete(root.right, 2 * index + 2, num_nodes)

def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)

def is_full(root):
    if root is None:
        return True
    if (root.left is None and root.right is not None) or \
       (root.left is not None and root.right is None):
        return False
    return is_full(root.left) and is_full(root.right)

def get_height(root):
    if root is None:
        return 0
    return 1 + max(get_height(root.left), get_height(root.right))

def is_perfect(root):
    if root is None:
        return True
    if root.left is None and root.right is None:
        return True
    if root.left is not None and root.right is not None:
        return is_perfect(root.left) and is_perfect(root.right) and \
               get_height(root.left) == get_height(root.right)
    return False

def determine_tree_type(root):
    num_nodes = count_nodes(root)
    if is_perfect(root):
        return "ідеальне"
    elif is_full(root):
        return "заповнене"
    elif is_complete(root, 0, num_nodes):
        return "повне"
    else:
        return "ні повне, ні заповнене, ні ідеальне"

def preorder_traversal(root):
    if root:
        print(root.value, end=" ")
        preorder_traversal(root.left)
        preorder_traversal(root.right)

def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.value, end=" ")
        inorder_traversal(root.right)

def postorder_traversal(root):
    if root:
        postorder_traversal(root.left)
        postorder_traversal(root.right)
        print(root.value, end=" ")

blocks = [
    {'id': 'a1b2c3d4', 'view': 10, 'value': 5.0},
    {'id': 'e5f6g7h8', 'view': 20, 'value': 3.0},
    {'id': 'i9j0k1l2', 'view': 15, 'value': 7.0},
    {'id': 'm3n4o5p6', 'view': 25, 'value': 2.0},
    {'id': 'q7r8s9t0', 'view': 5, 'value': 6.0}
]

bst_root = build_bst(blocks)

# Завдання 1
tree_type = determine_tree_type(bst_root)
print(f"Тип побудованого бінарного дерева пошуку: {tree_type}")

# Завдання 2
print("\nОбхід дерева (pre-order):")
preorder_traversal(bst_root)
print("\nОбхід дерева (in-order):")
inorder_traversal(bst_root)
print("\nОбхід дерева (post-order):")
postorder_traversal(bst_root)
print()