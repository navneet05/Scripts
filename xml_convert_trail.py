# dependencies
import os
from sklearn.model_selection import train_test_split
import cv2
import xml.etree.ElementTree as ET
import shutil

# dataset directory. Change with your own path->ch
# classes we want to use->change
classes = {'0' : '0',  '1': '1'}

def xml_to_txt(path, dest):
    # read xml file using xml.etree
    tree = ET.parse(path) 
    root = tree.getroot()
    
    # output labels txt file
    file = open(dest, "w")
    # iterate over each annotation in file
    class_name=[]
    xmin = [] 
    ymin = []
    xmax = []
    ymax = []
    for member in root.findall('object'):
        class_name.append(member[0].text)
        image_width=int(root.find('size')[0].text)
        image_height=int(root.find('size')[1].text)
        xmin.append((member[4][0].text))
        ymin.append((member[4][1].text))
        xmax.append((member[4][2].text))
        ymax.append((member[4][3].text))
    print(class_name)
    #print(ymax)
    xmin=[float(i) for i in xmin]
    ymin=[float(i) for i in ymin]
    xmax=[float(i) for i in xmax]
    ymax=[float(i) for i in ymax]
    for i in range(len(xmin)):
        print('in loop')
        if class_name[i] not in classes: continue    
        # convert bbox coordinates to yolo format
        center_x = (xmin[i] + (xmax[i] - xmin[i]) / 2) / image_width # Get center (X) of bounding box and normalize
        center_y = (ymin[i] + (ymax[i] - ymin[i]) / 2) / image_height # Get center (X) of bounding box and normalize
        width = (xmax[i] - xmin[i]) / image_width # Get width of bbox and normalize
        height = (ymax[i] - ymin[i]) / image_height # Get height of bbox and normalize
        # write to file
        print('print')
        print(f"{classes[str(class_name[i])]} {center_x} {center_y} {width} {height}\n")
    # close file
    file.close()




xml_to_txt("dataset\\test_dataset\\Annotations\\240.xml", "demo.txt")
'''tree = ET.parse("240.xml") 
root = tree.getroot()
print(root)
print(root.tag)
print('child')
for child in root:
    print(child.tag, child.attrib)
print('-------------------------------------------------')
class_name=[]
xmin = [] 
ymin = []
xmax = []
ymax = []
for member in root.findall('object'):
    class_name.append(member[0].text)
    image_width=int(root.find('size')[0].text)
    image_height=int(root.find('size')[1].text)
    xmin.append((member[4][0].text))
    ymin.append((member[4][1].text))
    xmax.append((member[4][2].text))
    ymax.append((member[4][3].text))
print(class_name)
print(ymax)'''