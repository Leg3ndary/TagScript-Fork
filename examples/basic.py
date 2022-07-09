from bTagScript import Interpreter, block

blocks = [
    block.RandomBlock(),
    block.LooseVariableGetterBlock(),
]

intepreter = Interpreter(blocks)

TAGSCRIPT = """{=(statuses):Happy~Sad~Angry}{#:{statuses}}"""

response = intepreter.process(TAGSCRIPT)

print(response.body)
