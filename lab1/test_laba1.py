import unittest
from laba1 import ChainBuilder

class TestChainBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = ChainBuilder()

    def test_add_block_and_vote_in_order(self):
        block = {'id': 'B0', 'view': 0}
        self.builder.add_block(block)
        self.builder.add_vote({'block_id': 'B0'})
        self.assertEqual(len(self.builder.chain), 1)
        self.assertEqual(self.builder.chain[0]['id'], 'B0')

    def test_add_vote_before_block(self):
        self.builder.add_vote({'block_id': 'B0'})
        self.builder.add_block({'id': 'B0', 'view': 0})
        self.assertEqual(len(self.builder.chain), 1)

    def test_unvoted_blocks_not_added(self):
        self.builder.add_block({'id': 'B0', 'view': 0})
        self.builder.add_block({'id': 'B1', 'view': 1})
        self.assertEqual(len(self.builder.chain), 0)

    def test_multiple_candidates_in_same_view(self):
        b1 = {'id': 'B0a', 'view': 0}
        b2 = {'id': 'B0b', 'view': 0}
        self.builder.add_block(b1)
        self.builder.add_block(b2)
        self.builder.add_vote({'block_id': 'B0a'})
        self.assertEqual(len(self.builder.chain), 1)
        self.assertEqual(self.builder.chain[0]['id'], 'B0a')

    def test_gap_in_views_halts_extension(self):
        self.builder.add_block({'id': 'B0', 'view': 0})
        self.builder.add_block({'id': 'B2', 'view': 2})
        self.builder.add_vote({'block_id': 'B0'})
        self.builder.add_vote({'block_id': 'B2'})
        self.assertEqual(len(self.builder.chain), 1)

if __name__ == '__main__':
    unittest.main()