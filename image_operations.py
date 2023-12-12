from datetime import datetime
import os
from typing import Optional

import cv2
import numpy as np
from PIL import Image, ImageGrab
from app_config import OUTPUTS_DIR_PATH, get_save_images_flags
from logger import app_logger

def convert_screenshot_for_opencv(screenshot: ImageGrab) -> np.ndarray:
    """
    Converts a screenshot into a format compatible with OpenCV.

    Args:
        screenshot (PIL ImageGrab object): Screenshot captured using the PIL library.

    Returns:
        Numpy array: A representation of the image in OpenCV format (BGR color space).
    """
    try:
        image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        app_logger.debug(f"screenshot was converted to opencv format")
        return open_cv_image
    except Exception as ex:
        app_logger.error(ex)

def convert_cv_image_to_gray(image: np.ndarray) -> np.ndarray:
    """
    Converts a color OpenCV image to grayscale.

    Args:
        image (Numpy array): An image in OpenCV format (BGR color space).

    Returns:
        Numpy array: The converted grayscale image.
    """
    try:
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            app_logger.debug(f"screenshot was converted to gray")
            return gray_image
        else:
            app_logger.debug(f"screenshot is already in gray")
            return image
    except Exception as ex:
        app_logger.error(ex)

def crop_image_by_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Crops an image using a binary mask.

    Args:
        image (Numpy array): The image to be cropped.
        mask (Numpy array): A binary mask indicating the region to crop.

    Returns:
        Numpy array: The cropped image.
    """
    try:
        points = np.where(mask == 255)
        y1, x1 = np.min(points, axis=1)
        y2, x2 = np.max(points, axis=1)
        cropped_image = image[y1:y2, x1:x2]
        app_logger.debug(f"image was cropped using mask")
        return cropped_image
    except Exception as ex:
        app_logger.error(ex)

def save_cv_image(image: np.ndarray, output_folder: str = OUTPUTS_DIR_PATH, filename: Optional[str] = None) -> None:
    """
    Saves an OpenCV image to a file.

    Args:
        image (Numpy array): The image to be saved.
        output_folder (str): Directory path where the image will be saved.
        filename (str, optional): The name of the file. Defaults to a timestamp if not provided.
    """
    try:
        if image is not None:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}.png"
            file_path = os.path.join(output_folder, filename)
            cv2.imwrite(file_path, image)
            app_logger.info(f"Image saved as {file_path}")
        else:
            app_logger.warning("Taked image is None")
    except Exception as ex:
        app_logger.error(ex)

def show_cv_image(image: np.ndarray) -> None:
    """
    Displays an OpenCV image in a window.

    Args:
        image (Numpy array): The image to be displayed.
    """
    try:
        if image is not None and image.size > 0:
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            app_logger.warning("Image is None or or is too small.")
    except Exception as ex:
        app_logger.error(ex)

def load_cv_image(file_path: str) -> Optional[np.ndarray]:
    """
    Loads an image from a file into OpenCV format.

    Args:
        file_path (str): The path to the image file.

    Returns:
        Numpy array: The loaded image in OpenCV format, or None if loading fails.
    """
    try:
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if image is not None:
            return image
        else:
            app_logger.info(f"Failed to load image from {file_path}.")
            return None
    except Exception as ex:
        app_logger.info(f"An exception occurred while loading an image: {ex}")
        return None

def save_image_for_function(function_name: str, image_variable_name: str, image: np.ndarray) -> None:
    """
    Saves an image if flag for function_name is set True with a filename that includes the function name, image variable name, and a timestamp.

    Args:
        function_name (str): The name of the function calling this save operation.
        image_variable_name (str): The name of the variable holding the image.
        image (np.ndarray): The image to be saved.
    """
    save_images_flags = get_save_images_flags()
    if save_images_flags[function_name]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename = f"{function_name}_{image_variable_name}_{timestamp}.png"
        save_cv_image(filename=filename, image=image)
        app_logger.debug(f"Saved {image_variable_name} in default path with filename: {filename}")