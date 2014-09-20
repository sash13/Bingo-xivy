# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.utils import get_color_from_hex as C

font_s = '[font=PT Sans Narrow][size=18]'
font_e = '[/size][/font]'
game_data_path = 'game_data.csv'
text_choise = 'Выбрано: '
game_pole = 25

def get_fast(s):
    s = s.replace("\n", "\\n")
    return s[s.find('=18]')+len('=18]'):s.find('[/size]')]

class MainApp(App):

    def build(self):
        self.game_select = []
        self.games_index = {}
        self.index = [0]*game_pole
        self.game_end = 0
        self.game_buttons = []

        self.game_data = [[word for word in line.strip().split('|')] 
		 for line in open(game_data_path)]

        self.game_select = self.game_data[0][1:]
        self.root.ids.open_butt.text = text_choise + self.game_data[0][0]

        for idx, words in enumerate(self.game_data):
            word = words[0]
            self.games_index[word] = idx
            btn = Button(text = words[0],size_hint_y = None, height = '40dp')
            btn.bind(on_release=lambda btn:self.root.ids.drop.select(btn.text))
            self.root.ids.drop.add_widget(btn)

	for i in xrange(game_pole):
            btn = Factory.GameButton()
            btn.text = font_s + self.game_select[i].replace("\\n", "\n") + font_e
            btn.id = 'b' + str(i)
            self.game_buttons.append(btn)
            self.root.ids.nomad.add_widget(btn)

        self.update_button()

    def update_button(self):
        for i, btn in enumerate(self.game_buttons):
            btn.text = font_s + self.game_select[i].replace("\\n", "\n") + font_e

    def press(self, value):
        idx = self.game_select.index(get_fast(value.text))
 
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
		#self.root.ids.b13.color = [0, 0, 0, 1]
		self.game_buttons[12].background_color = [0.5, 0, 0, 1]
		self.root.ids.info_label.text = font_s + 'BINGO!' + font_e
		self.game_end = 0

    def reset(self):
        for btn in self.game_buttons:
            btn.background_color = C('#2ecc71')
            btn.color = [1, 1, 1, 1]
        self.index = [0]*game_pole
	self.root.ids.info_label.text = ''

    def drop_select(self, value):
        self.root.ids.open_butt.text = text_choise + value
        self.game_select = self.game_data[self.games_index[value]][1:]
        self.reset()
        self.update_button()


if __name__ in ('__main__', '__android__'):
    Config.set('graphics', 'width', '540')
    Config.set('graphics', 'height', '960')  # 9:16
    Config.set('graphics', 'resizable', '1')

    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    LabelBase.register(name='PT Sans Narrow',
                       fn_regular='PTN57F.ttf')
    MainApp().run()
