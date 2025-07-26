from moviepy.editor import TextClip

with open('static/fonts.txt', 'w', encoding='utf-8') as fonts:
    fonts.write("\n".join(TextClip.list('font')))

with open('static/colors.txt', 'w', encoding='utf-8') as colors:
    colors_list = [color.decode("utf-8") for color in TextClip.list('color')[3:]]
    colors.write("\n".join(colors_list))