"""Calculating Vector of game (such as xDistance bird to pipe"""
from Parameters import *

class Vector:

    def distance( birdPosition, pipePosition, pipeHeight):
        topPosition = pipeHeight + pipePosition[1]
        horizontalDistance = pipePosition[0] - birdPosition[0]
        verticalDistance = topPosition - birdPosition[1]
        return horizontalDistance, verticalDistance