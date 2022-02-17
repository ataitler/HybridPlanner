import sys
import glob
import cv2


def create_video(frames_dir, output_file, fps):
    img_array = []
    file_list = sorted(
        [x for x in glob.glob(frames_dir + "/*.jpg")])
    for i in range(len(file_list)):
        img = cv2.imread(file_list[i])
        height, width, layers = img.shape
        if i==0:
            size = (width,height)
        img = cv2.resize(img,size)
        img_array.append(img)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(output_file, fourcc, fps, (size[0], size[1]))
    for frame in img_array:
        writer.write(frame)
    writer.release()


    return


def main():
    if len(sys.argv) < 3:
        print("Usage: Im2Vid.py <input folder> <output file> <fps=30>")
        return
    fps = 30
    if len(sys.argv) == 4:
        fps = float(sys.argv[3])
    create_video(sys.argv[1], sys.argv[2], fps)
    return


if __name__ == "__main__":
    main()


