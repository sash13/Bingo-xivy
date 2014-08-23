# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex as C

texts = ["Деды \nвоевали", "Гейропа", "Бендеровцы", "Крымнаш", "Салоеды",
         "...не\nпоставить\nна колени", "Укропы", "Майданутые", "Чурки",
         "Мы\nпобедили", "Героям сала", "Пиндосы", "ПУТИН", "Госдеп",
         "Федера-\nлизация", "Я помню,\nя горжусь", "Хунта", "Великая\nПобеда",
         "Порядок", "Стабильность", "Жидо\nфашисты", "Обезьяна\nчерножопая",
         "Нацисты", "Загниваюшая\nЕвропа", "Великая\nРусь"]

font_s = '[font=PT Sans Narrow][size=18]'
font_e = '[/size][/font]'

def get_fast(s):
    return s[s.find('=18]')+len('=18]'):s.find('[/size]')]

class MainApp(App):

    def build(self):
        self.index = [0]*25
        self.game_end = 0
        for (key, val) in self.root.ids.items():
            if key[0] == 'b':
		i = int(key.split('b')[-1])
		val.text = font_s + texts[i-1] + font_e


    def press(self, value):
        idx = texts.index(get_fast(value.text))
 
        if idx is not 12:
            value.background_color = [0, 1, 1, 1]
            value.color = [0, 0, 0, 1]
            self.index[idx] = 1

            ii = 0
            jj = 0

            for i in range(5):
                for j in range(5):
                    jj += self.index[i*5+j]
                    ii += self.index[j*5+i]

                if ii is 5 or jj is 5:  # check v/h line
		    self.game_end = 1
                if i is 2:
                    if ii is 4 or jj is 4:  # check mediana
			self.game_end = 1
                ii = 0
                jj = 0
            k = 0
            for i in range(5):
                ii += self.index[i*5+k]
                jj += self.index[4+i*5-k]
                k += 1

            if ii is 4 or jj is 4:  # check main diagonal
		self.game_end = 1
	    if self.game_end:
		self.root.ids.b13.color = [0, 0, 0, 1]
		self.root.ids.b13.background_color = [0, 1, 1, 1]
		self.root.ids.info_label.text = font_s + 'BINGO!' + font_e
		self.game_end = 0

    def reset(self):
        for (key, val) in self.root.ids.items():
            if key[0] == 'b':
                val.background_color = C('#2ecc71')
                val.color = [1, 1, 1, 1]
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
    LabelBase.register(name='PT Sans Narrow',
                       fn_regular='PTN57F.ttf')
    MainApp().run()
