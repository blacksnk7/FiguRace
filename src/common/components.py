import PySimpleGUI as sg

class Styles:
    """general styles for components"""
    def __init__(self):
        self.font = "Verdana"
        self.padding = ((0, 0),(0, 8))
        self.sizes = {
            "sm": (22, 2),
            "md": (18, 2),
            "lg": (20, 2)
        }
        self.font_sizes = {
            "sm": "10",
            "md": "13",
            "lg": "14",
            "xl": "20"
        }
    def get_font(self, size):
        return self.font + " " + self.font_sizes[size]
    
    def set_font_sizes(self, new):
        self.font_sizes = new
        
    def get_size(self, size):
        return self.sizes[size]
styles =  Styles()

class Button(sg.Button):
    """custom Button component with positional shortcuts, size, applied styles and same properties as sg Button"""
    def __init__(self, text="", key=None, size="md", **kwargs):
        super().__init__(key=key, size=styles.get_size(size), button_text=text, font=styles.get_font(size), pad=styles.padding, **kwargs)

class Text(sg.Text):
    """custom Text component with positional shortcuts, size, applied styles and same properties as sg Text"""
    def __init__(self, text="", key=None, size="md", font="", width=(None, None), **kwargs):
        styles = Styles()
        styles.set_font_sizes({
            "sm": "12",
            "md": "16",
            "lg": "18",
            "xl": "20"
        })
        super().__init__(text, key=key, font= (font if font else styles.get_font(size)), size=width, **kwargs)
        
class Input(sg.Input):
    """custom Input component with positional shortcuts, size, applied styles and same properties as sg Input"""
    def __init__(self, text="", key=None, size="md", font="", **kwargs):
        super().__init__(text, key=key, font= (font if font else styles.get_font(size)), enable_events=True, size=styles.get_size(size), **kwargs)
    

class Combo(sg.Combo):
    """custom Combo component with positional shortcuts, size, applied styles and same properties as sg Combo"""
    def __init__(self, values=[], key=None, size="md", readonly=True, default_value="", **kwargs):
        super().__init__(values, default_value=default_value or values[0] if len(values) > 0 else None, key=key, readonly=readonly, enable_events=True, font=styles.get_font(size), size=(16, 6), expand_y=True, **kwargs)

class Title(list):
    """Title component, its a page Heading and returns and already centered list with the text inside"""

    def __init__(self, text=""):
        super().__init__()
        self.append(sg.Push())
        self.append(Text(text, font=(styles.get_font("xl") + " " + "underline"), pad=((0,0),(0, 30))))
        self.append(sg.Push())

class Column(sg.Column):
    """custom Column component with positional shortcuts, applied styles and has the same properties as sg.Column"""
    def __init__(self, elements, justification="left", **kwargs):
        super().__init__([el if isinstance(el, list) else [el]for el in elements],  expand_x=True, element_justification=justification, p=(64, 0), vertical_alignment="top", **kwargs)

class Slider(sg.Slider):
    """custom Slider component with positional shortcuts, applied styles and has the same properties as sg.Slider"""
    def __init__(self, value=10, key=None, default=1, **kwargs):
        super().__init__(range=value if type(value) is tuple else (1, value), default_value=default, key=key, orientation='horizontal', font=styles.get_font("sm") ,size=(22, 18), **kwargs)
        
