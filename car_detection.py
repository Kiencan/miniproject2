import cv2
import numpy as np


cap = cv2.VideoCapture('car.mp4')

kernel = np.ones((20, 20), np.uint8)

# Initialize counters and a dictionary to store car directions
left_car_count = 0
right_car_count = 0
car_positions = {}  # Dictionary to track car positions between frames

middle_line_y = 400  # Y-coordinate of the middle line

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(3))
height = int(cap.get(4))

output = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()

    if ret:

        # Convert the frame to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
		# thresholding image
        ret, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        
		# 
        invert = cv2.bitwise_not(thresh)
        dilation = cv2.dilate(invert, kernel, iterations=1) 
        dilation = cv2.bitwise_not(dilation)
        
        # Edge detection using Canny
        edges = cv2.Canny(dilation, 50, 200)
        
        contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # middle_line = cv2.line(frame, (0, frame.shape[0]//2), (frame.shape[1], frame.shape[0]//2), (255, 0, 0), 3)
        middle_line = cv2.line(frame, (0, middle_line_y), (frame.shape[1], middle_line_y), (255, 0, 0), 3)
        
        left_polygon = np.array([(82, 451), (257, 358), (576, 358), (548, 489)])
        left_area = cv2.polylines(frame, [left_polygon], True, (0, 255, 0), 2)
        
        right_polygon = np.array([(668, 514), (647, 394), (976, 375), (1181, 510)])
        right_area = cv2.polylines(frame, [right_polygon], True, (0, 255, 0), 2)
        
		# Reset the car counts for each frame
        left_car_count = 0
        right_car_count = 0

        current_centers = {}
        
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if  w < 250 and h < 250 and w > 10 and h > 5:
                # cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)
                center_x = x + w // 2
                center_y = y + h // 2
                point = (center_x, center_y)
                if cv2.pointPolygonTest(left_polygon, point, False) >= 0:
                    left_car_count += 1
                     
                elif cv2.pointPolygonTest(right_polygon, point, False) >= 0:
                    right_car_count += 1

                # Initialize bounding box color (green by default)
                bbox_color = (0, 255, 0)

                # Identify the car's movement direction
                if i in car_positions:
                    prev_y = car_positions[i]
                    
                    # If the car crosses the middle line, detect direction
                    if center_x < frame.shape[1]//2 and prev_y < middle_line_y:
                        # Car is moving up (crossed from below)
                        bbox_color = (0, 0, 0)  # Change color to black
                    elif center_x > frame.shape[1]//2 and prev_y > middle_line_y:
                        # Car is moving down (crossed from above)
                        bbox_color = (0, 255, 255)  # Change color to yellow
                    else: 
                        bbox_color = (0, 255, 0)  # Change color to green
                
                # Update the car's current position
                car_positions[i] = center_y

                # Draw the bounding box with the respective color
                cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), bbox_color, 2)
        
        cv2.putText(frame, f'Lan trai: {left_car_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Lan phai: {right_car_count}', (frame.shape[1] - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Display the video  with detected cars and lane lines
        output.write(frame)
        cv2.imshow('origin', frame)
        

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

output.release()
cap.release()
cv2.destroyAllWindows()