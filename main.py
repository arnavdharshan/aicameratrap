from picamzero import Camera
import gpiod
import time
import pathlib
import os
platform = os.name
if not platform == 'nt': pathlib.WindowsPath = pathlib.PosixPath
import yolov9
from PIL import Image as PILImage

def take_picture():
	cam = Camera()
	cam.start_preview()
	cam.take_photo("./cam1.jpg")
	cam.stop_preview()	

def get_pil_image(image_url):
    pillow_image = PILImage.open(image_url).convert("RGB")
    return pillow_image

def get_image_category_from_yolo(image_url):
    if image_url:
        yoloModel.conf = 0.1  # NMS confidence threshold
        yoloModel.iou = 0.45  # NMS IoU threshold
        yoloModel.agnostic = False  # NMS class-agnostic
        yoloModel.multi_label = False  # NMS multiple labels per box
        yoloModel.max_det = 100  # maximum number of detections per image
        results = yoloModel(get_pil_image(image_url))
        predictions = results.pred[0]
        boxes = predictions[:, :4] # x1, y1, x2, y2
        scores = predictions[:, 4]
        categories = predictions[:, 5]

        classes = results.pandas().xyxy[0]["name"].tolist()
        return classes	
    else:
        return "No image provided.", 400

def is_human_present_in_image(image_url):
   categories = get_image_category_from_yolo(image_url)
   if "Human" in categories:
      return True
   else:
      return False
LED_PIN = 13
def blink_led_red(truefalse):
	if truefalse == True:
		chip = gpiod.Chip('gpiochip4')
		led_line = chip.get_line(LED_PIN)
		led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
		try:
		   count=1
		   while count<5:
		       led_line.set_value(1)
		       time.sleep(1)
		       led_line.set_value(0)
		       time.sleep(1)
		       count=count+1
		finally:
		   print("Releasing the line")
		   led_line.release()


yoloModel = yolov9.load('model.pt')
#print(is_human_present_in_image("./camtest1.jpg"))
#print(is_human_present_in_image("./bb1.jpg"))
blink_led_red(is_human_present_in_image("./camtest1.jpg"))
take_picture()
