import sys
import os

class Photo:

    def merge(pic1, pic2):
        merge_tags = list(set(pic1.tags).union(pic2.tags))
        return Photo(pic1.id, 'M', merge_tags)

    def __init__(self, id, orientation, tags):
        self.orientation = orientation
        self.id = int(id)
        self.nb_tags = len(tags)
        self.tags = tags

    def common_tags(self, other):
        return len(list(set(self.tags).intersection(other.tags)))

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"Picture {self.id} : {self.orientation}, {self.nb_tags} -> {'/'.join(self.tags)}"


class MergedPhoto(Photo):

    def merge(pic1, pic2):
        return list(set(pic1.tags).union(pic2.tags))

    def __init__(self, pic1, pic2):
        self.id1 = pic1.id
        self.id2 = pic2.id
        self.tags = MergedPhoto.merge(pic1, pic2)
        self.nb_tags = len(self.tags)

    def get_id(self):
        return str(self.id1) + ' ' + str(self.id2)

    def __repr__(self):
        return f"Picture {self.id1}, {self.id2} : VV, {self.nb_tags} -> {'/'.join(self.tags)}"


def write_output(output_file, slides):
    n = len(slides)

    s = '\n'
    i = 0
    while i < n:
        if i < n-1 and slides[i].orientation == 'V' and slides[i+1].orientation != 'V':
            i += 1
            continue

        s += str(slides[i].id)
        if i < n-1 and slides[i].orientation == 'V':
            assert slides[i+1].orientation == 'V'
            s += ' ' + str(slides[i+1].id)
            i += 1
        s += '\n'
        i += 1
    with open(output_file, 'w') as f:

        f.write(str(s.count('\n') - 1) + s)

def write_output_vert(output_file, slides):
    n = len(slides)
    s = '\n'
    i = 0
    while i < n:
        s += slides[i].get_id() + '\n'
        i += 1
    with open(output_file, 'w') as f:
        f.write(str(s.count('\n') - 1) + s)


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


def compute_slide_vert(slide):
    score = 0
    n, i = len(slide), 0
    i = 0
    while i < len(slide)-1:
        score += compute_transition(slide[i], slide[i+1])
        i += 1
    return score


def compute_slide(slide):
    score = 0
    n, i = len(slide), 0
    merged_slide = []
    i = 0
    while i < n:
        if i < n-1 and slide[i].orientation == 'V':
            merged_slide.append(Photo.merge(slide[i], slide[i+1]))
            i += 1
        else:
            merged_slide.append(slide[i])
        i += 1
    i = 0
    while i < len(merged_slide)-1:
        score += compute_transition(merged_slide[i], merged_slide[i+1])
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

def find_pic_with_tag(tag, pictures):
    pic_list = []
    for pic in pictures:
        if tag in pic.tags:
            pic_list.append(pic)
    return pic_list

def get_most_different(pictures, picture):
    v_pics = []
    for pic in pictures:
        if pic.orientation == 'V' and pic != picture:
            v_pics.append(pic)

    return min(v_pics, key=lambda pic:picture.common_tags(pic))

def get_most_different_vert(pictures, picture):
    return min(range(len(pictures)), key=lambda i:picture.common_tags(pictures[i]))

def merge_verticals(pictures):
    horizon_pics, vertical_pics = [], []
    for pic in pictures:
        if pic.orientation == 'V':
            vertical_pics.append(pic)
        else:
            horizon_pics.append(pic)
    merged_pics = []
    while len(vertical_pics) > 1:
        pic = vertical_pics.pop(0)
        i_diff = get_most_different_vert(vertical_pics, pic)
        merged_pics.append(MergedPhoto(pic, vertical_pics[i_diff]))
        vertical_pics.pop(i_diff)

    return horizon_pics + merged_pics


def merge_verticals_dumb(pictures):
    horizon_pics, vertical_pics = [], []
    for pic in pictures:
        if pic.orientation == 'V':
            vertical_pics.append(pic)
        else:
            horizon_pics.append(pic)
    merged_pics = []
    while len(vertical_pics) > 1:
        pic = vertical_pics.pop(0)
        diff = vertical_pics.pop(0)
        # i_diff = get_most_different_vert(vertical_pics, pic)
        merged_pics.append(MergedPhoto(pic, diff))
        # vertical_pics.pop(i_diff)
        len(vertical_pics)

    return horizon_pics + merged_pics

def brutal_slide(pictures):
    slides = []
    pictures_copy = pictures.copy()
    sorted_tag = get_tags_dict(pictures)
    temp_pic = 0
    for tag in sorted_tag:
        print(len(pictures_copy))
        pic_with_tag = find_pic_with_tag(tag, pictures_copy)
        for p in pic_with_tag:
            if p.orientation == "H":
                slides.append(p)
                pictures_copy.remove(p)
            else:
                try:
                    temp_p = get_most_different(pictures_copy, p)
                    slides.append(temp_p)
                    slides.append(p)
                    pictures_copy.remove(p)
                    pictures_copy.remove(temp_p)
                except:
                    a = 0
    return slides

def bourrin_slide(pictures):
    print("Sorting pictures...")
    sorted_pics = sort_pic_nb_tags(pictures)
    # sorted_pics = pictures.copy()
    slides = []
    slides.append(sorted_pics.pop(0))

    print("Creating Slides...")
    while len(sorted_pics) > 0 :
        pic = slides[-1]
        if len(slides) % 2000 == 0 : print("Done ", round(len(slides)/len(pictures)*100,2))

        best_score = -1
        best_pic = pic
        id_best_pic = -1
        for i in range(min(len(sorted_pics), 1000)) :
            other_pic = sorted_pics[i]
            score = compute_transition(pic, other_pic)
            if score > best_score :
                best_score = score
                best_pic = other_pic
                id_best_pic = i
            if best_score >= int(pic.nb_tags / 2) : break
        slides.append(sorted_pics.pop(id_best_pic))

    print("Computing Score...")
    print("SCORE = ", compute_slide_vert(slides))

    return slides

import threading

class Test:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.res = [[] for i in range(1000)]

    def run(self, i, pictures):
        l = pictures[(i*10000):min((i+1)*10000, len(pictures))]
        self.res[i] = bourrin_slide(l)


def segment_bourrin(pictures):
    slides = []
    index = 0
    test = Test()
    threads = []
    for index in range(len(pictures)//10000):
        threads.append(threading.Thread(target=lambda: test.run(index, pictures)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return test
