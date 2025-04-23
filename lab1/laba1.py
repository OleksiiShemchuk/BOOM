from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class ChainBuilder:
    def __init__(self):
        self.chain = []
        self.blocks = {}
        self.votes = {}
        self.tree_root = None

    def add_block(self, block):
        view = block['view']
        if view not in self.blocks:
            self.blocks[view] = []
        self.blocks[view].append(block)
        self.try_extend_chain()
        if 'value' in block:
            self.tree_root = self.insert(self.tree_root, block['value'])

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

    def insert(self, node, value):
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self.insert(node.left, value)
        else:
            node.right = self.insert(node.right, value)
        return node

    def analyze_tree(self):
        types = []
        if self.is_complete(self.tree_root):
            types.append("complete")
        if self.is_full(self.tree_root):
            types.append("full")
        if self.is_perfect(self.tree_root):
            types.append("perfect")
        return types

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

    def tree_depth(self, node):
        if node is None:
            return 0
        return 1 + max(self.tree_depth(node.left), self.tree_depth(node.right))

    def is_perfect(self, root):
        def check(node, depth, level=0):
            if node is None:
                return True
            if node.left is None and node.right is None:
                return depth == level + 1
            if node.left is None or node.right is None:
                return False
            return check(node.left, depth, level + 1) and check(node.right, depth, level + 1)

        depth = self.tree_depth(root)
        return check(root, depth)

    def print_traversals(self):
        print("\nTree traversals:")
        print("Pre-order:", end=' ')
        self.preorder(self.tree_root)
        print("\nIn-order:", end=' ')
        self.inorder(self.tree_root)
        print("\nPost-order:", end=' ')
        self.postorder(self.tree_root)
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

    def get_input(self):
        while True:
            print("\nCurrent chain:", [b['id'] for b in self.chain])
            command = input("\nEnter command (block/vote/analyze/end): ").strip().lower()
            
            if command == "end":
                break
                
            elif command == "block":
                try:
                    block_id = input("Enter unique block ID: ").strip()
                    if not block_id:
                        raise ValueError("Block ID cannot be empty")
                        
                    view = int(input("Enter block view: "))
                    value = float(input("Enter block value: "))
                    
                    block = {
                        'id': block_id,
                        'view': view,
                        'value': value
                    }
                    self.add_block(block)
                    print(f"Block {block_id} added successfully!")
                    
                except ValueError as e:
                    print(f"Error: {e}. Please enter valid input.")
                    
            elif command == "vote":
                try:
                    block_id = input("Enter block ID to vote for: ").strip()
                    if not block_id:
                        raise ValueError("Block ID cannot be empty")
                        
                    vote = {'block_id': block_id}
                    self.add_vote(vote)
                    print(f"Vote for block {block_id} recorded!")
                    
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif command == "analyze":
                if not self.chain:
                    print("Chain is empty! Add blocks first.")
                elif not self.tree_root:
                    print("No values available for tree analysis.")
                else:
                    types = self.analyze_tree()
                    print("\nTree analysis results:")
                    print("Type:", ", ".join(types) if types else "No specific type")
                    print("Depth:", self.tree_depth(self.tree_root))
                    self.print_traversals()
                    
            else:
                print("Invalid command! Available commands: block, vote, analyze, end")

if __name__ == "__main__":
    print("=== Blockchain Tree Builder ===")
    print("Commands: block, vote, analyze, end")
    builder = ChainBuilder()
    builder.get_input()