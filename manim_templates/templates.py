from manim import *
import manim
import funcy as f
from manim_slides import Slide

config.background_color = WHITE
def with_defaults(fun, default_kwargs):
    def fun_with_defaults(*args, **kwargs):
        return fun(*args, **f.merge(default_kwargs, kwargs))
    return fun_with_defaults


TexTable = with_defaults(Table, {
    "h_buff": 0.5,
    "v_buff": 0.3,
    "element_to_mobject": Tex,
    "arrange_in_grid_config": {
        "cell_alignment": LEFT,
    },
    "line_config": {
        "color": config.background_color
    },
})



def ParTex(tex, width=0.5, width_unit=r"\textwidth", **kwargs):
    """
    A Tex environment with automatic wrapping
    """
    return Tex(r"\parbox{" + str(width) + str(width_unit) + r"}{" + tex + "}",
               tex_environment="justify",
               **kwargs)


def annotate(objs, annotation: Mobject, color, position):
    mobjs = [obj.mobject
             if isinstance(obj, manim.mobject.mobject._AnimationBuilder) else obj
             for obj in objs]
    annotation.set_color(color).next_to(mobjs[0], position)
    arrows = [Arrow(annotation.get_top(),
                    mobj.get_bottom(),
                    buff=0.03,
                    stroke_width=2,
                    color=color,
                    tip_shape=StealthTip,
                    tip_length=0.2
                )
              for mobj in mobjs]
    annotation_group = Group(annotation, *arrows)
    return ([obj.add_background_rectangle(color=color, buff=0.03) for obj in objs],
            annotation_group)


class BaseSlide(Slide):
    def setup_slide(self, title, subtitle=None):
        mytemplate = TexTemplate(
            tex_compiler='xelatex',
            output_format='.xdv',
            preamble=r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fontspec}
\usepackage{ragged2e}
\setmainfont{Helvetica Neue}[
BoldFont = * Thin
]
            """)
        fg_color = BLACK
        Line.set_default(color=fg_color)
        Arrow.set_default(color=fg_color,
                          stroke_width=2,
                          tip_length=0.2)
        MathTex.set_default(color=fg_color,
            font_size=40
        )
        Tex.set_default(color=fg_color,
            font_size=40,
            tex_template=mytemplate
        )
        self.title = Tex(f"{{\\bf {title} }}", font_size=60).to_corner(UP + LEFT)
        self.add(self.title)
        if subtitle is not None:
            self.subtitle = (Tex(subtitle, font_size=30, color=GRAY)
                             .next_to(title, DOWN, buff=0.1)
                             .to_edge(LEFT, buff=0.5))
            self.play(FadeIn(self.subtitle, run_time=0.2))

    def play_animations(self, animations):
        for anim in animations:
            self.play(anim, run_time=0.5)
            self.next_slide()


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
        mytemplate = TexTemplate(tex_compiler='xelatex', output_format='.xdv')
        mytemplate.body = rf"""
    \documentclass[preview]{{standalone}}
    \usepackage[english]{{babel}}
    \usepackage{{amsmath}}
    \usepackage{{amssymb}}
    \usepackage{{fontspec}}
    \usepackage{{ragged2e}}
    \setmainfont{{Helvetica Neue}}[
    BoldFont = * Thin
    ]

    \begin{{document}}
     \parbox{{{page_width}}}{{
    \begin{{{itemize}}}
    YourTextHere
    \end{{{itemize}}}
        }}
    \end{{document}}
        """
        super().__init__(*args, tex_template=mytemplate, tex_environment=None, **kwargs)
