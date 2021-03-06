import cv2 as cv
import pytesseract as pyte
import difflib as diff
import csv
import xlsxwriter as xlw
from typing import List

# TODO: make this handle short usernames
class boxes(object):
    def __init__(self, img):
        self.img = img
        self.killboxW:    int = 115
        self.killboxH:    int = 12
        self.leftkillX:   int = 1041
        self.rightkillX:  int = 1215
        firstkillY:  int = 190
        self.blY: List[int] = []
        self.blY.append(firstkillY)
        for i in range(4):
            self.blY.append(self.blY[i] + self.killboxH)

    def getKiller(self, index: int):
        assert index < 5
        return self.img[self.blY[index]:self.blY[index + 1], self.leftkillX:self.leftkillX + self.killboxW]

    def getVictim(self, index: int):
        assert index < 5
        return self.img[self.blY[index]:self.blY[index + 1], self.rightkillX:self.rightkillX + self.killboxW]

    def getTimestamp(self):
        tsWidth:  int = 80
        tsHeight: int = 40
        tsX: int = 642
        tsY: int = 45
        return self.img[tsY:tsY + tsHeight, tsX:tsX + tsWidth]

    def getRound(self):
        rnumWidth:  int = 80
        rnumHeight: int = 20
        rnumX: int = 640
        rnumY: int = 85
        return self.img[rnumY:rnumY + rnumHeight, rnumX:rnumX + rnumWidth]

def validate_round_num(parsedround: str, maxRounds: int = 3) -> str:
    roundList: List[str] = []
    for i in range(1, maxRounds):
        roundList.append(f"ROUND {i}")
    return diff.get_close_matches(parsedround, roundList, 1)[0]

def find_closest_username(parsedname: str, usernames: List[str]) -> str:
    names = diff.get_close_matches(parsedname, usernames, 1)
    if len(names) > 0:
        return diff.get_close_matches(parsedname, usernames, 1)[0]

def get_usernames_from_csv(filename: str) -> List[str]:
    assert ".csv" in filename or ".txt" in filename
    userList: List[str] = []
    with open(filename) as file:
        usernames = csv.reader(file, delimiter=",")
        for row in usernames:
            userList.append(row[0])
    return userList

def main(filename: str, userfile: str, video: str) -> int:
    usernames: List[str] = get_usernames_from_csv(userfile)
    # TODO: add excel spreadsheet stuff
    # TODO: add logic to make sure the same kill is only added once
    vc = cv.VideoCapture(video)
    rv = 1
    counter = 0
    killCount = 0
    while rv:
        rv, img = vc.read()
        counter += 1
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 3, -3)
        killboxes: boxes = boxes(img)
        killimg = killboxes.getKiller(0)
        victimg = killboxes.getVictim(0)
        killer = pyte.image_to_string(killimg)
        victim = pyte.image_to_string(victimg)
        actualKiller = find_closest_username(killer, usernames)
        actualVictim = find_closest_username(victim, usernames)
        if actualKiller != None and actualVictim != None:
            killCount += 1
    print(killCount)

    # TODO: either save the image and insert it into the excel sheet directly or add some serious filtering
    cropped = killboxes.getTimestamp()
    cv.imshow("cropped", cropped)
    cv.waitKey()
    cropped = killboxes.getRound()
    cv.imshow("cropped", cropped)
    cv.waitKey()
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, help="image to open")
    parser.add_argument("-u", "--usernames", type=str, help="username file, csv or txt")
    parser.add_argument("-v", "--video", type=str, help="video filename, mp4 only")
    args = parser.parse_args()
    main(args.filename, args.usernames, args.video)