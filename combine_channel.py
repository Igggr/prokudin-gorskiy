from skimage.io import imread, imshow, imsave
from skimage import img_as_float
import numpy as np
 
def read_and_split(image):
    """ read image, and split it into three parts """
    img = imread(img)
    height_div_3 = img.shape[0] // 3
    b = img[ : height_div_3 , : ]
    g = img[height_div_3 : 2 * height_div_3, : ]    
    r = img[2 * height_div_3 : 3 * height_div_3, : ]
    b, g, r = list(map(img_as_float, (b, g, r, )))
    return b, g, r
 
def clip_border(b, g, r, obresat = 20):
    """ get rid of border """
    height, width = b.shape
    centre_part = lambda x: x[height//obresat : -height//obresat , width//obresat : -width//obresat]  
    b = centre_part(b)
    g = centre_part(g)
    r = centre_part(r)
    return b, g, r
 
def find_shift(canal_1, canal_2, axis, max_shift = 15):
    """ move channel_2 relativly to channel_1 and 
    find what shift provide a best correlation between them"""
    min_corelation = 0
    right_shift = 0
    for shift in range(-max_shift, max_shift + 1):
        canal_2_shift = np.roll(canal_2, shift, axis)
        current_corelation = (canal_1 * canal_2_shift).sum()
        if current_corelation >= min_corelation:
            min_corelation = current_corelation
            right_shift = shift
    return right_shift
   
def find_all_shifts(b, g, r):
    """ find shifts for red and blue channel relativle to the green channel
    on the axis x and y"""
    gr_x = find_shift(g, r, 0)
    gr_y = find_shift(g, r, 1)
    gb_x = find_shift(g, b, 0)
    gb_y = find_shift(g, b, 1)
    return  gb_x, gb_y, gr_x, gr_y
     
def combine_image(b, g, r, gr_x, gr_y, gb_x, gb_y):
    """ shift red and blue channel on that ammount, that they will better correspond with green channel- 
    and then combine all three channel into one colorfull image""""
    r_sh = np.roll(r, gr_x, axis = 0)
    r_sh = np.roll(r_sh, gr_y, axis = 1)
    b_sh = np.roll(b, gb_x, axis = 0)
    b_sh = np.roll(b_sh, gb_y, axis = 1)
    combined_img =  np.stack((r_sh, g, b_sh), 2)
    return combined_img
    
def result_img(image):
    """all previous steps combined together"""
    b, g, r = read_and_split(image)
    b, g, r = clip_border(b, g, r, 5)
    gb_x, gb_y, gr_x, gr_y = find__all_shifts(b, g, r)
    result_img = combine_image(b, g, r, gr_x, gr_y, gb_x, gb_y)
    return result_img
