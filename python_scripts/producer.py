'''
*****************************************************************************/

File: producer.py
Author: Andrew Ize-Iyamu
Date: 2024-11-26
Description: Producer thread that recognises the hand gesture using
OpenCV and Google's Gesture Recogniser model, and then sends the gesture ID 
into the queue for the consumer thread to recieve

*****************************************************************************/

References:

*****************************************************************************/
*    Title: An Intro to Threading in Python
*    Author: Anderson, J
*    Date: 2019
*    Code version: N/A
*    Availability: https://realpython.com/intro-to-python-threading/
****************************************************************************/

*****************************************************************************/
*    Title: Multithreading - Producer and Consumer with Queue
*    Author: Hong, K
*    Date: 2020
*    Code version: N/A
*    Availability: https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Producer_Consumer_using_Queue.php
****************************************************************************/

*****************************************************************************/
*    Title: Gesture Recognition Guide for Python
*    Author: Goolge AI for Developers
*    Date: 2024
*    Code version: N/A
*    Availability: https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python
****************************************************************************/
'''

# Establishes a path to the gesture recognizer model
model_path = 'gesture_recognizer.task'

def determine_gesture_id(category_name):
    '''
    Mapping function for category names of hand gestures to assigned number IDs
    '''

    # Dictionary for Gesture IDs
    gestures = {
        'Closed_Fist': 1,
        'Open_Palm': 2,
        'Pointing_Up': 3,
        'Thumb_Down': 4,
        'Thumb_Up': 5,
        'Victory': 6,
        'I_Love_You': 7,
        'None': 8
    }
    return gestures.get(category_name, 8)


def producer(queue):
    '''
    Producer logic that recognises single hand gestures as an input,
    converts them into their gesture ID as the output,
    and places into the threading queue
    '''

    # Google's Gesture Recongition Guide provided the general framework
    # on how to deploy their HandGestureClassifier model on python using
    # the OpenCV and Mediapipe libraries

    # Import required libraries
    import cv2
    import mediapipe as mp
    import numpy as np
    import time

    # Initialize MediaPipe components
    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    def print_result(result: GestureRecognizerResult,
                     output_image: mp.Image,
                     timestamp_ms: int):
        '''
        Callback function that handles the gesture recognition results
        '''
        if result.gestures:
            # Determines the recognised hand gesture's ID and sends it to the queue
            gesture_ID = determine_gesture_id(result.gestures[0][0].category_name)
            print(f"Enqueued gesture ID: {gesture_ID}", flush=True)
            queue.put(gesture_ID)
        else:
            # Defaults unrecognised hand gestures to ID of 8
            queue.put(8)

    # Setup options for the gesture recognizer
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result
    )

    # Start video capture
    capture = cv2.VideoCapture(0)

    # Set interval for processing gestures to reduce latency of signals 
    # sent to the queue for the consumer logic
    processing_interval = 1
    last_processed_time = 0

    # Framework for the Gesture Recognizer instance
    with GestureRecognizer.create_from_options(options) as recognizer:
        while True:
            ret, frame = capture.read()
            if not ret:
                pass
            
            # Monitors the current time as a reference point to establish 
            # intervals for signal retrieval
            current_time = time.time()

            # Flips the frame horizontally for a mirrored view
            frame = cv2.flip(frame, 1)

            # Converts frame to RGB format as MediaPipe requires RGB input
            rgb_frame = cv2.cvtColor(frame, (cv2.COLOR_BGR2RGB))

            # Converts the frame to a MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Processes gestures only at specified intervals to reduce latency
            if current_time - last_processed_time >= processing_interval:
                last_processed_time = current_time

                # Gets an integer timestamp in milliseconds
                timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

                # Processees the frame asynchronously
                recognizer.recognize_async(mp_image, timestamp_ms=timestamp_ms)

            # Displays the processed frame
            # cv2.imshow('Gesture Recognition', frame)
            
            # Breaks loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Releases resources
    capture.release()
    cv2.destroyAllWindows()
