import os, sys

# This try-catch is a workaround for Python3 when used with ROS; it is not needed for most platforms
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass

import cv2
import numpy as np


def detect_arrow(frame):
    """
    Arrow detection using Corners and further detects its orientation
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
    masked_img =  cv2.bitwise_and(image, image, mask=mask_green)

    # Apply Gaussian Blur to remove noise
    blur_img = cv2.GaussianBlur(mask_green, (5,5), 1)

    blur_img_comparision = np.hstack((mask_green, blur_img))
    mask_hsv_comparision = np.hstack((image, hsv, masked_img))

    # Shi-Tomasi Corner Detection
    feature_params = dict(maxCorners=7,
                            qualityLevel=0.01,
                            minDistance=10,
                            blockSize=10)
    corners = cv2.goodFeaturesToTrack(blur_img, mask=None, **feature_params)
    
    if corners is not None and len(corners) > 5:
        corners = np.int0(corners)
        
        points_x = []
        points_y = []
        
        for corner in corners:
            x,y = corner.ravel()
            points_x.append(x)
            points_y.append(y)
            cv2.circle(image, (x,y), 1, (255, 0, 0), -1)
            
        # Fit an ellipse to the corners detected
        ellipse_center, (MA, ma), angle = cv2.fitEllipse(corners)
        cv2.circle(image, (int(ellipse_center[0]), int(ellipse_center[1])), 2, (255, 0, 0), -1)

        # Check if the object detected fits an ellipse (arrow) by a threshold
        if ma/MA > 1.25:
        
            # Find the momentum to detect the arrow head orientation
            M = cv2.moments(blur_img, True)
            moment_center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            # print(moment_center)
            cv2.circle(image, (int(moment_center[0]), int(moment_center[1])), 2, (0, 0, 255), -1)
            
            x_diff = abs(ellipse_center[0] - moment_center[0])
            y_diff = abs(ellipse_center[1] - moment_center[1])
            
            if x_diff > y_diff and moment_center[0] > moment_center[1]:
                if moment_center[0] > ellipse_center[0]:
                    orientation = 'East'
                elif moment_center[0] < ellipse_center[0]:
                    orientation = 'West'
            else:
                if moment_center[1] > ellipse_center[1]:
                    orientation = 'South'
                elif moment_center[1] < ellipse_center[1]:
                    orientation = 'North'
      
        #################################################################
        # NOTE: Following method is slightly flawed and deprecated
        # Find orientation based on where most points fall 
        # away from the center
        #################################################################
                
        # points_x = np.asarray(points_x)
        # points_y = np.asarray(points_y)
        
        # arrow_mid_x = int((np.max(points_x) + np.min(points_x))/2)
        # arrow_dist_x = np.max(points_x) - np.min(points_x)
        
        # arrow_mid_y = int((np.max(points_y) + np.min(points_y))/2)
        # arrow_dist_y = np.max(points_y) - np.min(points_y)
        
        # if arrow_dist_x > arrow_dist_y:
        #     west_corners = 0
        #     east_corners = 0
            
        #     for corner in corners:
        #         x, y = corner.ravel()
        #         if x < int(arrow_mid_x):
        #             west_corners += 1
        #         else:
        #             east_corners += 1

        #     if west_corners > east_corners:
        #         orientation = 'West'
        #     else:
        #         orientation = 'East'
        # else:
        #     north_corners = 0
        #     south_corners = 0
            
        #     for corner in corners:
        #         x, y = corner.ravel()
        #         if y < int(arrow_mid_y):
        #             north_corners += 1
        #         else:
        #             south_corners += 1

        #     if north_corners > south_corners:
        #         orientation = 'North'
        #     else:
        #         orientation = 'South'
        
    return image, orientation, mask_hsv_comparision, blur_img_comparision


if __name__ == '__main__':
    
    test_images = ['test_east.jpg',
                   'test_west.jpg',
                   'test_north.jpg',
                   'test_south.jpg']
    
    for path in test_images:
        img = cv2.imread(path)
        
        arrow_img, orientation, mask, blur = detect_arrow(img)
    
        cv2.putText(arrow_img, orientation, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), lineType=cv2.LINE_AA)
        cv2.imshow("Arrow Detected", arrow_img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    
