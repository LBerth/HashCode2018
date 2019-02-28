import sys
import os

if len(sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = "a_example.txt"

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

slides = pictures.copy()
write_output(slides)
