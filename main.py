import cv2 as cv
import os
from pathlib import Path

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.config import Config


Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '360')
Config.set('graphics', 'resizable', False)


class MainWindow(Widget):
    images_path = ObjectProperty(text="C:\\Users\\Alpha\\Desktop\\watermark\\images")
    masks_path = ObjectProperty(text="C:\\Users\\Alpha\\Desktop\\watermark\\masks")

    def clear_image(self, image, mask):
        img = cv.imread(image)
        mask = cv.imread(mask, 0)
        dst = cv.inpaint(img, mask, 3, cv.INPAINT_TELEA)
        result_path = os.path.join(Path(self.images_path.text).parent, "result")
        try:
            os.mkdir(result_path, mode=0o777)
        except FileExistsError:
            pass
        img_name = image.replace("\\", "/").split("/")[-1]
        print(os.path.join(result_path, img_name))
        cv.imwrite(os.path.join(result_path, img_name), dst)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def run_button(self):
        if self.images_path.text != "" and self.masks_path.text != "":
            img_list = os.listdir(path=self.images_path.text)
            for i in img_list:
                self.clear_image(os.path.join(self.images_path.text, i),
                                 os.path.join(self.masks_path.text, i))


class WatermarkApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    WatermarkApp().run()
