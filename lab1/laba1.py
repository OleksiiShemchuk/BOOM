from collections import deque


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TreeAnalyzer:
    def __init__(self, chain):
        self.root = None
        values = [b['value'] for b in chain]
        for val in values:
            self.root = self.insert(self.root, val)

    def insert(self, node, value):
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self.insert(node.left, value)
        else:
            node.right = self.insert(node.right, value)
        return node

    def tree_depth(self, node):
        if node is None:
            return 0
        return 1 + max(self.tree_depth(node.left), self.tree_depth(node.right))

    def is_full(self, node):
        if node is None:
            return True
        if (node.left is None) != (node.right is None):
            return False
        return self.is_full(node.left) and self.is_full(node.right)

    def is_complete(self, root):
        if root is None:
            return True
        queue = deque([root])
        end = False
        while queue:
            current = queue.popleft()
            if current.left:
                if end:
                    return False
                queue.append(current.left)
            else:
                end = True
            if current.right:
                if end:
                    return False
                queue.append(current.right)
            else:
                end = True
        return True

    def is_perfect(self, root):
        def check(node, depth, level=0):
            if node is None:
                return True
            if node.left is None and node.right is None:
                return depth == level + 1
            if node.left is None or node.right is None:
                return False
            return check(node.left, depth, level + 1) and check(node.right, depth, level + 1)
        return check(root, self.tree_depth(root))

    def analyze(self):
        types = []
        if self.is_complete(self.root):
            types.append("complete")
        if self.is_full(self.root):
            types.append("full")
        if self.is_perfect(self.root):
            types.append("perfect")
        return types

    def print_traversals(self):
        print("\nTree traversals:")
        print("Pre-order:", end=' ')
        self.preorder(self.root)
        print("\nIn-order:", end=' ')
        self.inorder(self.root)
        print("\nPost-order:", end=' ')
        self.postorder(self.root)
        print()

    def preorder(self, node):
        if node:
            print(node.value, end=' ')
            self.preorder(node.left)
            self.preorder(node.right)

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.value, end=' ')
            self.inorder(node.right)

    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.value, end=' ')

class ChainBuilder:
    def __init__(self):
        self.chain = []
        self.blocks = {}
        self.votes = {}

    def add_block(self, block):
        view = block['view']
        if view not in self.blocks:
            self.blocks[view] = []
        self.blocks[view].append(block)
        self.try_extend_chain()

    def add_vote(self, vote):
        block_id = vote['block_id']
        self.votes[block_id] = vote
        self.try_extend_chain()

    def try_extend_chain(self):
        while True:
            next_view = len(self.chain)
            if next_view not in self.blocks:
                break
            candidates = self.blocks[next_view]
            for block in candidates:
                if block['id'] in self.votes:
                    self.chain.append(block)
                    del self.votes[block['id']]
                    break
            else:
                break

    def get_chain(self):
        return self.chain

    def get_input(self):
        while True:
            print("\nFinal chain blocks:")
            for b in self.chain:
                print(f"ID: {b['id']}, View: {b['view']}, Value: {b['value']}")
            command = input("\nEnter command (block/vote/end): ").strip().lower()

            if command == "end":
                break

            elif command == "block":
                try:
                    block_id = input("Enter unique block ID: ").strip()
                    view = int(input("Enter block view: "))
                    value = float(input("Enter block value: "))
                    block = {'id': block_id, 'view': view, 'value': value}
                    self.add_block(block)
                    print(f"Block {block_id} added successfully!")
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "vote":
                try:
                    block_id = input("Enter block ID to vote for: ").strip()
                    vote = {'block_id': block_id}
                    self.add_vote(vote)
                    print(f"Vote for block {block_id} recorded!")
                except ValueError as e:
                    print(f"Error: {e}")

            else:
                print("Invalid command! Available commands: block, vote, end")


if __name__ == "__main__":
    print("=== Blockchain ChainBuilder ===")
    print("Commands: block, vote, end")
    builder = ChainBuilder()
    builder.get_input()

    chain = builder.get_chain()
    
    if chain:
        analyzer = TreeAnalyzer(chain)
        types = analyzer.analyze()
        print("\nTree analysis results:")
        print("Type:", ", ".join(types) if types else "No specific type")
        print("Depth:", analyzer.tree_depth(analyzer.root))
        analyzer.print_traversals()
    else:
        print("\nNo blocks in chain, skipping tree analysis.")
