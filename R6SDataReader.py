import cv2 as cv
import pytesseract as pyte
# TODO: import python library for comparing strings


killX: int = 1041
killY: int = 190
boxW:  int = 115
boxH:  int = 12

def main(filename: str) -> int:
    # TODO: add excel spreadsheet stuff
    # TODO: add logic to make sure the same kill is only added once
    # vc = cv.VideoCapture(filename)
    # rv, img = vc.read()
    # if not rv:
    #     print("failed to read image\n")
    #     return -1
    img = cv.imread(filename)
    cv.imshow("original", img)
    cv.waitKey()
    cropped = img[killY:killY + boxH, killX:killX + boxW]
    cropped = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    th = cv.adaptiveThreshold(cropped, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 3, -3)
    cv.imshow("cropped", th)
    cv.waitKey()
    
    text = pyte.image_to_string(th)

    print(text)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, help="image to open")
    args = parser.parse_args()
    main(args.filename)