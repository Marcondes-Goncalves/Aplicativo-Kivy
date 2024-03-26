from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior

class ImageButton(ButtonBehavior, Image):
    """Classe personalizada

    Desc:
        Esta classe herda da ButtonBehavior e Label e isso é suficiente para transformar uma Imagem em um botão
    """
    pass


class LabelButton(ButtonBehavior, Label):
    """Classe personalizada

    Desc:
        Esta classe herda da ButtonBehavior e Label e isso é suficiente para transformar um Label em um botão
    """
    pass

