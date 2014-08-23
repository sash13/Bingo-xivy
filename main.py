# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button


texts = ["Деды \nвоевали", "Гейропа", "Бендеровцы", "Крымнаш", "Салоеды",
         "... не\nпоставить\nна колени", "Укропы", "Майданутые", "Чурки",
         "Мы\nпобедили", "Героям сала", "Пиндосы", "ПУТИН", "Госдеп",
         "Федера-\nлизация","Я помню,\nя горжусь", "Хунта", "Великая\nПобеда",
         "Порядок","Стабильность", "Жидо\nфашисты", "Обезьяна\nчерножопая",
         "Нацисты", "Загниваюшая\nЕвропа", "Великая\nРусь"]


class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        self.index = [0]*25;
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout
        
        self.layout = GridLayout(padding=20, cols=5, 
                            pos_hint={'center_y': 0.3})

        self.bingo = texts[12]
        for i in range(5*5):
            btn = Button(
                    text=texts[i],
                    size=(100, 100),
                    size_hint=(None, None),
                    #markup=True,
                    halign='center',
                    #color = [0,0,0,1],
                    #background_color = [1,1,1,1],
                    border = [20,20,20,20],
                    #background_normal = ""
                    #pos_hint={'center_x': .5, 'center_y': .5}
                    )

            btn.bind(on_press=self.callback)
            self.layout.add_widget(btn)
        btn = Button(
                text="Reset",
                halign='center',
                size=(150, 150), 
                pos_hint={'x': 0.36, 'center_y' : .1},
                size_hint=(None, None)
                #border = [16,16,16,16]
                )
        btn.bind(on_press=self.reset)

        self.add_widget(self.layout)
        self.add_widget(btn)
        
        #self.add_widget(rootLayout)

    def callback(self, value):
        if value.text is not self.bingo:
            value.background_color = [0,1,1,1]
            self.index[texts.index(value.text)] = 1
            
            line_x = [0] *5
            line_y = [0] *5
            ii = 0
            jj = 0

            for i in range(5):
                for j in range(5):
                    jj +=self.index[i*5+j]
                    ii +=self.index[j*5+i]
                 
                if ii is 5 or jj is 5:  #check v/h line
                    self.layout.children[12].background_color = [0,1,1,1]
                if i is 2:              
                    if ii is 4 or jj is 4: # check mediana
                        self.layout.children[12].background_color = [0,1,1,1]
                ii = 0
                jj = 0
            k = 0
            for i in range(5):
                ii+=self.index[i*5+k]
                jj+=self.index[4+i*5-k]
                k+=1

            if ii is 4 or jj is 4:    #check main diagonal
                self.layout.children[12].background_color = [0,1,1,1] 
                
    def reset(self, pok):
        for child in self.layout.children:
            child.background_color = [1,1,1,1]
            self.index = [0]*25


class MainApp(App):

    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ in ('__main__', '__android__'):
    Config.set('graphics', 'width', '540')
    Config.set('graphics', 'height', '960')  # 9:16
    Config.set('graphics', 'resizable', '1')
    
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    MainApp().run()
