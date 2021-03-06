# import the necessary packages
from PIL import Image
import numpy as np
import flask
import io

import constants, configurations, utils

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)

existing_board = []


@app.route("/digitize_board", methods=["POST"])
def digitize_chess_board():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            gameid = flask.request.form["gameid"]
            move_number = flask.request.form["move_number"]

            print(gameid)
            print(move_number)

            if gameid and move_number and image:
                if len(existing_board) > 0:
                    current_element = utils.simulate_move()
                else:
                    current_element = utils.generate_dummy_board()
                existing_board.append(current_element)

                data["board"] = existing_board
                # indicate that the request was a success
                data["success"] = True


    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":

    app.run()
