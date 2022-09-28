import os

from flask import Flask, request
from flask_cors import CORS, cross_origin

from tictactoe.tictactoe import TicTacToe, WIN_STATUS, NONE_STATUS


BOARD_SIZE = os.environ.get('REACT_APP_BOARD_SIZE') or 3
WIN_SIZE = os.environ.get('WIN_SIZE') or 3

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
ttt: TicTacToe = None


@app.route("/start_game", methods=["GET"])
@cross_origin()
def start_game():
    """
    Game init route
    """
    global ttt
    ttt = TicTacToe(int(BOARD_SIZE), int(WIN_SIZE))
    return {"status": NONE_STATUS}


@app.route("/set_value", methods=["POST"])
@cross_origin()
def set_value():
    """
    Set X or O in cell endpoint
    """
    global ttt
    if ttt is None:
        return {"error": "Game not started"}
    cords = request.json.get("cords")
    value = request.json.get("value")
    response = ttt.change_cell_value(cords, value)
    if response["status"] == WIN_STATUS:
        ttt = None
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)