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



class Photo:

    def merge(pic1, pic2):
        merge_tags = list(set(pic1.tags).union(pic2.tags))
        return Photo(pic1.id, 'M', merge_tags)

    def __init__(self, id, orientation, tags):
        self.orientation = orientation
        self.id = int(id)
        self.nb_tags = len(tags)
        self.tags = tags

    def __repr__(self):
        return f"Picture {self.id} : {self.orientation}, {self.nb_tags} -> {'/'.join(self.tags)}"


def write_output(slides):
    n = len(slides)
    s = str(n) + '\n'
    i = 0
    while i < n:
        s += str(slides[i].id)
        if i < n - 1 and slides[i].orientation == 'V':
            s += ' ' + str(slides[i+1].id)
            i += 1
        s += '\n'
        i += 1
    with open(OUTPUT_FILE, 'w') as f:
        f.write(s)

def sort_pic_nb_tags(pics):
    return sorted(pics, key=lambda x: x.nb_tags, reverse=True)

def compute_transition(pic1, pic2):
    only1, common = [], []
    idx = [False] * len(pic2.tags)
    for tag in pic1.tags:
        if tag in pic2.tags:
            common.append(tag)
            idx[pic2.tags.index(tag)] = True
        else:
            only1.append(tag)
    only2 = [pic2.tags[i] for i in range(len(pic2.tags)) if not idx[i]]
    return min(len(only1), len(common), len(only2))


def compute_slide(slide):
    score = 0
    n, i = len(slide), 0
    while i < n-1:
        if i < n-2 and slide[i+1].orientation == 'V':
            score += compute_transition(slide[i], Photo.merge(slide[i+1], slide[i+2]))
            i += 1
        else:
            score += compute_transition(slide[i], slide[i+1])
        i += 1
    return score


def get_tags_dict(pictures):
    tag_dict = {}
    for pic in pictures:
        for tag in pic.tags:
            if (not tag in tag_dict):
                    tag_dict[tag] = 1
            else:
                    tag_dict[tag] += 1
    return sorted(tag_dict)


n = int(data.pop(0))

pictures = []
for i, line in enumerate(data):
    split_line = line.split()
    orientation = split_line.pop(0)
    nb_tags = int(split_line.pop(0))
    pictures.append(Photo(i, orientation, split_line))

# print("Pictures : ", pictures)
# print("Pictures sorted by tags :", sort_pic_nb_tags(pictures))
# print("Slide score :", compute_slide(pictures))


def find_pic_with_tag(tag, pictures):
    pic_list = []
    for pic in pictures:
            if tag in pic.tags:
                    pic_list.append(pic)
    return pic_list


# slides = pictures.copy()
# write_output(slides)
