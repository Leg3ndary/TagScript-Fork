import time
from typing import Callable

from bTagScript import Interpreter, adapter, block

blocks = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
    block.StrfBlock(),
    block.VarBlock(),
    block.LooseVariableGetterBlock(),
]
x = Interpreter(blocks)

dummy = {"message": adapter.StringAdapter("Hello, this is my message.")}


def timerfunc(func: Callable) -> Callable:
    """
    A timer decorator
    """

    def function_timer(*args, **kwargs) -> None:
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        print(f"The runtime for {func.__name__} took {runtime} seconds to complete 1,000 times")
        return value

    return function_timer


@timerfunc
def v2_test() -> None:
    """
    V2 Testing benchmarks
    """
    for _ in range(1000):
        x.process(
            r"{message} {#:1,2,3,4,5,6,7,8,9,10} {range:1-9} {=(variablename):Hello World} {variablename} {message} {strf:Its %A}",
            dummy,
        )


if __name__ == "__main__":
    v2_test()
