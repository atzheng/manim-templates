import os
from typing import Optional
from manim import *
import manim
import funcy as f
from manim_slides import Slide, ThreeDSlide


config.background_color = WHITE


def with_defaults(fun, default_kwargs):
    def fun_with_defaults(*args, **kwargs):
        return fun(*args, **f.merge(default_kwargs, kwargs))

    return fun_with_defaults


TexTable = with_defaults(
    Table,
    {
        "h_buff": 0.5,
        "v_buff": 0.3,
        "element_to_mobject": Tex,
        "arrange_in_grid_config": {
            "cell_alignment": LEFT,
        },
        "line_config": {"color": config.background_color},
    },
)


def ParTex(tex, width=0.5, width_unit=r"\textwidth", **kwargs):
    """
    A Tex environment with automatic wrapping
    """
    return Tex(
        r"\parbox{" + str(width) + str(width_unit) + r"}{" + tex + "}",
        tex_environment="justify",
        **kwargs,
    )


def annotate(objs, color, annotation: Optional[Mobject] = None, position=DOWN):
    mobjs = [
        obj.mobject if isinstance(obj, manim.mobject.mobject._AnimationBuilder) else obj
        for obj in objs
    ]
    rects = [obj.add_background_rectangle(color=color, buff=0.1) for obj in objs]
    if annotation is not None:
        annotation.set_color(color).next_to(mobjs[0], position)
        arrows = [
            Arrow(
                annotation.get_edge_center(-position),
                mobj.get_edge_center(position),
                buff=0.03,
                stroke_width=2,
                color=color,
                tip_shape=StealthTip,
                tip_length=0.2,
            )
            for mobj in mobjs
        ]
        annotation_group = Group(annotation, *arrows)
        return (rects, annotation_group)
    else:
        return rects


class BaseSlide(Slide):
    def setup_slide(self, title=None, subtitle=None):
        mytemplate = TexTemplate(
            tex_compiler="xelatex",
            output_format=".xdv",
            preamble=r"""
\usepackage[english]{babel}
\usepackage{xcolor}
\newcommand\red[1]{\color{red}#1}
\newcommand\blue[1]{\color{blue}#1}
\newcommand\green[1]{\color{green}#1}
% \newcommand[red][\color{red}]
% \newcommand[blue][\color{blue}]
% \newcommand[green][\color{green}]
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{varwidth}
\usepackage{fontspec}
\usepackage{ragged2e}
            """,
        )
        fg_color = BLACK
        Line.set_default(color=fg_color)
        Dot.set_default(color=fg_color)
        Arrow.set_default(color=fg_color, stroke_width=2, tip_length=0.2)
        MathTex.set_default(color=fg_color, font_size=40)
        Tex.set_default(color=fg_color, font_size=40, tex_template=mytemplate)
        if title is not None:
            self.title = Tex(f"{{\\bf {title} }}", font_size=50).to_corner(UP + LEFT)
        else:
            self.title = Mobject().to_corner(UP + LEFT)

        self.body = VGroup()
        self.left = VGroup()
        self.right = VGroup()

        if subtitle is not None:
            self.subtitle = (
                Tex(subtitle, font_size=30, color=GRAY)
                .next_to(title, DOWN, buff=0.1)
                .to_edge(LEFT, buff=0.5)
            )
            self.play(FadeIn(self.subtitle, run_time=0.2))

        self.is_first_animation = True

    def play_animations(self, animations):
        self.left.arrange(DOWN).next_to(self.title, DOWN).to_edge(LEFT)
        self.right.arrange(DOWN).next_to(self.title, DOWN).to_edge(RIGHT)
        self.body.arrange(DOWN).next_to(self.title, DOWN, buff=0.3)

        # Functionality for creating previews and condensing animations
        if os.environ.get("GRID", "FALSE") == "TRUE" and self.is_first_animation:
            c = NumberPlane().add_coordinates().fade(0.9)
            c.get_x_axis().numbers.set_color(BLACK)
            c.get_y_axis().numbers.set_color(BLACK)
            self.add(c)

        if self.is_first_animation:
            animations = [FadeIn(self.title)] + animations

        if os.environ.get("PREVIEW", "FALSE") == "TRUE":
            animations = [AnimationGroup(*animations)]

        self.next_slide()

        if len(animations) >= 1:
            for anim in animations[:-1]:
                # if not (isinstance(anim, list) or isinstance(anim, tuple)):
                #     anim = [anim]
                self.play(anim, run_time=0.5)
                self.wait(0.1)
                self.next_slide()


            self.play(animations[-1], run_time=0.5)

        if self.is_first_animation:
            self.is_first_animation = False

        self.wait(1)


