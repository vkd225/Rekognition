
import urllib
import cv2
import numpy as np
import os


def store_raw_images():
    # http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957 --> Face images
    images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    image_urls = urllib.urlopen(images_link).read().decode('utf-8')
    pic_num = 1

    if not os.path.exists('neg'):
        os.makedirs('neg')

    pic_num = 1538

    for i in image_urls.split('\n'):
        try:
            print(i)
            urllib.urlretrieve(i, "neg/" + str(pic_num) + ".jpg")
            img = cv2.imread("neg/" + str(pic_num) + ".jpg")
            # should be larger than samples / pos pic (so we can place our image on it)
            # resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/" + str(pic_num) + ".jpg", img)
            pic_num += 1

        except Exception as e:
            print(str(e))


store_raw_images()

