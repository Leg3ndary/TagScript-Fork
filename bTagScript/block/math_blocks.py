from __future__ import division

import math
import operator
from typing import Optional as Optional_

from pyparsing import (
    CaselessLiteral,
    Combine,
    Forward,
    Group,
    Literal,
    Optional,
    Word,
    ZeroOrMore,
    alphas,
    nums,
    oneOf,
)

from ..interface import Block
from ..interpreter import Context


class NumericStringParser(object):
    """
    Most of this code comes from the fourFn.py pyparsing example

    """

    def pushFirst(self, strg: str, loc, toks) -> None:  # pylint: disable=unused-argument
        """
        Parse actions that push the first element of the matched tokens
        """
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg: str, loc, toks) -> None:  # pylint: disable=unused-argument
        """
        Parse actions that push the last element of the matched tokens??
        """
        if toks and toks[0] == "-":
            self.exprStack.append("unary -")

    def __init__(self) -> None:
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        self.exprStack = []
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(
            Word("+-" + nums, nums)
            + Optional(point + Optional(Word(nums)))
            + Optional(e + Word("+-" + nums, nums))
        )
        ident = Word(alphas, alphas + nums + "_$")
        mod = Literal("%")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        iadd = Literal("+=")
        imult = Literal("*=")
        idiv = Literal("/=")
        isub = Literal("-=")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div | mod
        iop = iadd | isub | imult | idiv
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = (
            (
                Optional(oneOf("- +"))
                + (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst)
            )
            | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
        ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore(  # pylint: disable=expression-not-assigned
            (expop + factor).setParseAction(self.pushFirst)
        )
        term = factor + ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + ZeroOrMore(  # pylint: disable=expression-not-assigned
            (addop + term).setParseAction(self.pushFirst)
        )
        final = expr + ZeroOrMore((iop + expr).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = final
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {
            "+": operator.add,
            "-": operator.sub,
            "+=": operator.iadd,
            "-=": operator.isub,
            "*": operator.mul,
            "*=": operator.imul,
            "/": operator.truediv,
            "/=": operator.itruediv,
            "^": operator.pow,
            "%": operator.mod,
        }
        self.fn = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "exp": math.exp,
            "abs": abs,
            "trunc": lambda a: int(a),  # pylint: disable=unnecessary-lambda
            "round": round,
            "sgn": lambda a: abs(a) > epsilon and ((a > 0) - (a < 0)) or 0,
            "log": lambda a: math.log(a, 10),
            "ln": math.log,
            "log2": math.log2,
            "sqrt": math.sqrt,
        }

    def evaluateStack(self, s):
        """
        Evaluate the expression on the input data in the stack.
        """
        op = s.pop()
        final = None
        if op == "unary -":
            final = -self.evaluateStack(s) # pylint: disable=invalid-unary-operand-type
        elif op in self.opn:
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            final = self.opn[op](op1, op2)
        elif op == "PI":
            final = math.pi  # 3.1415926535
        elif op == "E":
            final = math.e  # 2.718281828
        elif op in self.fn:
            final = self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            final = 0
        if final is not None:
            return final
        return float(op)

    def eval(self, num_string: str, parseAll: bool = True) -> float:
        """
        Evaluate the expression on the input data.
        """
        # results = self.bnf.parseString(num_string, parseAll)  # pylint: disable=unused-variable
        self.bnf.parseString(num_string, parseAll)
        return self.evaluateStack(self.exprStack[:])


NSP = NumericStringParser()


class MathBlock(Block):
    """
    A math block is a block that contains a math expression.
    If the block fails to parse if will return the declaration
    plus error like so: `<math error>`, <+ error> etc.

    **Usage:** ``{math:<expression>}``

    **Aliases:** ``math, m, +, calc``

    **Payload:** ``expression``

    **Parameter:** None

    **Examples:**

    .. tagscript::

        {m:2+3}
        5.0

        {math:7(2+3)}
        42.0

        {math:trunc(7(2+3))}
        42
    """

    ACCEPTED_NAMES = ("math", "m", "+", "calc")

    def process(self, ctx: Context) -> Optional_[str]:
        """
        Try and process the block into a float
        """
        try:
            return str(NSP.eval(ctx.verb.payload.strip(" ")))
        except:  # pylint: disable=bare-except
            return f"<{ctx.verb.declaration} error>"


class OrdinalAbbreviationBlock(Block):
    """
    The ordinalabbreviation block returns the ordinal abbreviation of a number.
    If a parameter is provided, it must be, one of, c, comma, indicator, i
    Comma being adding commas every 3 digits, indicator, meaning the ordinal indicator.
    (The st of 1st, nd of 2nd, etc.)

    The number may be positive or negative, if the payload is invalid, the
    declaration plus error is returned.

    **Usage:** ``{ord(["c", "comma", "i", "indicator"]):<number>}``

    **Aliases:** ``None``

    **Payload:** ``number``

    **Parameter:** ``"c", "comma", "i", "indicator"``

    .. tagscript::

        {ord:1000}
        1,000th

        {ord(c):1213123}
        1,213,123

        {ord(i):2022}
        2022nd
    """

    ACCEPTED_NAMES = ("ord",)

    def process(self, ctx: Context) -> str:
        """
        Process the ordinal abbreviation block
        """
        num = ctx.verb.payload.split("-", 1)[-1]
        if num.isdigit():
            comma = f"{int(num):,}"
            if ctx.verb.parameter in ["c", "comma"]:
                return comma
            i = int(ctx.verb.payload.split("-", 1)[-1])
            indicator = "tsnrhtdd"[
                (i // 10 % 10 != 1) * (i % 10 < 4) * i % 10 :: 4
            ]  # I stole this from stack overflow
            if ctx.verb.parameter in ["i", "indicator"]:
                return f"{ctx.verb.payload}{indicator}"  # concatenation is slower?
            return f"{comma}{indicator}"
        return f"<{ctx.verb.declaration} error>"
