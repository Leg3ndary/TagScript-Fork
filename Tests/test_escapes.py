import bTagScript as tse

blocks = [
    tse.MathBlock(),
    tse.RandomBlock(),
    tse.RangeBlock(),
    tse.AnyBlock(),
    tse.IfBlock(),
    tse.AllBlock(),
    tse.BreakBlock(),
    tse.StrfBlock(),
    tse.StopBlock(),
    tse.VarBlock(),
    tse.LooseVariableGetterBlock(),
    tse.EmbedBlock(),
    tse.ReplaceBlock(),
    tse.PythonBlock(),
    tse.URLEncodeBlock(),
    tse.RequireBlock(),
    tse.BlacklistBlock(),
    tse.CommandBlock(),
    tse.OverrideBlock(),
]
engine = tse.Interpreter(blocks)

msg = tse.escape_content("message provided :")
response = engine.process("{if({msg}==):provide a message|{msg}}", {"msg": tse.StringAdapter(msg)})

print(response)
print(response.body)
