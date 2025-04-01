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

    def get_input(self):
        while True:
            command = input("Enter command (block/vote/exit): ")
            if command == "exit":
                break
            elif command == "block":
                block = {
                    'id': input("Enter block ID: "),
                    'view': int(input("Enter block view: "))
                }
                self.add_block(block)
                print(f"Chain: {[b['id'] for b in self.chain]}")
            elif command == "vote":
                vote = {
                    'block_id': input("Enter block ID to vote for: ")
                }
                self.add_vote(vote)

if __name__== "__main__":
    builder = ChainBuilder()
    builder.get_input()