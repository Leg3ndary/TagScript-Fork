from appJar import gui

from bTagScript import Interpreter, block

blocks = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
    block.AnyBlock(),
    block.IfBlock(),
    block.AllBlock(),
    block.BreakBlock(),
    block.StrfBlock(),
    block.StopBlock(),
    block.AssignmentBlock(),
    block.FiftyFiftyBlock(),
    block.ShortCutRedirectBlock("message"),
    block.LooseVariableGetterBlock(),
    block.SubstringBlock(),
]
x = Interpreter(blocks)

default = """{=(smth):Hello, how are you doing today?}

{smth}
{smth(-1)}
"""

def press(button):
    o = x.process(app.getTextArea("input")).body
    app.clearTextArea("output")
    app.setTextArea("output", o)


app = gui("TSE Playground", "750x450")
app.setPadding([2, 2])
app.setInPadding([2, 2])
app.addTextArea("input", text=default, row=0, column=0)
app.addTextArea("output", text="Press process to continue", row=0, column=1)
app.addButton("Process", press, row=1, column=0, colspan=2)

app.go()
