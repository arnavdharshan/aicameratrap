import pathlib
import os
platform = os.name
if not platform == 'nt': pathlib.WindowsPath = pathlib.PosixPath
import yolov9
from PIL import Image as PILImage

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

yoloModel = yolov9.load('model.pt')
print(is_human_present_in_image("./camtest1.jpg"))
print(is_human_present_in_image("./bb1.jpg"))

