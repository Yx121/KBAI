# Allowable libraries:
# - Python 3.10.12
# - Pillow 10.0.0
# - numpy 1.25.2
# - OpenCV 4.6.0 (with opencv-contrib-python-headless 4.6.0.66)

# To activate image processing, uncomment the following imports:
from PIL import Image, ImageOps
import numpy as np
from random import randint


def matrix_image(image):
    return np.array(image).clip(max=1)


def get_statistics(train_imgA, train_imgB):
    compare_array = np.equal(train_imgA, train_imgB).astype(np.uint8)
    mean = np.mean(compare_array)
    rms = np.sqrt(np.mean(np.square(train_imgA - train_imgB)))
    return mean > 0.97, mean, rms


def similarity_2x2(answers_dict, train_imgA, train_imgB, test_imgA):
    answer = -1
    target_diff = 1
    similar_train, mean_train, _ = get_statistics(train_imgA, train_imgB)
    if similar_train:
        for key, test_imgB in answers_dict.items():
            similar_test, mean_test, _ = get_statistics(test_imgA, test_imgB)
            if similar_test and abs(mean_test - mean_train) < target_diff:
                target_diff = abs(mean_test - mean_train)
                answer = int(key)
    return answer


def transform_images(image_dict):
    transformed_images = []
    for operation, prefix in [('mirror', 'h'), ('flip', 'v')]:
        for img in ['A', 'B', 'C']:
            transformed_images.append(matrix_image(getattr(ImageOps, operation)(image_dict[img])))
    return transformed_images


class Agent:

    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        """
        The default constructor for your Agent. Make sure to execute any processing necessary before your Agent starts
        solving problems here. Do not add any variables to this signature; they will not be used by main().
        """
        pass

    def solution2x2(self, problem):
        answer = -1
        image_dict = {name: Image.open(problem.figures[name].visualFilename) for name in
                      ['A', 'B', 'C', '1', '2', '3', '4', '5', '6']}
        image_matrix_dict = {name: matrix_image(image) for name, image in image_dict.items()}
        answers_dict = {k: v for k, v in image_matrix_dict.items() if k in ['1', '2', '3', '4', '5', '6']}

        h_mirror_A, h_mirror_B, h_mirror_C, v_mirror_A, v_mirror_B, v_mirror_C  = transform_images(image_dict)

        if answer == -1:
            answer = similarity_2x2(answers_dict, image_matrix_dict['A'], image_matrix_dict['B'],
                                    image_matrix_dict['C'])  # A&B
        if answer == -1:
            answer = similarity_2x2(answers_dict, image_matrix_dict['A'], image_matrix_dict['C'],
                                    image_matrix_dict['B'])  # A&C
        if answer == -1:
            answer = similarity_2x2(answers_dict, h_mirror_A, image_matrix_dict['B'], h_mirror_C)  # -A & B
        if answer == -1:
            answer = similarity_2x2(answers_dict, h_mirror_A, image_matrix_dict['C'], h_mirror_B)  # -A & C
        if answer == -1:
            answer = similarity_2x2(answers_dict, v_mirror_A, image_matrix_dict['B'], v_mirror_C)  # |A & B
        if answer == -1:
            answer = similarity_2x2(answers_dict, v_mirror_A, image_matrix_dict['C'], v_mirror_B)  # |A & C

        if answer == -1:  # Rotation
            background = Image.new('RGBA', image_dict['A'].size, 'white')

            for angle in [45, 90, 135, 180, 225, 270, 315]:
                ra = image_dict['A'].rotate(angle)
                rb = image_dict['B'].rotate(angle)
                rc = image_dict['C'].rotate(angle)

                rotateA = matrix_image(Image.composite(ra, background, ra))
                rotateB = matrix_image(Image.composite(rb, background, rb))
                rotateC = matrix_image(Image.composite(rc, background, rc))

                if answer == -1:  # A horizontal mirror B
                    answer = similarity_2x2(answers_dict, rotateA, image_matrix_dict['B'], rotateC)
                if answer == -1:  # A horizontal mirror C
                    answer = similarity_2x2(answers_dict, rotateA, image_matrix_dict['C'], rotateB)
                if answer > 0:
                    break
        if answer == -1:
            answer = randint(1, 6)

        return answer

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

        if problem.problemType == '2x2':
            answer = self.solution2x2(problem)

        else:
            answer = -1
        return answer


