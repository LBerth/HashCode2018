import sys
import os

from utils import *

if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = "c_memorable_moments.txt"

if not os.path.isdir("./outputs"):
    os.mkdir("outputs")
OUTPUT_FILE = "outputs/output_" + INPUT_FILE


with open(INPUT_FILE, 'r') as f:
    data = f.read()

data = data.split('\n')[:-1]

n = int(data.pop(0))

pictures = []
for i, line in enumerate(data):
    split_line = line.split()
    orientation = split_line.pop(0)
    nb_tags = int(split_line.pop(0))
    pictures.append(Photo(i, orientation, split_line))

print("Pictures : ", pictures)
print("Pictures sorted by tags :", sort_pic_nb_tags(pictures))
print("Slide score :", compute_slide(pictures))

#slides = pictures.copy()

def brutal_slide(pictures):
    slides = []
    pictures_copy = pictures.copy()
    sorted_tag = get_tags_dict(pictures)
    temp_pic = 0
    for tag in sorted_tag:
        pic_with_tag = find_pic_with_tag(tag, pictures_copy)
        for p in pic_with_tag:
            if p.orientation == "H":
                slides.append(p)
                pictures_copy.remove(p)
            else:
                if temp_pic != 0:
                    slides.append(temp_pic)
                    slides.append(p)
                    temp_pic = 0
                    pictures_copy.remove(p)
                else:
                    temp_pic = p
                    pictures_copy.remove(p)
    return slides
brutal_slide(pictures)
                

write_output(OUTPUT_FILE, slides)
