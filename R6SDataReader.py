import cv2 as cv
import pytesseract as pyte
import difflib as diff
import csv
import xlsxwriter as xlw
from typing import List

# TODO: make globals into locals bc globals are bad
killX: int = 1041
killY: int = 190
boxW:  int = 115
boxH:  int = 12

def get_usernames_from_csv(filename: str) -> List[str]:
    assert ".csv" in filename or ".txt" in filename
    userList: List[str] = []
    with open(filename) as file:
        usernames = csv.reader(file, delimiter=",")
        for row in usernames:
            userList.append(row[0])
    return userList

def validate_round_num(parsedround: str, maxRounds: int = 3) -> str:
    roundList: List[str] = []
    for i in range(1, maxRounds):
        roundList.append(f"ROUND {i}")
    return diff.get_close_matches(parsedround, roundList, 1)[0]

def find_closest_username(parsedname: str, usernames: List[str]) -> str:
    return diff.get_close_matches(parsedname, usernames, 1)[0]


def main(videofile: str, userfile: str) -> int:
    usernames: List[str] = get_usernames_from_csv(userfile)
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

    diff.get_close_matches()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, help="image to open")
    args = parser.parse_args()
    main(args.filename)