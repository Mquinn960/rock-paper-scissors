import cv2, sys, os
from time import sleep

# removable config - will prompt otherwise

mode = "auto"
images = 100                # Total images captured in auto mode
test_to_train_ratio = 0.2      # Ratio of training images to testing images required
delay = 3                   # Camera initialisation delay
delaybetween = 0.1          # Delay between image captures
train_path = "train"         # Training image folder
test_path = "test"           # Testing image folder
folder_paths = [train_path, test_path] 

def is_set(variable):
    return (variable in locals() or variable in globals())

if not is_set('label'):
    label = input("Please enter training class label: ").upper()

if not is_set('mode'):
    mode = input("Training Mode [manual/auto]: ")

if mode != "manual" and mode != "auto":
    print("Training mode unrecognised")
    sys.exit()

if mode == "auto":
    if not is_set('images'):
        images = input("Number of images to record per class: ")
    if not is_set('delay'):
        delay = input("Delay before recording (seconds): ")
    if not is_set('delaybetween'):
        delaybetween = input("Delay between image captures: ")

if not is_set('train_path'):
    train_path = input("If training folder required specify name otherwise leave blank: ")
if not is_set('test_path'):
    test_path = input("If testing folder required specify name otherwise leave blank: ")

for path in folder_paths:
    if path != "":
        if os.path.exists(path) == False:
            os.mkdir(path)

cam = cv2.VideoCapture(0)

cv2.namedWindow("Dataset Creator Test View")

img_counter = 1

if mode == "manual":
    while True:
        ret, frame = cam.read()
        cv2.imshow("Dataset Creator Capture Window", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Exiting Application")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = train_path + "/" + label + "_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
elif mode == "auto":
    train_cut_off = images - (test_to_train_ratio * images)
    ret, frame = cam.read()
    cv2.imshow("Camera Initialiation Window", frame)
    sleep(float(delay))
    while True and img_counter <= int(images):
        ret, frame = cam.read()
        cv2.imshow("Dataset Creator Capture Window", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Exiting Application")
            break

        if (img_counter <= train_cut_off):
            img_name = train_path + "/" + label + "_{}.png".format(img_counter)
        else:
            img_name = test_path + "/" + label + "_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        sleep(float(delaybetween))

cam.release()

cv2.destroyAllWindows()