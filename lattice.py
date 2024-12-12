from manim import *
from manim import config


class SquareLattice(Scene):
    def construct(self):

        # Create horizontal lines
        horizontal_lines = VGroup()
        for y in range(-3, 4):
            line = Line(start=[-5, y, 0], end=[5, y, 0])
            line.z_index = 0
            horizontal_lines.add(line)

        self.play(*[Create(line) for line in horizontal_lines], run_time=1)

        # Create vertical lines
        vertical_lines = VGroup()
        for x in range(-5, 6):
            line = Line(start=[x, -3, 0], end=[x, 3, 0])
            line.z_index = 0
            vertical_lines.add(line)
        self.play(*[Create(line) for line in vertical_lines], run_time=1)

        # Create a grid of dots
        dots = VGroup()
        idx_lookup = {}
        idx = 0
        for x in range(-5, 6):
            for y in range(-3, 4):
                dot = Dot(point=[x, y, 0], radius=0.15, color=RED_A)
                dot.z_index = 1
                dots.add(dot)
                idx_lookup[(x, y, 0)] = idx
                idx += 1

        self.play(*[Create(dot) for dot in dots], run_time=1)

        # Highlight specific dots by causing them to glow
        glowing_dots = VGroup(dots[idx_lookup[(0, 0, 0)]], dots[idx_lookup[(3, 2, 0)]])

        # Replace their color with a darker red
        self.play(
            *[dot.animate.set_color(PURE_RED) for dot in glowing_dots], run_time=0.01
        )

        self.play(
            *[Indicate(dot, color=PURE_RED, scale_factor=1.5) for dot in glowing_dots],
            run_time=2
        )

        # Draw a dashed white line connecting the glowing dots
        dashed_line = DashedLine(
            start=glowing_dots[0].get_center(),
            end=glowing_dots[1].get_center(),
            color=WHITE,
        )
        self.play(Create(dashed_line), run_time=1)

        # Remove the dashed line
        self.play(FadeOut(dashed_line), run_time=1)

        def line_segment_highlight(chk_pts, dt=1):
            highlights = VGroup()
            for ptA, ptB in zip(chk_pts[0:-1], chk_pts[1:]):
                bold_line = Line(
                    start=ptA,
                    end=ptB,
                    color=BLUE_D,
                    stroke_width=8,
                )
                highlights.add(bold_line)
                self.play(Create(bold_line), run_time=dt, rate_function=linear)
            return highlights

        path1 = line_segment_highlight([[0, 0, 0], [3, 0, 0], [3, 2, 0]])
        self.play(FadeOut(path1))

        # Create a black box
        black_box1 = Rectangle(
            width=3.2,
            height=2.2,
            color=BLACK,
            fill_opacity=1,
            fill_color=BLACK,
        ).move_to([1.5, 1, 0])
        black_box1.z_index = 0
        # Add the black box to the scene
        self.play(Create(black_box1), run_time=1)
        self.play(Wait(), run_time=3)

        path2 = line_segment_highlight(
            [
                [0, 0, 0],
                [0, -1, 0],
                [3, -1, 0],
                [3, 0, 0],
                [4, 0, 0],
                [4, 2, 0],
                [3, 2, 0],
            ]
        )
        self.play(FadeOut(path2))
        self.play(FadeOut(black_box1))

        # Create a black box
        black_box2 = Rectangle(
            width=2.2,
            height=7.2,
            color=BLACK,
            fill_opacity=1,
            fill_color=BLACK,
        ).move_to([2, 0, 0])
        black_box2.z_index = 0
        # Add the black box to the scene
        self.play(Create(black_box2), run_time=2)
        self.play(Wait(), run_time=3)

        # Draw a dashed white line connecting the glowing dots
        dashed_line = DashedLine(
            start=glowing_dots[0].get_center(),
            end=glowing_dots[1].get_center(),
            color=WHITE,
        )
        self.play(Create(dashed_line), run_time=1)

        # Draw a red 'X' over the center of the dashed line
        center = dashed_line.get_center()
        x1 = Line(
            start=center + [-0.5, -0.5, 0],
            end=center + [0.5, 0.5, 0],
            color=RED,
            stroke_width=15,
        )
        x2 = Line(
            start=center + [-0.5, 0.5, 0],
            end=center + [0.5, -0.5, 0],
            color=RED,
            stroke_width=15,
        )
        red_x = VGroup(x1, x2)
        self.play(Create(red_x), run_time=1)

        # Remove the dashed line
        self.play(FadeOut(red_x), run_time=1)
        self.play(FadeOut(dashed_line), run_time=1)
