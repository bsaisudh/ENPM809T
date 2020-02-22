import cv2
import numpy as np


def detect_arrow_1(frame):
    """
    Arrow detection using Corners and further detects its orientation
    @author: Rama Prashanth
    """
    image = frame.copy()
    orientation = ''
    
    # Covert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green Color HSV Range
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([90, 255, 255])

    # Thresolding HSV range to get only green mask
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    masked_image =  cv2.bitwise_and(image, image, mask=mask_green)
    mask_hsv_comparision = np.hstack((image, hsv, masked_image))

    # Morphological Operation - Opening
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    # Apply Gaussian Blur to remove noise
    blur_img = cv2.GaussianBlur(mask_green, (5,5), 1)
    blur_img_comparision = np.hstack((mask_green, blur_img))

    # Shi-Tomasi Corner Detection
    corners = cv2.goodFeaturesToTrack(blur_img, 100, 0.1, 5)
    corners = np.int0(corners)
    
    points_x = []
    points_y = []
    
    for corner in corners:
        x,y = corner.ravel()
        points_x.append(x)
        points_y.append(y)
        cv2.circle(image, (x,y), 3, (255, 0, 0), -1)
    
    arrow_mid_x = int((max(points_x) + min(points_x))/2)
    arrow_dist_x = max(points_x) - min(points_x)
    
    arrow_mid_y = int((max(points_y) + min(points_y))/2)
    arrow_dist_y = max(points_y) - min(points_y)
    
    if arrow_dist_x > arrow_dist_y:
        west_corners = 0
        east_corners = 0
        
        for corner in corners:
            x, y = corner.ravel()
            if x < int(arrow_mid_x):
                west_corners += 1
            else:
                east_corners += 1

        if west_corners > east_corners:
            orientation = 'West'
        else:
            orientation = 'East'
    else:
        north_corners = 0
        south_corners = 0
        
        for corner in corners:
            x, y = corner.ravel()
            if y < int(arrow_mid_y):
                north_corners += 1
            else:
                south_corners += 1

        if north_corners > south_corners:
            orientation = 'North'
        else:
            orientation = 'South'
    
    return image, orientation, mask_hsv_comparision, blur_img_comparision


if __name__ == '__main__':
    
    test_images = ['test_east.jpg',
                   'test_west.jpg',
                   'test_north.jpg',
                   'test_south.jpg']
    
    for path in test_images:
        img = cv2.imread(path)
        
        arrow_img, orientation, mask, blur = detect_arrow_1(img)
    
        cv2.putText(arrow_img, orientation, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), lineType=cv2.LINE_AA)
        cv2.imshow("Arrow Detected", arrow_img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    