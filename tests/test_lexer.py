#  To test the lexer functionality
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer.lexer import Lexer, TokenType


def test_basic_formula():
    lexer = Lexer("SUM(A1:B5)+10")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.FUNCTION
    assert tokens[2].type == TokenType.RANGE
    assert tokens[-1].type == TokenType.EOF
