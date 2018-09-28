from PIL import Image, ImageDraw, ImageFont
import os, uuid, random

fnt = ImageFont.truetype('res/ssp.ttf', 50)

def generate(gids):
  im = Image.open("res/ghosting.png")
  im = im.convert("RGB")
  draw = ImageDraw.Draw(im)

  draw.text((840,510), gids[0], font=fnt, fill=(0,0,0,255))
  draw.text((840,950), gids[1], font=fnt, fill=(0,0,0,255))

  filename = "res/" + str(uuid.uuid1()) + ".pdf"

  im.save(filename, "PDF", resolution=100.0)

  return filename
