#
# you need pil to make this work.
#   $: pip install pillow
#

import os
from sys import version_info
from PIL import Image, ImageDraw, ImageFont
import json


metadata_directory = "../sploot-generator/metadata"
card_template_directory = "templates"
card_output_directory = "cards"

overlayAnchor = (200, 100)

headerStyle = ImageFont.truetype(
    card_template_directory + "/Inter-Bold.ttf", 64)
statStyle = ImageFont.truetype(
    card_template_directory + "/Inter-Bold.ttf", 18)
traitStyle = ImageFont.truetype(
    card_template_directory + "/Inter-Regular.ttf", 16)
labelStyle = ImageFont.truetype(
    card_template_directory + "/LeagueGothic-Regular.otf", 32)
ovrStyle = ImageFont.truetype(
    card_template_directory + "/LeagueGothic-Regular.otf", 64)


def create_cards():
    # global metadata_directory

    print("============ PROCESSING CARDS ============")

    for filename in os.listdir(metadata_directory):
        if filename.endswith('.json'):
            print("opening metadata: " + metadata_directory + "/" + filename)

            with open(os.path.join(metadata_directory, filename)) as file:
                jsonString = file.read()
                index = filename.split(".")[0]
                merge_metadata(json.loads(jsonString), index)

    print("")
    print("===> Finished.")
    print("")
    main_menu()


def merge_metadata(metadata, index):

    card_output_filename = card_output_directory + "/" + index + ".png"

    if not os.path.exists(card_output_directory):
        os.makedirs(card_output_directory)

    background = Image.open(card_template_directory + "/SPLOOT_Card_Grey.png")
    width, height = background.size

    draw_target = ImageDraw.Draw(background)
    draw_target = draw_name(draw_target, metadata["name"], width)

    # handle the text.
    for attribute_data in metadata["attributes"]:

        if attribute_data["trait_type"] == "Personality":
            draw_target = draw_personality(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Vice":
            draw_target = draw_vice(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Phobia":
            draw_target = draw_phobia(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Role":
            draw_target = draw_role(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Class":
            draw_target = draw_class(
                draw_target, attribute_data["value"], width)

    # handle the stats.
    draw_target = draw_stats(draw_target, metadata["attributes"], width)

    # handle the dna band.

    background.save(card_output_filename)

    print("saving: " + card_output_filename)
    print("")


def draw_name(draw_target, name, image_width):

    # first name
    first_name = name.split()[0].upper()
    textwidth, textheight = draw_target.textsize(
        first_name, font=headerStyle)
    x = image_width / 2 - textwidth / 2
    y = 170 + overlayAnchor[1]
    draw_target.text((x, y), first_name,
                     (255, 255, 255), font=headerStyle)

    # last name
    last_name = name.upper().replace(first_name, "", 1)
    textwidth, textheight = draw_target.textsize(
        last_name, font=headerStyle)
    x = image_width / 2 - textwidth / 2
    y = 235 + overlayAnchor[1]
    draw_target.text((x, y), last_name,
                     (255, 255, 255), font=headerStyle)

    return draw_target


def draw_personality(draw_target, personality, image_width):

    draw_string = "PERSONALITY: " + personality

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 330 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_vice(draw_target, vice, image_width):

    draw_string = "VICE: " + vice

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 355 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_phobia(draw_target, phobia, image_width):

    draw_string = "PHOBIA: " + phobia

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 380 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_class(draw_target, player_class, image_width):

    draw_string = player_class.upper()
    textwidth, textheight = draw_target.textsize(
        draw_string, font=labelStyle)

    x = image_width / 2 - textwidth / 2
    y = 65 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=labelStyle)

    return draw_target


def draw_role(draw_target, role, image_width):

    draw_string = role.upper()

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 100 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_stats(draw_target, attributes, image_width):

    stat_count = 0
    col_count = 0
    col_gap = 165
    row_gap = 36
    overall = 0.0
    running_total = 0.0

    for attribute_data in attributes:
        if isinstance(attribute_data["value"], str) == False:

            running_total = running_total + attribute_data["value"]
            overall = overall + attribute_data["value"]

            x = overlayAnchor[0] + (col_count * col_gap) + 210
            y = overlayAnchor[1] + (stat_count % 3 * row_gap) + 600
            draw_target.text((x, y), str(attribute_data["value"]),
                             (255, 255, 255), font=statStyle)

            stat_count = stat_count + 1

            if stat_count % 3 == 0:
                # draw col average.
                x = overlayAnchor[0] + \
                    (col_count * col_gap) + 203
                y = overlayAnchor[1] + (3 * row_gap) + 600
                draw_target.text((x, y), str(round(running_total/3, 1)),
                                 (196, 196, 196), font=statStyle)

                running_total = 0.0
                col_count = col_count + 1

    # overall
    x = 105 + overlayAnchor[0]
    y = 420 + overlayAnchor[1]
    draw_target.text((x, y), str(round(overall/9, 1)),
                     (255, 255, 255), font=ovrStyle)

    return draw_target


def getUserData(questionString):
    # creates boolean value for test that Python major version > 2
    py3 = version_info[0] > 2
    if py3:
        response = input(questionString + ": ")
    else:
        print("NOTE:  Python v3 required.")
        exit()

    return response


def main_menu():
    print("")
    print("========= MAIN MENU ===========")
    print("a) Create All Cards")
    print("-------------------")
    print("q) Quit")
    print("")

    menuSelection = getUserData("Which selection? (a)")

    if menuSelection.lower() == "a":
        create_cards()

    elif menuSelection.lower() == "q":
        print("Quitting.")
        exit()

    else:
        print("")
        # print("Please make a valid selection.")
        # main_menu()

        print("Defaulting to `Create All Cards`.")
        print("")
        create_cards()


if __name__ == "__main__":
    main_menu()
