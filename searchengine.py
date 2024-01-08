import os, ast, pprint, string, contractions, csv
import numpy as np
import cv2
from glob import glob
from captioning import predict_step
import time
from playMov import ply
from textblob import TextBlob
from autocorrect import Speller
from nltk.corpus import stopwords

from ultralytics import YOLO
from IPython.display import display, Image

def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name {path}")

def save_frame(video_path, save_dir):
    name = video_path.split("\\")[-1].split(".")[0]
    save_path = os.path.join("C:\\Users\\bibas\Music",save_dir, name)
    create_dir(save_path)

#    print(name)

    cap = cv2.VideoCapture(video_path)
    fps=round(cap.get(cv2.CAP_PROP_FPS))
    idx = 0

    while True:
        ret, frame = cap.read()

        if ret == False:
            cap.release()
            break

        if idx == 0:
            cv2.imwrite(f"{save_path}/{idx}.png", frame)
        else:
            if idx % fps == 0:
                cv2.imwrite(f"{save_path}/{idx}.png", frame)

        idx += 1

def frames():
    video_paths = glob("C:\\Users\\bibas\Music\\videos\\*")

    print(video_paths)

    save_dir = "save2"

    for path in video_paths:
        save_frame(path, save_dir)
    #save_frame("C:\\Users\\bibas\\Music\\videos", save_dir)

def procs():
    names= {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
    HOME = r"C:\\Users\\bibas\Music"
    pic= r"C:\Users\bibas\Music\save2\shorts"
    model = YOLO(f'{HOME}/yolov8x.pt')
    data = {}
    
    with open('data1.csv','w',newline='') as f:
        fieldnames = ['TIME','YOLO','VIT']
        thewriter = csv.DictWriter(f,fieldnames=fieldnames)
        thewriter.writeheader()

    for filename in os.listdir(pic):
            if filename.endswith('.png'):
                with open(os.path.join(pic, filename)) as f:
                    #print(filename)
                    results1 = model.predict(source=os.path.join(pic, filename), conf=0.25)
                    di = os.path.join(pic, filename)
                    results2 = str(predict_step([di]))
                    #print(results[0].boxes.cls)
                    a = results1[0].boxes.cls
                    temp=""
                    for i in a:
                        #print(names[int(i)])
                        temp += f" {names[int(i)]}"
                        
                    tempTuple = os.path.splitext(filename)
                    filename = tempTuple[0]
                    data[filename] = f"{temp}, {results2[2:-2]}"  
                    
                    with open('data1.csv','a',newline='') as f:
                        fieldnames = ['TIME','YOLO','VIT']
                        thewriter = csv.DictWriter(f,fieldnames=fieldnames)
                        thewriter.writerow({"TIME": int(filename),"YOLO": temp,"VIT": results2[2:-2]})
    
    print(data)

    print(len(data))

    with open(r'C:\Users\bibas\Music\Data\data1.txt','w') as text:
        text.write(str(data))


def result():       
    os.chdir(r'C:\Users\bibas\music')

    with open(r'C:\Users\bibas\Music\Data\easy.txt','r') as text:
        stt = str(text.readline())

    dx = ast.literal_eval(str(stt)) 
    #pprint.pprint(rr)
    #pprint.pprint(len(dx))

    print("Enter discription of any scence in the video: ")
    a = input()
    org=a
    a=a.lower()
    a=contractions.fix(a)
    a = a.translate(str.maketrans('','',string.punctuation))
    a= TextBlob(a)
    a = a.correct().string
    spell = Speller()
    a = spell(a)

    nt=[]
    for word in a.split():
        if word not in stopwords.words('english'):
            nt.append(word)
    a = " ".join(nt)
    nt.clear()
    print(a)

    c={}
    for k in dx.keys():
        c[int(k)] = dx[k]
    c = dict(sorted(c.items()))
    print(c)
 
    flo=1
    for i in c.keys():
        if flo == 2:
            fps = i
        if list(c)[-1] == i:
            last = k
            print(f"last= {last}")
        flo += 1

    a=a.split()
    print(a)
    
    score = []
    star = []
    stp = []
    s=0
    one = 0
    two = 0
    for k,i in c.items():
        #print(k, i)
        for j in a:
            #print(j)
            if j in i:
                two = 1
        
        if one == 1 and two == 1:
            s += 1
            one = 1
            two=0

        elif one == 0 and two == 1:
            s += 1
            star.append(k)
            one = 1
            two=0
        
        elif one == 1 and two == 0:
            stp.append(k)
            score.append(s)          
            s = 0
            one = 0
            two=0
        else:
            two = 0
        
        if one == 1 and k == last:
            stp.append(k)
            score.append(s)          
            s = 0
            one = 0
            two=0


    print(score, len(score))
    print(star,len(star))
    print(stp,len(stp))
    
    vv=max(score)
    print(f"Max score= {vv}")
    print(f"No. of Contact= {score.count(vv)}")
    ss = 0
    for i, j in enumerate(score):
        if j == vv:
            print(f"\nAt index= {i}")
            print(star[i])
            print(stp[i])
            ply(star[i],stp[i],ss,fps,"easy")
            ss += 1

if __name__ == "__main__":
    #frames()
    #procs()
    result()


