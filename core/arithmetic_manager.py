from liblet import ANTLR

from core.atw_block_generator import AtwBlockGenerator
from core.atw_latex_formatter import AtwLatexFormatter
from core.atw_ptree_to_ast import AtwPtreeToAst
from core.atw_expr_eval import AtwEvalExpr
from core.atw_block_priority import AtwBlockPriority


class ArithManager:

    def __init__(self):
        print("*d")
        self._atw_ptree_to_ast = AtwPtreeToAst()
        self._atw_block_generator = AtwBlockGenerator()
        self._atw_latex_formatter = AtwLatexFormatter()
        self._atw_block_priority = AtwBlockPriority()
        self._atw_eval_expr = AtwEvalExpr()

    def ptree(self, grammar_file, expr):
        with open(grammar_file, 'r') as reader:
            arith = ANTLR(reader.read())
            return arith.tree(expr, 's')

    def ptree2ast(self, ptree):
        return self._atw_ptree_to_ast(ptree)

    def blocks(self, ast):
        return self._atw_block_generator.start(ast)

    def prior(self, ast):
        return self._atw_block_priority.start(ast)

    def eval(self, ast, memory=None):
        if memory is None:
            memory = dict()
        return self._atw_eval_expr.start(ast, memory)

    def latex(self, ast, memory):
        return self._atw_latex_formatter.start(ast, memory)
