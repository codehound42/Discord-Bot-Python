import os
from typing import List
from discord.ext import commands
from difflib import get_close_matches
from PIL import Image, ImageFont, ImageDraw
import textwrap
import math


class MemeGenerator:
    memes_folder_path = "./assets/memes/"
    DEBUG = False
    line_spacing = 5
    font_type = "./assets/fonts/impact.ttf"
    meme_draft_name = "meme_edited"


    def get_all_meme_names(self) -> List[str]:
        meme_file_names = os.listdir(self.memes_folder_path)
        memes = [meme_name.split('.', 1)[0] for meme_name in meme_file_names]

        # Exclude image file used for editing
        if self.meme_draft_name in memes:
            memes.remove(self.meme_draft_name)

        return memes


    def get_closest_matching_meme_filename(self, meme_name):
        closest_matching_element_list = get_close_matches(meme_name, self.get_all_meme_names(), n=1, cutoff=0.3)
        if not closest_matching_element_list:
            raise commands.BadArgument("Meme not recognised. Try with another one.")
        return closest_matching_element_list[0]


    def draw_text_border(self, draw, x, y, line, font, font_size):
        SHADOWCOLOR = "black"
        BORDER_THICKNESS = math.ceil(0.03*font_size)

        draw.text((x-BORDER_THICKNESS, y-BORDER_THICKNESS), line, font=font, fill=SHADOWCOLOR)
        draw.text((x+BORDER_THICKNESS, y-BORDER_THICKNESS), line, font=font, fill=SHADOWCOLOR)
        draw.text((x-BORDER_THICKNESS, y+BORDER_THICKNESS), line, font=font, fill=SHADOWCOLOR)
        draw.text((x+BORDER_THICKNESS, y+BORDER_THICKNESS), line, font=font, fill=SHADOWCOLOR)


    def compute_initial_y_pos(self, total_text_height, top=True):
        if top:
            return self.margin
        return self.H - self.margin - total_text_height


    def compute_draw_info(self, draw, text, font_size):
        TOTAL_TEXT_HEIGHT_MIN = 8
        TOTAL_TEXT_HEIGHT_MAX = int(0.25*self.H)

        # Load font
        font = ImageFont.truetype(self.font_type, font_size)

        # Compute draw info
        text_width_pixels, text_height_pixels = font.getsize(text)
        char_width_pixels = max(text_width_pixels // max(len(text), 1), 1)
        max_width_pixels = self.W - self.margin*2
        max_width_chars = max_width_pixels // char_width_pixels
        lines = textwrap.wrap(text, width=max_width_chars)
        number_of_lines = len(lines)
        total_text_height = number_of_lines * (text_height_pixels + self.line_spacing) - self.line_spacing

        # Recurse if text too large or too small
        if total_text_height > TOTAL_TEXT_HEIGHT_MAX and not total_text_height < TOTAL_TEXT_HEIGHT_MIN:
            new_font_size = int(0.9*font_size)-1
            return self.compute_draw_info(draw, text, new_font_size)

        # Return draw info once font size approved
        return font, font_size, lines, total_text_height


    def draw_text(self, draw, text, top=True):
        TEXT_COLOR = "white"
        DEFAULT_FONT_SIZE_TOP = 300
        DEFAULT_FONT_SIZE_BOTTOM = 300
        default_font_size = DEFAULT_FONT_SIZE_TOP if top else DEFAULT_FONT_SIZE_BOTTOM
        
        font, font_size, lines, total_text_height = self.compute_draw_info(draw, text, default_font_size)

        # Identify text y position based on draw info and number of lines
        y = self.compute_initial_y_pos(total_text_height, top)
        for line in lines:
            w, h = draw.textsize(line, font=font)
            x = (self.W - w) // 2
            
            # Make adjustment to take care of intrinsic font offset c.f. approach @ https://github.com/python-pillow/Pillow/issues/2486
            xOffset, yOffset = font.getoffset(line)
            x -= xOffset
            y -= yOffset
            self.draw_text_border(draw, x, y, line, font, font_size)
            draw.text((x, y), line, font=font, fill=TEXT_COLOR)
            
            y += h + self.line_spacing


    def generate_meme(self, meme_name, top_text, bottom_text):
        meme_filename = self.get_closest_matching_meme_filename(meme_name)
        meme_path = self.memes_folder_path + meme_filename + ".jpg"

        # Open image
        img = Image.open(meme_path)
        self.W, self.H = img.size
        self.margin = math.ceil(0.025*self.H)

        # Draw on image
        draw = ImageDraw.Draw(img)
        self.draw_text(draw, top_text, top=True)
        self.draw_text(draw, bottom_text, top=False)

        # Save draft image
        img.save(self.memes_folder_path + self.meme_draft_name + ".jpg")