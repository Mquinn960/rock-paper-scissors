import cv2, sys, os
from time import sleep

mode = "auto"
images_per_class = 10 
test_to_train_ratio = 0.2 
init_delay = 3
delaybetween = 0.2 
base_path = "..\\datasets\\"
dataset_name = "career-ready\\"
train_path = "train"
test_path = "test"
classes = ["rock", "paper", "scissors", "none"]
# classes = ["rock", "paper", "scissors", "lizard", "spock", "none"]
participant = input("Please enter participant name: ").upper()

paths = [base_path + dataset_name + train_path,
         base_path + dataset_name + test_path]

for path in paths:
    if path != "":
        if os.path.exists(path) == False:
            os.makedirs(path)

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (50,200)
fontScale              = 2
fontColor              = (255,255,255)
lineType               = 2

def write_message(img, text, ):
    cv2.putText(img, text, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
    
cam = cv2.VideoCapture(0)

cv2.namedWindow("Dataset Creator Test View")

iteration = 1
class_count = len(classes)

while True:
    ret, frame = cam.read()
    write_message(frame, "Spacebar to Start")
    cv2.imshow("Dataset Creator Capture Window", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Exiting Application")
        cam.release()
        cv2.destroyAllWindows()
        break
    elif k%256 == 32:
        # SPACE pressed
        print("Begin Capture")
        for image_class in classes:
            img_counter = 1
            image_class = image_class.upper()
            train_cut_off = images_per_class - (test_to_train_ratio * images_per_class)

            ret, frame = cam.read()
            write_message(frame, image_class)
            cv2.imshow("Dataset Creator Capture Window", frame)
            cv2.waitKey(0)

            while True and img_counter <= int(images_per_class):
                ret, frame = cam.read()
                cv2.imshow("Dataset Creator Capture Window", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)

                if k%256 == 27:
                    # ESC pressed
                    print("Exiting Application")
                    cam.release()
                    cv2.destroyAllWindows()
                    break

                if (img_counter <= train_cut_off):
                    img_name = base_path + dataset_name + train_path + "/{}_{}_{}.png".format(image_class, participant, img_counter)
                else:
                    img_name = base_path + dataset_name + test_path + "/{}_{}_{}.png".format(image_class, participant, img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
                sleep(float(delaybetween))
            
            if (iteration == class_count):
                ret, frame = cam.read()
                write_message(frame, "Good Job! Next! :)")
                cv2.imshow("Dataset Creator Capture Window", frame)
                cv2.waitKey(0)
                print("Exiting Application")
                cam.release()
                cv2.destroyAllWindows()
                sys.exit()
            else:
                iteration += 1
        
cam.release()

cv2.destroyAllWindows()