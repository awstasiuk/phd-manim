from manim import *


class CreateCircle(Scene):
    def construct(self):
        circ = Circle()
        circ.set_fill(PINK, opacity=0.5)
        self.play(Create(circ))


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount
        test = Text("High Alex")

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
        self.play(Create(test))
