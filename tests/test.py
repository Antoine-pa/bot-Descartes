from PIL import Image, ImageDraw, ImageFont
colors = [(241, 196, 15, 255), (243, 156, 18, 255), 
    (230, 126, 34, 255), (211, 84, 0, 255), (192, 57, 43, 255), (231, 76, 60, 255), (155, 89, 182, 255), (142, 68, 173, 255),
    (41, 128, 185, 255), (52, 152, 219, 255), (26, 188, 156, 255), (22, 160, 133, 255),
    (39, 174, 96, 255), (46, 204, 113, 255)]

i = 0
for col in colors:
    font = ImageFont.truetype("font_discord_bold.ttf", 65)
    im = Image.new('RGBA', (70, 70), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((0, 0, 70, 70),radius=10, fill = col)
    draw.text((35, 35), text=str(i), font = font, fill = (0, 0, 0, 255), anchor="mm")
    im.save(f"number_{i}.png")
    i+=1
"""
i = 0
for col in colors:
    im = Image.new('RGBA', (70, 70), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.pieslice((10, 10, 60, 60), start=0, end=360, fill=col)
    im.save(f"circle_{i}.png")
    i+=1
"""