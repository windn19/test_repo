import json
from os import listdir
import re

import easyocr
import cv2
import numpy as np
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import rotate


# haar_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')



def prepare_image(read, img, res):
  # res = []
  # img = cv2.imread(path)
  # print(img.shape)
  # img = cv2.resize(img, (160, 90))
  grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  # grayimg = img
  img1 = canny(grayimg, sigma=3.0)
  out, angles, distances = hough_line(img1)
  h, theta,  d= out, angles, distances 
  angle_step = 0.5 * np.diff(theta).mean()
  d_step = 0.5 * np.diff(d).mean()
  bounds = [np.rad2deg(theta[0] - angle_step),
          np.rad2deg(theta[-1] + angle_step),
          d[-1] + d_step, d[0] - d_step]
  _, angles_peaks, _ = hough_line_peaks(out, angles, distances, num_peaks=20)
  angle = np.mean(np.rad2deg(angles_peaks))
  # print(angle, type(angle))
  if 0 <= angle <= 90:
    rot_angle = angle - 90
  elif -45 <= angle < 0:
      rot_angle = angle - 90
  elif -90 <= angle < -45:
      rot_angle = 90 + angle
  else:
    rot_angle = 0
  if abs(rot_angle) > 20:
      rot_angle=0
  # print('угол наклона',rot_angle )
  rotated = rotate(img, rot_angle, resize=True)*255
  rotated =rotated.astype(np.uint8)
  # rotated = cv2.resize(rotated, (160, 90))
  # rotated = np.reshape(rotated,  (90, 160, 1))
  # print(rotated.shape)
  # rotated1 = rotated[:,:,:]
  # if rotated.shape[1]/rotated.shape[0] < 2:
  #     minus = np.abs(int(np.sin(np.radians(rot_angle))*rotated.shape[0]))
  #     rotated1 = rotated[minus:-minus,:,:]
  #     print(minus)
  # print(rotated1.shape)
  lab= cv2.cvtColor(rotated, cv2.COLOR_BGR2LAB)
  l, a, b = cv2.split(lab)
  clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
  cl = clahe.apply(l)
  limg = cv2.merge((cl,a,b))
  final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
  grayfinal = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
  tfinal = cv2.threshold(grayfinal, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
  
  # text = read.readtext(final, detail=0, allowlist=list('АВЕКМНОРСТУХ0987654321авекмнорстух'), paragraph=True)
  # text1 = read.readtext(img, detail=0, allowlist=list('АВЕКМНОРСТУХ0987654321авекмнорстух'), paragraph=True)
  # text2 = read.readtext(tfinal, detail=0, allowlist=list('АВЕКМНОРСТУХ0987654321авекмнорстух'), paragraph=True)
  text = read.readtext(final, detail=0, allowlist=list('ABEKMHOPCTYXabekmhopctyx0987456321'), paragraph=True)
  text1 = read.readtext(img, detail=0,  allowlist=list('ABEKMHOPCTYXabekmhopctyx0987456321'), paragraph=True)
  text2 = read.readtext(tfinal, detail=0,  allowlist=list('ABEKMHOPCTYXabekmhopctyx0987456321'), paragraph=True)
  print(text)
  print(text1)
  print(text2)
  res.extend(text + text1 + text2)
  # final2=rotated1-final
  # final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
  # final = np.expand_dims(final, axis=-1)
  # print('>', final.shape)
  return res


if __name__ == '__main__':
	number = re.compile(r'[АВЕКМНОРСТУХавекмнорстух]\d{3}[АВЕКМНОРСТУХавекмнорстух]{2}\s?\d{2,3}')
	n = []
	
	for filename in listdir('car-numbers/'):
	  if filename.endswith('.jpg'):
	  	print(f'{filename:>50}')
	  	n.extend(prepare_image(f'car-numbers/{filename}'))
	d = {'result': n}
	with open('list.json', mode='w', encoding='utf8') as f:
	  json.dump(d, f, ensure_ascii=False)

    
    
