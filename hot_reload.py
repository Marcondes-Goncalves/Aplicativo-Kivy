
from kivy.lang import Builder
from kivymd.tools.hotreload.app import MDApp


class HotReload(MDApp):

    ARQUIVOS_KV = ['testeHotReload.kv']
    DEBUG = True

    def build_app(self): # type: ignore[Unknown]
        return Builder.load_file('testeHotReload.kv')


HotReload().run()
