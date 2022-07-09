import time

from bTagScript import Interpreter, adapter, block

blocks = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
    block.StrfBlock(),
    block.AssignmentBlock(),
    block.FiftyFiftyBlock(),
    block.LooseVariableGetterBlock(),
]
x = Interpreter(blocks)

dummy = {"message": adapter.StringAdapter("Hello, this is my message.")}


def timerfunc(func):
    """
    A timer decorator
    """

    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "The runtime for {func} took {time} seconds to complete 1,000 times"
        print(msg.format(func=func.__name__, time=runtime))
        return value

    return function_timer


@timerfunc
def v2_test():
    """
    V2 Testing benchmarks
    """
    for _ in range(1000):
        x.process(
            "{message} {#:1,2,3,4,5,6,7,8,9,10} {range:1-9} {#:1,2,3,4,5} {message} {strf:Its %A}",
            dummy,
        )


if __name__ == "__main__":
    v2_test()
