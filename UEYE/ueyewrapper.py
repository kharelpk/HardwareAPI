from pyueye import ueye
import numpy as np

class UYECAM:
    """Wrapper class for controlling uEye cameras."""

    def __init__(self, device_id=0):
        self.h_cam = ueye.HIDS(device_id)
        self.pc_image_memory = ueye.c_mem_p()
        self.mem_id = ueye.int()
        self.pitch = ueye.int()

    def connect(self):
        """
        Initialize the camera and check for errors.
        """
        ret = ueye.is_InitCamera(self.h_cam, None)
        self.__check_error(ret)

    def get_camera_info(self):
        """
        Get the camera serial number.
        
        :return: Camera serial number as a string.
        :rtype: str
        """
        c_info = ueye.CAMINFO()
        ret = ueye.is_GetCameraInfo(self.h_cam, c_info)
        self.__check_error(ret)
        return c_info.SerNo.decode('utf-8')
        
    def get_sensor_info(self):
        """
        Get the camera sensor name.
        
        :return: Sensor name as a string.
        :rtype: str
        """
        s_info = ueye.SENSORINFO()
        ret = ueye.is_GetSensorInfo(self.h_cam, s_info)
        self.__check_error(ret)
        return s_info.strSensorName.decode('utf-8')
    
    def reset_to_default(self):
        """
        Reset the camera settings to default values.
        """
        ret = ueye.is_ResetToDefault(self.h_cam)
        self.__check_error(ret)

    def get_aoi(self):
        """
        Get the Area of Interest (AOI) of the camera.
        
        :return: Tuple of AOI parameters (x, y, width, height).
        :rtype: tuple
        """
        rect_aoi = ueye.IS_RECT()
        ret = ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_GET_AOI, rect_aoi, ueye.sizeof(rect_aoi))
        self.__check_error(ret)
        return (rect_aoi.s32X.value,
                rect_aoi.s32Y.value,
                rect_aoi.s32Width.value,
                rect_aoi.s32Height.value)
        
    def set_aoi(self, x, y, width, height):
        """
        Set the Area of Interest (AOI) of the camera.
        
        :param x: The x-coordinate of the AOI.
        :type x: int
        :param y: The y-coordinate of the AOI.
        :type y: int
        :param width: The width of the AOI.
        :type width: int
        :param height: The height of the AOI.
        :type height: int
        """
        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(x)
        rect_aoi.s32Y = ueye.int(y)
        rect_aoi.s32Width = ueye.int(width)
        rect_aoi.s32Height = ueye.int(height)
        ret = ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))
        self.__check_error(ret)

    def get_colormode(self):
        """
        Get the current color mode of the camera.
        
        :return: The current color mode.
        :rtype: ueye.int
        """
        ret = ueye.is_SetColorMode(self.h_cam, ueye.IS_GET_COLOR_MODE)
        return ret
    
    def set_colormode(self, colormode):
        """
        Set the color mode of the camera.
        
        :param colormode: The color mode to set.
        :type colormode: ueye.int
        """
        ret = ueye.is_SetColorMode(self.h_cam, colormode)
        self.__check_error(ret)

    def allocate_image_memory(self):
        """
        Allocate memory for image data.
        """
        _ , _, self.width, self.height = self.get_aoi()
        self.bitsppixel = self.get_bits_per_pixel(self.get_colormode())
        ret = ueye.is_AllocImageMem(self.h_cam, 
                                      self.width,
                                      self.height, 
                                      self.bitsppixel, 
                                      self.pc_image_memory, 
                                      self.mem_id)


        self.__check_error(ret)


    def capture_video(self, wait=False):
        """
        Start capturing video with the camera.
        
        :param wait: If True, wait for the capture to start; otherwise, don't wait. Default is False.
        :type wait: bool
        """
        if wait:
            ret = ueye.is_CaptureVideo(self.h_cam, ueye.IS_WAIT)
        else:
            ret = ueye.is_CaptureVideo(self.h_cam, ueye.IS_DONT_WAIT)
        self.__check_error(ret)


    def inquire_image_mem(self):
        """
        Inquire the image memory.
        """
        _ , _, self.width, self.height = self.get_aoi()
        self.bitsppixel = self.get_bits_per_pixel(self.get_colormode())
 
        ret = ueye.is_InquireImageMem(self.h_cam, 
                                      self.pc_image_memory,
                                      self.mem_id, 
                                      self.width, 
                                      self.height, 
                                      self.bitsppixel, 
                                      self.pitch)

        self.__check_error(ret)

    def get_image_data(self):
        """
        Get the image data as a NumPy array.
        
        :return: The image data as a NumPy array.
        :rtype: numpy.ndarray
        """
        array = ueye.get_data(self.pc_image_memory,
                              self.width,
                               self.height,
                                 self.bitsppixel,
                                 self.pitch,
                                 copy=False)
        bytes_per_pixel = int(self.bitsppixel / 8)

        frame = np.reshape(array,
                           (self.height, 
                            self.width, 
                            bytes_per_pixel))
        
        return frame
    
    def stop_video(self):
        """
        Stop capturing video with the camera.
        """
        ret = ueye.is_StopLiveVideo(self.h_cam, ueye.IS_FORCE_VIDEO_STOP)
        self.__check_error(ret)

    def free_image_memory(self):
        """
        Free the allocated image memory.
        """
        ret = ueye.is_FreeImageMem(self.h_cam, 
                                   self.pc_image_memory,
                                     self.mem_id)
        self.__check_error(ret)

    def exit(self):
        """
        Close the camera connection and check for errors.
        """
        ret = ueye.is_ExitCamera(self.h_cam)
        self.__check_error(ret)


    def get_bits_per_pixel(self, color_mode):
        """
        Get the number of bits per pixel for the given color mode.
        
        :param color_mode: The color mode for which to get the bits per pixel.
        :type color_mode: ueye.int
        :return: The number of bits per pixel.
        :rtype: int
        """
        bits_per_pixel = {
            ueye.IS_CM_SENSOR_RAW8: 8,
            ueye.IS_CM_SENSOR_RAW10: 16,
            ueye.IS_CM_SENSOR_RAW12: 16,
            ueye.IS_CM_SENSOR_RAW16: 16,
            ueye.IS_CM_MONO8: 8,
            ueye.IS_CM_RGB8_PACKED: 24,
            ueye.IS_CM_BGR8_PACKED: 24,
            ueye.IS_CM_RGBA8_PACKED: 32,
            ueye.IS_CM_BGRA8_PACKED: 32,
            ueye.IS_CM_BGR10_PACKED: 32,
            ueye.IS_CM_RGB10_PACKED: 32,
            ueye.IS_CM_BGRA12_UNPACKED: 64,
            ueye.IS_CM_BGR12_UNPACKED: 48,
            ueye.IS_CM_BGRY8_PACKED: 32,
            ueye.IS_CM_BGR565_PACKED: 16,
            ueye.IS_CM_BGR5_PACKED: 16,
            ueye.IS_CM_UYVY_PACKED: 16,
            ueye.IS_CM_UYVY_MONO_PACKED: 16,
            ueye.IS_CM_UYVY_BAYER_PACKED: 16,
            ueye.IS_CM_CBYCRY_PACKED: 16,        
        } 
        
        return bits_per_pixel[color_mode]

    def __check_error(self, ret):
        """
        Check for errors and raise an exception if an error is found.
        
        :param ret: The return value to check for errors.
        :type ret: int
        """
        if ret != ueye.IS_SUCCESS:
            raise Exception(ret)
        