class BaseThreeDSlide(ThreeDSlide):
    def setup_slide(self, title=None, subtitle=None):
        mytemplate = TexTemplate(
            tex_compiler="xelatex",
            output_format=".xdv",
            preamble=r"""
\usepackage[english]{babel}
\usepackage{xcolor}
\newcommand\red[1]{\color{red}#1}
\newcommand\blue[1]{\color{blue}#1}
\newcommand\green[1]{\color{green}#1}
% \newcommand[red][\color{red}]
% \newcommand[blue][\color{blue}]
% \newcommand[green][\color{green}]
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{varwidth}
\usepackage{fontspec}
\usepackage{ragged2e}
            """,
        )
        fg_color = BLACK
        Line.set_default(color=fg_color)
        Dot.set_default(color=fg_color)
        Arrow.set_default(color=fg_color, stroke_width=2, tip_length=0.2)
        MathTex.set_default(color=fg_color, font_size=40)
        Tex.set_default(color=fg_color, font_size=40, tex_template=mytemplate)
        if title is not None:
            self.title = Tex(f"{{\\bf {title} }}", font_size=50).to_corner(UP + LEFT)
            self.play(FadeIn(self.title))
        else:
            self.title = Mobject().to_corner(UP + LEFT)

        self.body = VGroup()
        self.left = VGroup()
        self.right = VGroup()

        if subtitle is not None:
            self.subtitle = (
                Tex(subtitle, font_size=30, color=GRAY)
                .next_to(title, DOWN, buff=0.1)
                .to_edge(LEFT, buff=0.5)
            )
            self.play(FadeIn(self.subtitle, run_time=0.2))

    def play_animations(self, animations):
        self.left.arrange(DOWN).next_to(self.title, DOWN).to_edge(LEFT)
        self.right.arrange(DOWN).next_to(self.title, DOWN).to_edge(RIGHT)
        self.body.arrange(DOWN).next_to(self.title, DOWN, buff=0.3)
        for anim in animations:
            self.wait(0.1)
            if not (isinstance(anim, list) or isinstance(anim, tuple)):
                anim = [anim]
            self.next_slide()
            self.play(*anim, run_time=0.2)
        self.wait(1)


class LatexItems(Tex):
    def __init__(self, *args, page_width=r"0.5\textwidth", itemize="itemize", **kwargs):
        """
        https://gist.github.com/abul4fia/475577ef58e4cd3babc2028be7f960fa

        *args is a sequence of strings to be typeset by latex. The expected usage is that
           each of these strings starts by r"\item "

        page_width is the width of the minipage in which the environment will be typeset
           it is recommended to use "em" as unit (being 1em the width of letter m)

        itemize is the environment to use. It can be "itemize", "enumerate" or "description"
           The last one requires each item to be followed by the term to be defined in
           square brackets, eg: r"\item[Foo] this is a foo"

        EXAMPLE:

            items = LatexItems(r"\item Foo", r"\item Bar", r"\item Foobar")
            for item in items:
               self.play(Write(item))
        """
        mytemplate = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
        # \setmainfont{{Helvetica Neue}}[
        #   UprightFont=* Thin,
        #   BoldFont = * Medium
        # ]
        mytemplate.body = rf"""
    \documentclass[preview]{{standalone}}
    \usepackage[english]{{babel}}
    \usepackage{{amsmath}}
    \usepackage{{amssymb}}
    \usepackage{{fontspec}}
    \usepackage{{ragged2e}}
    \usepackage{{xcolor}}

    \begin{{document}}
     \parbox{{{page_width}}}{{
    \begin{{{itemize}}}
    YourTextHere
    \end{{{itemize}}}
        }}
    \end{{document}}
        """
        super().__init__(*args, tex_template=mytemplate, tex_environment=None, **kwargs)


class TexItems(LatexItems):
    pass
