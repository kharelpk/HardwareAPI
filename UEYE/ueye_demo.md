### **UEye Camera**
This IDS imaging uEye camera can be controlled via USB communication.

### **Prerequisite**
Please download and install the [uEye camera](https://www.ids-imaging.us/downloads.html) software that installs the necessary drivers from IDS imaging. 

You need to also install these python libraries.
```python
pip install pyueye numpy opencv-python
```

### **Example**

```python
import cv2
from ueyewrapper import UeyeCam

def display_camera_output(camera):
    while True:
        camera.inquire_image_mem()
        frame = camera.get_image_data()
        cv2.imshow('uEye Camera (Press q to exit)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    # Initalize the camera
    camera = UeyeCam(device_id=0)
    camera.connect()
    # Set color mode
    camera.set_colormode(ueye.IS_CM_BGR8_PACKED)
    # Ret area of interest and allocate memory for acquisition
    camera.set_aoi(0, 0, 1280, 1080)
    camera.allocate_image_memory()
    # Capture video
    camera.capture_video(wait=True)

    # display video and exit when you press 'q'
    try:
        display_camera_output(camera)
    finally:
        camera.stop_video()
        camera.free_image_memory()
        camera.exit()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

```

This example code does the following:

1. Imports the necessary modules and the UeyeCam class from the ueye_cam.py file provided.
2. Defines a display_camera_output function that shows the camera output and allows the user to exit by pressing 'q'.
3. Defines a main function that:
    - Initializes the uEye camera with the given device ID (0 by default).
    - Connects to the camera.
    - Sets the color mode.
    - Sets the region of interest (ROI).
    - Allocates image memory.
    - Captures video.
    - Displays the camera output using the display_camera_output function.
    - Stops the video, frees image memory, exits the camera, and closes the display window after the user presses 'q'.
To run the example, make sure you have the ueye_cam.py file (the UeyeCam class implementation) in the same directory as the example script.

