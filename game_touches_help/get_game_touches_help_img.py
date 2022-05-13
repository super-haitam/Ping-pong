from PIL import Image, ImageFont, ImageDraw
import pygame
import os

cwd = os.getcwd()
os.chdir(os.getcwd() + "\\game_touches_help\\images")
control_images = {}
current_file_name = os.path.basename(__file__)
for img in os.listdir():
    if img != current_file_name:
        control_images[img] = Image.open(img)
os.chdir(cwd)


class CreateImage:
    def __init__(self, bg_color: tuple, keys_dict: dict):
        """
            Parameters
                :bg_color
                    The background color of the image
                :keys_dict
                    A dictionary containing {Brief_description: Key/Keys[]}; Both are strings
        """
        if len(keys_dict) != 1:
            raise "keys_dict lenght Must Not exceed one!"

        self.bg_color = bg_color
        self.keys_dict = keys_dict
        self.size = self.get_size()

        self.write(list(keys_dict.keys())[0])
        self.paste_key_images()

    def write(self, text, font_size=35):
        font = ImageFont.truetype("game_touches_help/COMIC.TTF", font_size)

        image = Image.new("RGB", self.size, color=self.bg_color)

        image_editable = ImageDraw.Draw(image)
        w, self.text_height = image_editable.textsize(text, font=font)
        image_editable.text(((self.size[0] - w) / 2, 0), text, (0, 0, 0), font=font)

        self.size = self.size[0], self.size[1] + self.text_height

        self.image = Image.new("RGB", self.size, color=self.bg_color)
        image_editable = ImageDraw.Draw(self.image)
        image_editable.text(((self.size[0] - w) / 2, 0), text, (0, 0, 0), font=font)

    def get_image(self, key):
        d = {"space": "space.png",
             "up": "UP.png",
             "down": "DOWN.png"}

        for ltr in "abcdefghijklmnopqrstuvwxyz":
            d[ltr] = ltr.upper() + ".png"
        return control_images[d[key]]

    def get_size(self):
        if isinstance(self.keys_dict[list(self.keys_dict.keys())[0]], list):
            l = self.keys_dict[list(self.keys_dict.keys())[0]]
            return sum([self.get_image(l[l.index(i)]).size[0] for i in l]), \
                   max([self.get_image(l[l.index(i)]).size[1] for i in l])
        else:
            # The longest keyboard key image among keys_dict
            # Sum of all the keys' heights
            return self.get_image(self.keys_dict[list(self.keys_dict.keys())[0]]).size[0], \
                   self.get_image(self.keys_dict[list(self.keys_dict.keys())[0]]).size[1]

    def paste_key_images(self):
        if isinstance(self.keys_dict[list(self.keys_dict.keys())[0]], list):
            l = self.keys_dict[list(self.keys_dict.keys())[0]]
            for num, key in enumerate(l):
                key_image = self.get_image(key)
                self.image.paste(key_image, (sum([self.get_image(i).size[0] for i in l[:num]]), self.text_height),
                                 key_image)
        else:
            for num, f in enumerate(self.keys_dict):
                key = self.keys_dict[f]
                key_image = self.get_image(key)
                self.image.paste(key_image, ((self.size[0] - key_image.size[0]) // 2, self.text_height), key_image)


def get_pygame_img(img):
    """
    Will convert a PIL.Image to pygame image of type pygame.Surface
    """
    return pygame.image.fromstring(img.image.tobytes(), img.image.size, img.image.mode)
