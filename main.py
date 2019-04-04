import sys
import os

from utils import *

if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = "data/e_shiny_selfies.txt"

if not os.path.isdir("./outputs"):
    os.mkdir("outputs")
OUTPUT_FILE = "outputs/output_" + INPUT_FILE


with open(INPUT_FILE, 'r') as f:
    data = f.read()

data = data.split('\n')[:-1]

n = int(data.pop(0))

print("Parsing data...")
pictures = []
for i, line in enumerate(data):
    if i%10000 == 0:
        print(i)
    split_line = line.split()
    orientation = split_line.pop(0)
    nb_tags = int(split_line.pop(0))
    pictures.append(Photo(i, orientation, split_line))

print("Nb pictures = ", len(pictures))
print("Processing pictures...")
pictures = merge_verticals_dumb(pictures)
print("Processing done")

#slides = brutal_slide(pictures)
slides = segment_bourrin(pictures)
# slides = bourrin_slide(pictures)

# print("Pictures : ", slides)
# print("Pictures sorted by tags :", sort_pic_nb_tags(slides))
# print("Slide score :", compute_slide_vert(slides))


# write_output_vert(OUTPUT_FILE, slides)
