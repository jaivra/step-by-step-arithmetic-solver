import itertools

from core.MalformedExpression import MalformedExpression


class PARENTH_TYPE:
    UNKNOWN = 0
    SIMPLE = 1
    FREE = 2


class BLOCK_TYPE:
    ROUND = 1
    SQUARE = 2
    CURLY = 3
    INIT = 4


class ExprBlock:
    _count = itertools.count(0)

    def __init__(self, block_type, sub_blocks, tree):
        self._block_type = block_type
        self._tree = tree
        self._sub_blocks = sub_blocks
        self._cnt = next(ExprBlock._count)
        self._depth = -1

        if block_type == BLOCK_TYPE.ROUND or block_type == BLOCK_TYPE.INIT:
            self._parenth_type = PARENTH_TYPE.UNKNOWN
        else:
            self._parenth_type = PARENTH_TYPE.SIMPLE

        self._parenth_type = self._find_parenth_type(sub_blocks)

    def _find_parenth_type(self, sub_blocks):

        if len(sub_blocks) == 0:
            return self._parenth_type

        block_types = set(block.block_type for block in sub_blocks)
        parenth_types = set(block.parenth_type for block in sub_blocks) - {PARENTH_TYPE.UNKNOWN}

        #print((self._parenth_type, self._tree), '\n\n')
        #for block in self._sub_blocks:
        #    print((block.parenth_type, block.tree), '\n')
        #print('\n\n\n\n')
        if len(parenth_types) == 0:
            max_sub_blocks_grade = max(block_types)

            if self._block_type > max_sub_blocks_grade:
                return PARENTH_TYPE.SIMPLE

            if self._block_type == max_sub_blocks_grade == BLOCK_TYPE.ROUND:
                return PARENTH_TYPE.FREE

        elif len(parenth_types) == 1:
            parenth_ref = parenth_types.pop()
            if parenth_ref == self._parenth_type: return parenth_ref
            if self._parenth_type == PARENTH_TYPE.UNKNOWN and (parenth_ref == PARENTH_TYPE.SIMPLE or parenth_ref == PARENTH_TYPE.FREE):
                return PARENTH_TYPE.FREE

        raise MalformedExpression(
            'Errore nell\'annidamento delle parentesi, regole di parentesizzazione non rispettate, ', [], [], []
        )

    @property
    def tree(self):
        return self._tree

    @property
    def depth(self):
        return self._depth

    @property
    def cnt(self):
        return self._cnt

    @property
    def block_type(self):
        return self._block_type

    @property
    def parenth_type(self):
        return self._parenth_type

    def generate_sorted_trees_list(self):
        blocks = self._generate_trees_list()
        sorted_blocks = sorted(blocks)
        res = [(block.ID, block.tree) for block in sorted_blocks]
        return res

    def _generate_trees_list(self):
        blocks = [block._generate_trees_list() for block in self._sub_blocks]
        return [item for sublist in blocks for item in sublist] + [self]

    @property
    def ID(self):
        return f'{self._cnt}'

    def __lt__(self, other):
        if self._block_type < other.block_type: return True
        if self._block_type == other.block_type:
            if self._depth > other.depth: return True
            if self._depth == other.depth and self._cnt < other.cnt: return True
        return False

    def __repr__(self):
        return str(self._cnt)

    def build(self, depth=0):
        self._depth = depth
        for block in self._sub_blocks:
            block.build(depth + 1)
