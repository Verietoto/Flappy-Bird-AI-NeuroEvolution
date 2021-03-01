"""
Class where bird is controlled, drawing to screen, bird movement, etc is setting up here
"""

from Parameters import *

class Bird:
    def __init__(self):
        ## Setting Animation position of bird
        self.birdAnimation = 0

        ## Initial Bird Position
        self.birdPosition = BirdPosition

        ## Loading Bird Images
        self.birdImages = [pygame.image.load("assets/images/bird1.png"),
                           pygame.image.load("assets/images/bird2.png"),
                           pygame.image.load("assets/images/bird3.png")]
        self.birdStay = pygame.image.load("assets/images/bird2.png")

        ## fallVelocity and rotation degree is a function of time
        self.time = 0
        self.degree = 0
        self.fallVelocity = 0

    def rotate(self, bird,degree):
        """

        :param bird: bird image
        :param degree: how many the image will be rotated
        :return:
        """
        bird = pygame.transform.rotate(bird,degree)
        return bird

    def neuralNetworkJump(self, feedForward):
        """
        Taking action from neural network output
        :param feedForward: Output of feedforward neural network [value1, value2]
        :return:
        """
        action = np.argmax(feedForward)

        if action == 0:
            pass
        elif action == 1:
            self.fallVelocity = -10
            self.time = 0
            self.degree = 40

    def jump(self, key):
        """
        Jumping function
        :param key:
        :return:
        """
        if key == pygame.K_SPACE:
            self.fallVelocity = -10
            self.time = 0
            self.degree = 40

    def movement(self):
        """Setting up for bird movement"""
        self.time +=1
        self.fallVelocity = self.fallVelocity + GRAVITATION*self.time
        self.degree = self.degree - 2*GRAVITATION*self.time
        if self.fallVelocity > 15 and self.fallVelocity != 100:
            self.fallVelocity = 15
        if self.degree <= -90:
            self.degree = -90
        self.birdPosition = (self.birdPosition[0],self.birdPosition[1]+self.fallVelocity)
        if self.birdPosition[1] <= 0:
            self.birdPosition = (self.birdPosition[0], 0)


    def drawBIrd(self, screen):
        """
        Draw Bird on Screen
        :param screen: Which sceen will images going to be drawn
        :return:
        """
        bird = self.birdImages[int(self.birdAnimation)]
        bird = self.rotate(bird,self.degree)
        screen.blit(bird, self.birdPosition)

        self.birdAnimation +=0.4

        if self.birdAnimation > 2:
            self.birdAnimation=0