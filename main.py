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
    if i%1000 == 0:
        print(i)
    split_line = line.split()
    orientation = split_line.pop(0)
    nb_tags = int(split_line.pop(0))
    pictures.append(Photo(i, orientation, split_line))

#slides = pictures.copy()

slides = brutal_slide(pictures)
slides_bourrin = bourrin_slide(pictures)

print("Pictures : ", slides)
print("Pictures sorted by tags :", sort_pic_nb_tags(slides))
print("Slide score :", compute_slide(slides))


write_output(OUTPUT_FILE, slides)
