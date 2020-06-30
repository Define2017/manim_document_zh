from manimlib.constants import *
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import Rectangle
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.color import Color
from manimlib.utils.config_ops import digest_config


class SurroundingRectangle(Rectangle):
    """环绕矩形"""
    CONFIG = {
        "color": YELLOW,
        "buff": SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        """传入 ``mobject`` 为环绕的物体"""
        digest_config(self, kwargs)
        kwargs["width"] = mobject.get_width() + 2 * self.buff
        kwargs["height"] = mobject.get_height() + 2 * self.buff
        Rectangle.__init__(self, **kwargs)
        self.move_to(mobject)


class BackgroundRectangle(SurroundingRectangle):
    """背景矩形"""
    CONFIG = {
        "color": BLACK,
        "stroke_width": 0,
        "stroke_opacity": 0,
        "fill_opacity": 0.75,
        "buff": 0
    }

    def __init__(self, mobject, **kwargs):
        """传入 ``mobject`` 为需要添加背景的物体"""
        SurroundingRectangle.__init__(self, mobject, **kwargs)
        self.original_fill_opacity = self.fill_opacity

    def pointwise_become_partial(self, mobject, a, b):
        self.set_fill(opacity=b * self.original_fill_opacity)
        return self

    def set_style_data(self,
                       stroke_color=None,
                       stroke_width=None,
                       fill_color=None,
                       fill_opacity=None,
                       family=True
                       ):
        """除了不透明度，其余不可以更改（初始化时除外）"""
        VMobject.set_style_data(
            self,
            stroke_color=BLACK,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=fill_opacity
        )
        return self

    def get_fill_color(self):
        return Color(self.color)


class Cross(VGroup):
    """交叉错号"""
    CONFIG = {
        "stroke_color": RED,
        "stroke_width": 6,
    }

    def __init__(self, mobject, **kwargs):
        """传入的 ``mobject`` 为要打错号的物体"""
        VGroup.__init__(self,
                        Line(UP + LEFT, DOWN + RIGHT),
                        Line(UP + RIGHT, DOWN + LEFT),
                        )
        self.replace(mobject, stretch=True)
        self.set_stroke(self.stroke_color, self.stroke_width)


class Underline(Line):
    """下划线"""
    CONFIG = {
        "buff": SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        """传入的 ``mobject`` 为需要下划线的物体"""
        super().__init__(LEFT, RIGHT)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)