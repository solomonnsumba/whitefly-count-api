# -*- coding: utf-8 -*-


import cv2
import os
import json
from .parameters import par_dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fullpath = os.path.dirname(__file__)
cascade_file = fullpath + '/' + 'cascade/new_cascade.xml'


def rotate_to_landscape(img):
    # Change from portrait to landscape
    rotm = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), 90, 1.0)
    rotated = cv2.warpAffine(img, rotm, (img.shape[1], img.shape[0]))
    return rotated


def resize_images(img_path):
    # Resize image with reso greater than (1024,768) be
    # cause cascade detection will take long and application will freeze
    # also the image will be too big that it wont fit on screen during annotation

    # Resize image because skimage and generally the image processing will
    # take forever with large images
    img_file_name = os.path.basename(img_path)
    img_directory = os.path.dirname(img_path)

    output_dir = os.path.join(img_directory, 'data/')
    # Create results directory if it is non-existent
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    image = cv2.imread(img_path)
    h, w = image.shape[:2]
    if h > w and h > 1000:
        resized_img = cv2.resize(image, (768, 1024))
        image = rotate_to_landscape(image)
    elif w > h and w > 1000:
        resized_img = cv2.resize(image, (1024, 768))
    else:
        resized_img = image

    resized_img_file = os.path.join(output_dir, img_file_name)
    cv2.imwrite(resized_img_file, resized_img)
    return resized_img


'''
    The detect function processes a file to look for matches, and returns a list
    of tuples (x,y) containing the central point of each positive detection.
'''

# Detect matches for  API
def detect_matches_api(imgpath):
    img = resize_images(imgpath.strip('/'))  # cv2.imread(imgpath)
    imgcopy = img.copy()
    cascade = cv2.CascadeClassifier()
    cascade.load(cascade_file)

    scalefactor = 0.6
    if scalefactor != 1:
        width = img.shape[0]
        height = img.shape[1]
        img = cv2.resize(img, (int(height*scalefactor), int(width*scalefactor)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(
        gray, scaleFactor=par_dict['PAR_SCALE_FACTOR'], minNeighbors=par_dict['PAR_MIN_NEIGHBORS'],
        minSize=par_dict['PAR_MIN_SIZE'],  maxSize=par_dict['PAR_MAX_SIZE']
    )

    if len(rects) == 0:
        return [], img

    matches = []
    for r in rects:
        """changed this"""
        matches.append((int((1/scalefactor)*(r[0]+r[2]/2)), int((1/scalefactor)*(r[1]+r[3]/2))))
        # matches.append((int(r[0]+r[2]/2),int(r[1]+r[3]/2)))

    # filtered_matches = removematches.removematches(imagefilename, matches)
    filtered_matches = matches

    mb = convert_circles_rectangle_pts(filtered_matches)

    return mb, imgcopy, imgpath



# Call this function
def detect_matches(imgpath):
    img = resize_images(imgpath.strip('/'))  # cv2.imread(imgpath)
    imgcopy = img.copy()
    cascade = cv2.CascadeClassifier()
    cascade.load(cascade_file)

    scalefactor = 0.6
    if scalefactor != 1:
        width = img.shape[0]
        height = img.shape[1]
        img = cv2.resize(img, (int(height*scalefactor), int(width*scalefactor)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(
        gray, scaleFactor=par_dict['PAR_SCALE_FACTOR'], minNeighbors=par_dict['PAR_MIN_NEIGHBORS'],
        minSize=par_dict['PAR_MIN_SIZE'],  maxSize=par_dict['PAR_MAX_SIZE']
    )

    if len(rects) == 0:
        return [], img

    matches = []
    for r in rects:
        """changed this"""
        matches.append((int((1/scalefactor)*(r[0]+r[2]/2)), int((1/scalefactor)*(r[1]+r[3]/2))))
        # matches.append((int(r[0]+r[2]/2),int(r[1]+r[3]/2)))

    # filtered_matches = removematches.removematches(imagefilename, matches)
    filtered_matches = matches

    mb = convert_circles_rectangle_pts(filtered_matches)

    return mb, imgcopy, imgpath


def convert_circles_rectangle_pts(circlepts):
    rectpts = []
    cf = int(par_dict['PAR_BOX_WIDTH']/2.)
    for cpt in circlepts:
        x, y = cpt
        pt1x, pt1y, pt2x, pt2y = x-cf, y-cf, x+cf, y+cf
        rectpts.append((pt1x, pt1y, pt2x, pt2y))
    return rectpts


def draw_annotations(objects, img, imgpath):
    output_name = os.path.dirname(imgpath) + '/data/' + os.path.basename(imgpath)[:-4]

    if len(objects) > 0:
        for anno in objects:
            pt1 = (anno[0], anno[1])
            pt2 = (anno[2], anno[3])
            cv2.rectangle(img, pt1, pt2, par_dict['PAR_RECTS_COLOR'], 2)

    img_txt_position = (int(img.shape[0]/15), int(img.shape[1]/15))
    cv2.putText(
        img, "Wfly count: %d " % (len(objects)), img_txt_position,
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, par_dict['PAR_TEXT_COLOR'], 2
    )
    cv2.imwrite(output_name + '_detected.jpg', img)
    write_json(output_name, objects)


def redraw_annotations(objects, img, imgpath):
    print(imgpath)
    # output_name = os.path.dirname(imgpath) + '/data/' + os.path.basename(imgpath)[:-4]
    output_name = os.path.join(
        BASE_DIR, os.path.split(imgpath)[0].strip('/'),
        'data/results/'+os.path.basename(imgpath)[:-4]
                               )

    if len(objects) > 0:
        for anno in objects:
            pt1 = (anno[0], anno[1])
            pt2 = (anno[2], anno[3])
            cv2.rectangle(img, pt1, pt2, par_dict['PAR_RECTS_COLOR'], 2)

    img_txt_position = (int(img.shape[0]/15), int(img.shape[1]/15))
    cv2.putText(
        img, "Wfly count: %d " % (len(objects)), img_txt_position,
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, par_dict['PAR_TEXT_COLOR'], 2
    )
    cv2.imwrite(output_name + '_detected.jpg', img)
    print(BASE_DIR)
    print(os.path.join(BASE_DIR, output_name))

    write_json(output_name, objects)
    # write_json(os.path.join(BASE_DIR, output_name).strip('/'), objects)
    return (cv2.cvtColor(img, cv2.COLOR_RGB2BGR)), output_name + '_detected.jpg'


def write_json(fname, objects):
    # Write objects to json file

    d = [{'filename': fname, 'objects': objects}]
    with open(fname + '.json', 'w') as outfile:
        json.dump(d, outfile, sort_keys=True)
