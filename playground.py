from appJar import gui

from bTagScript import Interpreter, block

blocks = [
    block.BreakBlock(),
    block.CommentBlock(),
    block.AllBlock(),
    block.AnyBlock(),
    block.IfBlock(),
    block.CountBlock(),
    block.LengthBlock(),
    block.BlacklistBlock(),
    block.CommandBlock(),
    block.CooldownBlock(),
    block.DeleteBlock(),
    block.EmbedBlock(),
    block.OverrideBlock(),
    block.ReactBlock(),
    block.RedirectBlock(),
    block.RequireBlock(),
    block.MathBlock(),
    block.OrdinalAbbreviationBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
    block.PythonBlock(),
    block.ReplaceBlock(),
    block.StopBlock(),
    block.StrfBlock(),
    block.URLDecodeBlock(),
    block.URLEncodeBlock(),
    block.DebugBlock(),
    block.VarBlock(),
    block.LooseVariableGetterBlock(),
]
x = Interpreter(blocks)

DEFAULT = r"""{=(smth):Hello, how are you doing today?}
{smth}
{$parsed:{smth(-1)}}
{parsed} {debug}"""


def press(button: gui.button) -> None:  # pylint: disable=unused-argument
    """
    Button press handler.
    """
    response = x.process(app.getTextArea("input"))
    app.clearTextArea("output")
    app.setTextArea("output", response.body)
    app.clearTextArea("actions")
    app.setTextArea("actions", response.extras.get("debug", r"{}"))  # pylint: disable=no-member


app = gui("TSE Playground", "750x450")
app.setPadding([2, 3])
app.setInPadding([2, 3])
app.addTextArea("input", text=DEFAULT, row=0, column=0)
app.addTextArea("output", text="Press process to continue", row=0, column=1)
app.addTextArea("actions", text="Actions will be added here", row=1, column=0)
app.addButton("Process", press, row=1, column=1, colspan=2)

app.go()
