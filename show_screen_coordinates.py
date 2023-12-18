import sys
import time
from typing import Optional
import cv2
import numpy as np
from app_config import read_config_file
from screenshooter import get_screenshot

def display_rectangle(image: Optional[np.ndarray] = None, coordinates: dict = {}, color: tuple = (0, 255, 0), window_name: str = "Rectangle"):
    """
    Displays a rectangle on the screen using specified coordinates.

    Args:
    coordinates (dict): A dictionary with keys 'x1', 'y1', 'x2', 'y2' representing coordinates of the rectangle.

    The function creates an image and draws a rectangle based on the provided coordinates, then displays it.
    """
    if image is None:
        image = np.zeros((500, 800, 3), dtype=np.uint8)
    x1, y1, x2, y2 = coordinates["x1"], coordinates["y1"], coordinates["x2"], coordinates["y2"]
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    coordinates_keys_to_show = ["coordinates_screen_XYZ", "coordinates_screen_Facing"]
    config = read_config_file()
    print("The screenshot will be taken in 5s. Please make the focus on the game window.")
    time.sleep(5)
    image = get_screenshot()
    if image is None:
        print("Image is empty, try again")
        sys.exit()
    print("Press 'q' to close image")
    for coordinates in coordinates_keys_to_show:
        if coordinates in config:
            print(f"Show: {coordinates}")
            display_rectangle(image=image.copy(), coordinates=config[coordinates], window_name=coordinates)
        else:
            print(f"Can not find '{coordinates}' in readed config")
