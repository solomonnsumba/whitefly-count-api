import sys
import cv2 as cv
import requests
import os
import json


# Post image get response
def upload_image(path, url):
	files = {'image': open(path,'rb')}
	response = requests.post(url, files=files)
	output = response.json()
	return output


# draw boxes on image
def draw_annotations(boxes, img, path):
	image_name = os.path.split(path)[1]
	final_path = path.split(".")[0]+"_annotated.jpg"
	for b in boxes:
		cv.rectangle(img, (b[0], b[1]), (b[2], b[3]), (255,0,0), 2) # Define color of bounding box
		cv.imwrite(final_path, img)


# Load image and draw annotations
def annotate_image(boxes, path):
	img = cv.imread(path)
	height = img.shape[0]
	width = img.shape[1]
	fi = draw_annotations(boxes, img, path)


output = json.loads(upload_image(sys.argv[1], sys.argv[2]))

annotate_image(output['Detected_Boxes'], sys.argv[1])



