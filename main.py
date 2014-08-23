# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as C

texts = ["Деды \nвоевали", "Гейропа", "Бендеровцы", "Крымнаш", "Салоеды",
         "...не\nпоставить\nна колени", "Укропы", "Майданутые", "Чурки",
         "Мы\nпобедили", "Героям сала", "Пиндосы", "ПУТИН", "Госдеп",
         "Федера-\nлизация", "Я помню,\nя горжусь", "Хунта", "Великая\nПобеда",
         "Порядок", "Стабильность", "Жидо\nфашисты", "Обезьяна\nчерножопая",
         "Нацисты", "Загниваюшая\nЕвропа", "Великая\nРусь"]

class MainApp(App):

    def build(self):
        self.index = [0]*25
        self.bingo = texts[12]
        self.game_end = 0
        for (key, val) in self.root.ids.items():
            if key[0] == 'b':
		i = int(key.split('b')[-1])
		val.text = texts[i-1]


    def press(self, value):
        if value.text is not self.bingo:
            value.background_color = [0, 1, 1, 1]
            self.index[texts.index(value.text)] = 1

            ii = 0
            jj = 0

            for i in range(5):
                for j in range(5):
                    jj += self.index[i*5+j]
                    ii += self.index[j*5+i]

                if ii is 5 or jj is 5:  # check v/h line
                    self.root.ids.b13.background_color = [0, 1, 1, 1]
		    self.game_end = 1
                if i is 2:
                    if ii is 4 or jj is 4:  # check mediana
                        self.root.ids.b13.background_color = \
                            [0, 1, 1, 1]
			self.game_end = 1
                ii = 0
                jj = 0
            k = 0
            for i in range(5):
                ii += self.index[i*5+k]
                jj += self.index[4+i*5-k]
                k += 1

            if ii is 4 or jj is 4:  # check main diagonal
                self.root.ids.b13.background_color = [0, 1, 1, 1]
		self.game_end = 1
	    if self.game_end:
		self.root.ids.info_label.text = 'BINGO!'
		self.game_end = 0

    def reset(self):
        for (key, val) in self.root.ids.items():
            if key[0] == 'b':
                val.background_color = C('#2ecc71')
        self.index = [0]*25
	self.root.ids.info_label.text = ''

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ in ('__main__', '__android__'):
    Config.set('graphics', 'width', '540')
    Config.set('graphics', 'height', '960')  # 9:16
    Config.set('graphics', 'resizable', '1')

    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    MainApp().run()
