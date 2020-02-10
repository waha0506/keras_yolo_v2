import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse
from itertools import permutations
from lxml import etree as ET

ap=argparse.ArgumentParser()
ap.add_argument('-i', '--image', type=str)
args=vars(ap.parse_args())

image = cv2.imread(args['image'])
source = image.copy()
target = image.copy()
phone=source[101:286,209:394]
music=source[101:286,479:664]
maps=source[101:286,749:934]
messages=source[101:286,1019:1204]
playing=source[419:604,209:394]
podcasts=source[419:604,479:664]
audiobook=source[419:604,749:934]
audiotest=source[419:604,1019:1204]

icons_coordinate = {
0:[101,286,209,394],
1:[101,286,479,664],
2:[101,286,749,934],
3:[101,286,1019,1204],
4:[419,604,209,394],
5:[419,604,479,664],
6:[419,604,749,934],
7:[419,604,1019,1204]
}

icons = [phone, music, maps, messages, playing, podcasts, audiobook, audiotest]

icon_name = ["phone", "music", "maps", "messages", "playing", "podcasts", "audiobook", "audiotest"]

index = [0, 1, 2, 3, 4, 5, 6, 7]

index_set = []

def write_xml_file(index):
    root = ET.Element('annotation')
    folder = ET.SubElement(root, 'folder')
    folder.text='images'
    filename = ET.SubElement(root, 'filename')
    file_name = str(i)+'.jpg'
    filename.text = file_name
    path = ET.SubElement(root, 'path')
    path.text='/home/xueguang/images/'+str(i)+'.jpg'
    source = ET.SubElement(root, 'source')
    database = ET.SubElement(source, 'database')
    database.text='Unknown'
    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text='1280'
    height = ET.SubElement(size, 'height')
    height.text='768'
    depth = ET.SubElement(size, 'depth')
    depth.text='3'
    segmented = ET.SubElement(root, 'segmented')
    segmented.text='0'
    
    j = 0
    for j in range(8):
        write_object(index_set[index][j], root, j)

    tree = ET.ElementTree(root)
    filename = './annotations/'+str(i)+'.xml'
    tree.write(filename, pretty_print=True, xml_declaration=True,   encoding="utf-8")

def write_object(index_set_name, root_name, index):
    object_name = ET.SubElement(root_name, 'object')
    name = ET.SubElement(object_name, 'name')
    name.text = icon_name[index_set_name]
    pose = ET.SubElement(object_name, 'pose')
    pose.text = "Unspecified"
    truncated = ET.SubElement(object_name, 'truncated')
    truncated.text = "0"
    difficult = ET.SubElement(object_name, 'difficult')
    difficult.text = "0"
    bndbox = ET.SubElement(object_name, 'bndbox')
    xmin = ET.SubElement(bndbox, 'xmin')
    xmin_value = icons_coordinate[index][2]
    xmin.text = str(xmin_value)
    ymin = ET.SubElement(bndbox, 'ymin')
    ymin_value = icons_coordinate[index][0]
    ymin.text = str(ymin_value)
    xmax = ET.SubElement(bndbox, 'xmax')
    xmax_value = icons_coordinate[index][3]
    xmax.text = str(xmax_value)
    ymax = ET.SubElement(bndbox, 'ymax')
    ymax_value = icons_coordinate[index][1]
    ymax.text = str(ymax_value)

for p in permutations(index):
    index_set.append(p) 

#print(index_set)
#print(len(index_set))

#for i in range(len(index_set)):
#    print(index_set[i][0])

for i in range(len(index_set)):
    target[101:286,209:394]=icons[index_set[i][0]]
    target[101:286,479:664]=icons[index_set[i][1]]
    target[101:286,749:934]=icons[index_set[i][2]]
    target[101:286,1019:1204]=icons[index_set[i][3]]
    target[419:604,209:394]=icons[index_set[i][4]]
    target[419:604,479:664]=icons[index_set[i][5]]
    target[419:604,749:934]=icons[index_set[i][6]]
    target[419:604,1019:1204]=icons[index_set[i][7]]

    filename='./images/'+str(i)+'.jpg'
    cv2.imwrite(filename, target)
    write_xml_file(i)


