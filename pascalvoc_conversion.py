# dependencies
import os
from sklearn.model_selection import train_test_split
import cv2
import xml.etree.ElementTree as ET
import shutil

# dataset directory. Change with your own path->change
DATASET_DIR = "D:\\projects\\object_detection_test\\dataset\\test_dataset\\Annotations"

# list of all XML annotations
annotations = [filename for filename in os.listdir(DATASET_DIR) if filename.endswith(".xml")]
print(annotations)
# split into train and test
train_annotations, test_annotations = train_test_split(annotations, test_size=0.25)
# further split test into test and validation
test_annotations, val_annotations = train_test_split(test_annotations, test_size=0.5)

# View data in all splits
print("Training:", len(train_annotations), "Validation:", len(val_annotations),  "Test:", len(test_annotations))

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
        if class_name[i] not in classes: continue    
        # convert bbox coordinates to yolo format
        center_x = (xmin[i] + (xmax[i] - xmin[i]) / 2) / image_width # Get center (X) of bounding box and normalize
        center_y = (ymin[i] + (ymax[i] - ymin[i]) / 2) / image_height # Get center (X) of bounding box and normalize
        width = (xmax[i] - xmin[i]) / image_width # Get width of bbox and normalize
        height = (ymax[i] - ymin[i]) / image_height # Get height of bbox and normalize
        # write to file
        file.write(f"{classes[str(class_name[i])]} {center_x} {center_y} {width} {height}\n")
    # close file
    file.close()

def process_list(xmls, destination_dir, split_type):
    # open/create images txt file
    destination_dir_file = open(f"{destination_dir}/{split_type}.txt", "w")
    # destination directory for images and txt annotation
    destination_dir = f"{destination_dir}{split_type}"
    os.makedirs(f"{destination_dir}", exist_ok=True) # create path if not exists
    for xml_filename in xmls: # iterate over each xml
        # convert to txt using function and store in given path
        txt_name = xml_filename.replace('.xml', '.txt')
        xml_to_txt(f"{DATASET_DIR}/{xml_filename}", f"{destination_dir}/{txt_name}")
        
        # copy image to destination path
        image_name = xml_filename.replace('.xml', '.jpg')
        shutil.copy(f"{DATASET_DIR}/{image_name}", f"{destination_dir}/{image_name}")
        # add image path to txt file
        destination_dir_file.write(f"{destination_dir}/{image_name}\n")
    # close file
    destination_dir_file.close()
# calling function and store yolo format -> change
processed_path =  "D:\\projects\\object_detection_test\\dataset\\test_dataset_processed"
process_list(train_annotations, processed_path , "\\train")
process_list(test_annotations, processed_path , "\\test")
process_list(val_annotations, processed_path , "\\val")