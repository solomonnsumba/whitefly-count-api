"""
Parameters controlling the detection of whiteflies

ver. 20170215
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

defaults_dict = dict(
    PAR_RESULTS_DIR=os.path.join(BASE_DIR, 'media/uploads/data'),  # PAR_RESULTS_DIR = './data/',
    PAR_IMG_SOURCE_DIR='./test_source/',
    PAR_MIN_NEIGHBORS=3,
    PAR_MIN_SIZE=(10, 10),
    PAR_MAX_SIZE=(15, 15),
    PAR_SCALE_FACTOR=1.03,
    PAR_TEXT_COLOR=(255, 255, 255),
    PAR_RECTS_COLOR=(0, 0, 255),
    PAR_BOX_WIDTH=15)
        
par_dict = defaults_dict.copy()
