
from kivy.lang import Builder
from kivymd.tools.hotreload.app import MDApp


class HotReload(MDApp):

    ARQUIVOS_KV = ['testeHotReload.kv']
    DEBUG = True

    def build_app(self):
        return Builder.load_file('testeHotReload.kv')


HotReload().run()
