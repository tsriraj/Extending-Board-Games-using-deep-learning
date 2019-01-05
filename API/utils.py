from itertools import product
import numpy as np
import random
import base64
import cv2

cols = list("abcdefgh")
rows = list("12345678")
cartesian_product = list(product(cols, rows))

board_positions = [x[0] + x[1] for x in cartesian_product]

chess_pieces = list("p"*8 + "n"*2 + "r"*2 + "b"*2 + "k" + "q")

black_pieces = ["b" + x for x in chess_pieces]
white_pieces = ["w" + x for x in chess_pieces]
all_pieces = black_pieces
all_pieces.extend(white_pieces)



def generate_dummy_board(num_pieces=32):
    chosen_positions = random.sample(board_positions, num_pieces)
    chosen_pieces = random.sample(all_pieces, num_pieces)
    return dict(zip(chosen_positions, chosen_pieces))


def simulate_move():
    moves = {}
    moves["d3"] = "wp"
    moves["d2"] = "empty"
    return moves


def base64_encode_image(image):
    """
    Ref: https://www.pyimagesearch.com/2018/01/29/scalable-keras-deep-learning-rest-api/
    Usage: 
        d = {"id": k, "image": base64_encode_image(image)}
        db.set("ID123", json.dumps(d))
    """
    # ensure our NumPy array is C-contiguous as well, otherwise we won't be able to serialize it
    image = image.copy(order="C")

    # base64 encode the input NumPy array
    return base64.b64encode(image).decode("utf-8")

def base64_decode_image(image_obj, shape, dtype="float32"):
    """
    Ref: https://www.pyimagesearch.com/2018/01/29/scalable-keras-deep-learning-rest-api/
    Usage: 
        item = json.loads(item.decode("utf-8"))
        image = base64_decode_image(item["image"], (200, 200))
    """

    image = bytes(image_obj, encoding="utf-8")

    # convert the string to a NumPy array using the supplied data type and target shape
    image = np.frombuffer(base64.decodestring(image), dtype=dtype)

    #num_channels = 3
    #required_shape = (1, shape[0], shape[1], num_channels)
    #image = image.reshape(required_shape)
    resized_image = cv2.resize(image, shape, interpolation=cv2.INTER_AREA)

    # return the decoded image
    return image
