"""
An example of a simple API you can use to process tagscript.
"""

from flask import Flask, jsonify

import bTagScript as tse

tse_blocks = [
    tse.block.BreakBlock(),
    tse.block.CommentBlock(),
    tse.block.AllBlock(),
    tse.block.AnyBlock(),
    tse.block.IfBlock(),
    tse.block.CountBlock(),
    tse.block.LengthBlock(),
    tse.block.BlacklistBlock(),
    tse.block.CommandBlock(),
    tse.block.CooldownBlock(),
    tse.block.DeleteBlock(),
    tse.block.EmbedBlock(),
    tse.block.OverrideBlock(),
    tse.block.ReactBlock(),
    tse.block.RedirectBlock(),
    tse.block.RequireBlock(),
    tse.block.MathBlock(),
    tse.block.OrdinalAbbreviationBlock(),
    tse.block.RandomBlock(),
    tse.block.RangeBlock(),
    tse.block.PythonBlock(),
    tse.block.ReplaceBlock(),
    tse.block.StopBlock(),
    tse.block.StrfBlock(),
    tse.block.URLDecodeBlock(),
    tse.block.URLEncodeBlock(),
    tse.block.DebugBlock(),
    tse.block.VarBlock(),
    tse.block.LooseVariableGetterBlock(),
]

tsei = tse.interpreter.Interpreter(blocks=tse_blocks)

app = Flask(__name__)


@app.route("/")
def main() -> None:
    """
    Main function to return "Status"
    """
    return {"Status": "Alive"}


@app.route("/process/<string:tagscript>")
def process(tagscript: str) -> None:
    """
    Main function to return "Status"
    """

    output = tsei.process(tagscript)

    response = {"body": output.body, "actions": output.actions, "extras": output.extras}

    return jsonify(response)


app.run(host="0.0.0.0, port=8080")
