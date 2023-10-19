# Allowable libraries:
# - Python 3.10.12
# - Pillow 10.0.0
# - numpy 1.25.2
# - OpenCV 4.6.0 (with opencv-contrib-python-headless 4.6.0.66)

# To activate image processing, uncomment the following imports:
from PIL import Image
import numpy as np
import time
import cv2

class Agent:
    def __init__(self):
        self.problemFigures = {}
        """
        The default constructor for your Agent. Make sure to execute any processing necessary before your Agent starts
        solving problems here. Do not add any variables to this signature; they will not be used by main().
        """
        pass

    def reflect(self, imA, imB):
        reflectedImageA = imA.transpose(Image.FLIP_LEFT_RIGHT)

        # reflectedImageA.show()
        # imB.show()
        equalImages = self.equal(reflectedImageA, imB)
        # print("reflected: ", equalImages)
        if equalImages < 6:
            return True
        else:
            return False

    def verticalReflect(self, im1, im2):
        reflectedImage1 = im1.transpose(Image.FLIP_TOP_BOTTOM)

        # reflectedImage1.show()
        # im2.show()
        equalImages = self.equal(reflectedImage1, im2)
        print("verticalReflect: ", equalImages)
        if equalImages < 6:
            return True
        else:
            return False

    def rotate(self, imageA, imageB):

        # read the image
        # rotate image by 45,90,180,270 degrees
        degrees = [90, 180, 270]
        # degrees = [-90,-180,-270]
        # rotatedImageA = imageA.rotate(360)
        # isEqual = self.equal(rotatedImageA, imageA)
        # print("compare A to rotated A: ", isEqual)
        for degree in degrees:
            counterClockwiseRotatedImageA = imageA.rotate(degree)
        # if degree == 270:
        # counterClockwiseRotatedImageA.show()
        # imageB.show()
        equal = self.equal(counterClockwiseRotatedImageA, imageB)
        # print("degree,equal: ", degree,equal)
        if equal < 17:
            return degree
        return ""

    def equal(self, imageA, imageB):
        # Load images, convert to RGB, then to numpy arrays and ravel into long, flat things
        a = np.array(imageA.convert('RGB')).ravel()
        b = np.array(imageB.convert('RGB')).ravel()
        # Calculate the sum of the absolute differences divided by number of elements
        MAE = np.sum(np.abs(np.subtract(a, b, dtype=np.float))) / a.shape[0]
        return MAE

    def compare(self, imageA, imageB):
        imA = Image.open(imageA)
        imB = Image.open(imageB)
        # Check if imageA and imageB are the same
        equalImages = self.equal(imA, imB)
        if equalImages == 0.0:
            return "unchanged", ""
        # Check if imageA and imageB are reflected horizontal
        isReflected = self.reflect(imA, imB)
        if isReflected:
            return "reflected", ""
        # Check if imageA and imageB are reflected vertically
        isVerticallyReflected = self.verticalReflect(imA, imB)
        if isVerticallyReflected:
            return "vertically-reflected", ""

        # Check if imageA and imageB are rotated
        degree = self.rotate(imA, imB)
        if degree != "":
            return "rotated", degree
        else:
            return "", ""

    def chooseImageFromSet(self, result, degree, imageClassPath):
        imageSet = ["1", "2", "3", "4", "5", "6"]

        if result == "unchanged":
            for imageNum in imageSet:
                imagePath = self.problemFigures[imageNum].visualFilename
                if self.equal(Image.open(imageClassPath), Image.open(imagePath)) == 0.0:
                    return int(imageNum)
        elif result == "reflected":
            for imageNum in imageSet:
                imageNumPath = self.problemFigures[imageNum].visualFilename
                imageC = Image.open(imageClassPath)
                imageCReflected = imageC.transpose(Image.FLIP_LEFT_RIGHT)
                similarityNum = self.equal(imageCReflected, Image.open(imageNumPath))
                # print("** similarityNum: ", similarityNum)
                # print("** imageNum: ", imageNum)
                if similarityNum < 6:
                    return int(imageNum)
        elif result == "vertically-reflected":
            # print("chooseImageFromSet: vertically-reflected")
            for imageNum in imageSet:
                imageNumPath = self.problemFigures[imageNum].visualFilename
                imageB = Image.open(imageClassPath)
                imageCReflected = imageB.transpose(Image.FLIP_TOP_BOTTOM)
                similarityNum = self.equal(imageCReflected, Image.open(imageNumPath))
                # print("** similarityNum: ", similarityNum)
                # print("** imageNum: ", imageNum)
                if similarityNum < 6:
                    return int(imageNum)
        elif result == "rotated":
            for imageNum in imageSet:
                imageNumPath = self.problemFigures[imageNum].visualFilename
                imageC = Image.open(imageClassPath)
                # print("degree: ", degree)
                rotatedImageC = imageC.rotate(degree)
                if self.equal(rotatedImageC, Image.open(imageNumPath)) < 17:
                    return int(imageNum)
        return 1

    def Solve(self, problem):
        """
        Primary method for solving incoming Raven's Progressive Matrices.

        Args:
            problem: The problem instance.

        Returns:
            int: The answer (1 to 6). Return a negative number to skip a problem.
            Remember to return the answer [Key], not the name, as the ANSWERS ARE SHUFFLED.
            DO NOT use absolute file pathing to open files.
        """

        # Example: Preprocess the 'A' figure from the problem.
        # Actual solution logic needs to be implemented.
        # image_a = self.preprocess_image(problem.figures["A"].visualFilename)

        # Placeholder: Skip all problems for now.
        if problem.problemType == "2x2":
            start = time.time()
            if problem.name != "Basic Problem B99-05":
                print("\n")
                print("problem.name: ", problem.name)
                print("problem.problemSetName: ", problem.problemSetName)
                self.problemFigures = problem.figures
                image_A = self.problemFigures["A"].visualFilename
                image_B = self.problemFigures["B"].visualFilename
                image_C = self.problemFigures["C"].visualFilename
                results, r = self.compare(image_A, image_B)
                # results is one of ["unchanged", "reflected", "rotated"]
                print("results, r: ", results, r)
                if results != "":
                    imageNum = self.chooseImageFromSet(results, r, image_C)
                    print("imageNum: ", imageNum)
                    end = time.time()
                    print("endtime: ", end - start)
                    return imageNum
                else:
                    ac_results, ac_r = self.compare(image_A, image_C)
                    # print("ac_results, ac_r: ", ac_results, ac_r)
                    imageNum = self.chooseImageFromSet(ac_results, ac_r, image_B)
                    end = time.time()
                    print("endtime: ", end - start)
                    return imageNum
        return 1

