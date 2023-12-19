import datetime
import re
import threading
import time
from typing import Optional
import easyocr as easyocr
import numpy as np
import torch
from app_config import get_coordinates_screen_XYZ_analysis_flag, get_coordinates_screen_XYZ
from image_operations import convert_cv_image_to_gray, load_cv_image, save_image_for_function
from logger import app_logger
from screenshooter import get_last_screenshot

#to install PyTorch on Windows: pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# more on site: https://pytorch.org/

coordinates_flag_XYZ = False
coordinates_flag_Facing = False

def get_coordinates_flag_XYZ() -> bool:
    return coordinates_flag_XYZ

def get_coordinates_flag_Facing() -> bool:
    return coordinates_flag_Facing

analysis_frequency = 1

coordinates_XYZ = {}

def get_coordinates_XYZ() -> dict:
    return coordinates_XYZ

def set_coordinates_XYZ(new_coordinates_XYZ: dict = {}) -> None:
    global coordinates_XYZ
    coordinates_XYZ = new_coordinates_XYZ

def convert_to_float(string_value: str) -> float:
    """
    Attempts to convert a string to a float.

    Args:
        string_value (str): The string to be converted.

    Returns:
        float: The converted float value if the conversion is successful, or None if an error occurs.
    """
    try:
        return float(string_value)
    except ValueError:
        return None

def extract_text_from_image(image: Optional[np.ndarray] = None, coordinates: dict = {}) -> str:
    """
    Extracts text from a specified region of an image using OCR.

    Args:
        image (np.ndarray): The image from which text is to be extracted.
        coordinates (dict): A dictionary with keys 'x1', 'y1', 'x2', 'y2' specifying the region of interest.

    Returns:
        str: Extracted text from the specified region of the image. Returns an empty string if no text is detected.
    """
    app_logger.debug(f"torch.cuda.is_available(): {torch.cuda.is_available()}") #TODO: move out of the function
    app_logger.debug(f"torch.version.cuda: {torch.version.cuda}")
    app_logger.debug(f"print(torch.__version__): {torch.__version__}")

    reader = easyocr.Reader(['en'])
    contrast_ths = 0.5
    adjust_contrast = 1.5
    add_margin = 0.05
    try:
        if image is None:
            app_logger.warning("Taked image is None - exit the function")
            return ""
        if not coordinates:
            app_logger.warning("Taked coordinates is empty - exit the function")
            return ""
        elif not 'x1' in coordinates or not 'y1' in coordinates or not 'x2' in coordinates or not 'y2' in coordinates:
            app_logger.warning(f"Taked coordinates do not have the required keys - exit the function, coordinates: {coordinates}")
            return ""
        save_image_for_function("extract_text_from_image", "image", image)
        cropped_image = image[coordinates['y1']:coordinates['y2'], coordinates['x1']:coordinates['x2']]
        cropped_image_gray = convert_cv_image_to_gray(cropped_image)
        # cropped_image_blur = cv2.GaussianBlur(cropped_image_gray, (5,5), 0) #OUTPUT:  KZ: -831.920 66.50000 ~238.981 ------------------------ OUTPUT:  831.920 66.50000 / -238.981 --------------- OUTPUT:  Facing: north (Towards negative 2) (153.2 / -90.0)
        cropped_image_blur = cropped_image_gray #OUTPUT:  XyZ: 831.920 66.50000 -238.981 ---------------- OUTPUT:  831.920 66.50000 -238.981 ----------------- OUTPUT:  Facing: north (Touards negative Z) (1532 ~90.0)
        save_image_for_function("extract_text_from_image", "cropped_image_blur", cropped_image_blur)
        results = reader.readtext(cropped_image_blur,
                         detail = 0,
                         decoder = 'beamsearch',
                         contrast_ths=contrast_ths,
                         adjust_contrast=adjust_contrast,
                         add_margin=add_margin)
        extracted_text = ''
        for text in results:
            extracted_text = extracted_text + " " + text
        app_logger.debug(f"extracted_text: {extracted_text}")
        return extracted_text #TODO: add loggers
    except Exception as ex:
        app_logger.error(ex)

def coordinates_analyzer_loop_XYZ() -> None:
    """
    Continuously analyzes screen coordinates and extracts XYZ values from a designated screen area.

    This function runs in a loop, checking at regular intervals defined by 'analysis_frequency'.
    It loads an image (screenshot), extracts text from a predefined screen region, and processes
    this text to extract XYZ coordinate values. The function updates a global dictionary with
    these coordinates if successful. It handles cases where text extraction or conversion to float
    fails, logging appropriate messages.
    """
    last_iteration_time = datetime.datetime.now()
    run_flag = get_coordinates_screen_XYZ_analysis_flag()
    coordinates = get_coordinates_screen_XYZ()
    while run_flag:
        current_time = datetime.datetime.now()
        time_difference = current_time - last_iteration_time
        if time_difference.total_seconds() < analysis_frequency:
            app_logger.debug("Less than 1 second has passed since the last iteration - sleep for 0.5s.")
            time.sleep(0.5)
            continue
        image = get_last_screenshot()
        if image is not None:
            output_str = extract_text_from_image(image, coordinates)
            output_str.replace('~', '-')
            output_str.replace('/', ' ')
            output_str = re.sub("\s\s+", " ", output_str)
            output_list = [item for item in output_str.split(" ") if item]
            app_logger.debug(f"output_list: {output_list}")
            if len(output_list) == 4:
                output_list.pop(0)
            if len(output_list) == 3:
                x = convert_to_float(output_list[0])
                y = convert_to_float(output_list[1])
                z = convert_to_float(output_list[2])
                tmp_dict = {}
                if x is not None and y is not None and z is not None:
                    tmp_dict = {
                        'x': x,
                        'y': y,
                        'z': z,
                    }
                else:
                    app_logger.debug(f"One of the coordinates could not be converted to a number, x: {x} y: {y} z: {z}")
                app_logger.debug(f"coordinates_XYZ is set to new value: {tmp_dict}")
                set_coordinates_XYZ(tmp_dict)
            else:
                app_logger.debug(f"The list does not have the required length, output_list: {output_list}")
        else:
            app_logger.warning("Taked image is empty.")
            continue
        last_iteration_time = current_time

def start_analyzer_XYZ_thread() -> None:
    """
    Starts the 'coordinates_analyzer_loop_XYZ' function in a separate thread.

    This function initializes and starts a daemon thread running the coordinates analysis loop.
    The loop continuously monitors and analyzes screen coordinates for XYZ values extraction.
    The thread runs as a daemon, meaning it will automatically close when the main program exits.
    """
    watcher_thread = threading.Thread(target=coordinates_analyzer_loop_XYZ)
    watcher_thread.daemon = True
    watcher_thread.start()
