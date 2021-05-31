from flask import Flask, request, render_template
from PIL import Image
import numpy
import os
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


def digit_to_hex(r):
    convert_list = ["A", "B", "C", "D", "E", "F"]
    d = math.floor(r / 16)
    digit_1 = d
    if d > 9:
        digit_1 = convert_list[d - 10]
    digit_2 = r % 16
    if digit_2 > 9:
        digit_2 = convert_list[digit_2 - 10]
    return f"{digit_1}{digit_2}"


def rgb_to_hex(r, g, b):
    hexadecimal = "#"
    return f"{hexadecimal}{digit_to_hex(r)}{digit_to_hex(g)}{digit_to_hex(b)}"


def most_common_item(list_of_items):
    highest = {"num": 0, "item": None}
    for item in list_of_items:
        num_occurrences = list_of_items.count(item)
        if num_occurrences > highest["num"]:
            highest["num"] = num_occurrences
            highest["item"] = item

    return highest


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        img = request.files["file"]
        img = Image.open(img)
        data = numpy.asarray(img)
        list_of_rgbs = []

        print(data)
        for list_of_data in data:
            for piece_of_data in list_of_data:
                list_of_rgbs.append(str(piece_of_data))

        most_common = most_common_item(list_of_rgbs)["item"]
        most_common = most_common[2:].split(" ")
        message = f"RGB: {most_common[0]}, {most_common[1]}, {most_common[2]}"

        hex_code = rgb_to_hex(int(most_common[0]), int(most_common[1]), int(most_common[2]))

    try:
        if message is not None:
            return render_template("index.html", message=message, hex_code=hex_code)
    except NameError:
        return render_template("index.html", message="", hex_code="#ffffff")


if __name__ == "__main__":
    app.run(debug=True)
