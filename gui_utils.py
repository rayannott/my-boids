from pygame import Color


WHITE = Color('#ffffff')
LIGHT_YELLOW = Color('#f7f2b9')
LIGHT_GREEN = Color('#81F45F')
LIGHT_PURPLE = Color('#915cfb')


class ColorGradient:
    def __init__(self, start_color: Color, end_color: Color):
        self.start_color = start_color
        self.end_color = end_color

    def __call__(self, percent: float) -> Color:
        percent = max(0., min(1., percent))
        return Color(
            int(self.start_color.r + (self.end_color.r - self.start_color.r) * percent),
            int(self.start_color.g + (self.end_color.g - self.start_color.g) * percent),
            int(self.start_color.b + (self.end_color.b - self.start_color.b) * percent),
            int(self.start_color.a + (self.end_color.a - self.start_color.a) * percent)
        )
