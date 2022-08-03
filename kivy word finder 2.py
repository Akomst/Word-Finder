from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from itertools import combinations
import json

with open('dictionary2.json', 'r') as f:
		words = json.load(f)

def Finder(letters):
	anagram = [ ]
	#words = open('Collins Scrabble Words (2019).txt') 
	#words = open('words_alpha.txt')
	for numb in range(3, len(letters) +1):
		perm = combinations(letters, numb)
		perm = set(''.join(sorted(i)) for i in perm)
		found_words = [word for word in words if len(word) == numb and  ''.join(sorted(word)) in perm]
		#for word in words:
			#word_list = word.lower()
			#word_list = word.rstrip()
			#if len(word) != numb:
				#continue
			#word_list = ''.join(sorted(word))
			#if word_list.lower() in perm:
			#if word_list in perm:
				#found_words.append(word)
		if found_words != []:
			anagram.append(found_words)
	return (anagram)

class Board(BoxLayout):
	
	def clear_press (self, clear_pressed):
		self.large_box.clear_widgets(children = None)
		self.txn.text = ''
		#self.txn1.text = ''
	
	def but_press(self, but_pressed):
		self.large_box.clear_widgets(children = None)
		press = Finder(self.txn.text)
		for words in press:
			labl = Label(text = ""+ str(len(words[0])) +" " + 'letter-words', text_size = (self.width, None))
			self.large_box.add_widget(labl)
			fr = GridLayout(cols = 5, size_hint_y = None, height = self.minimum_height)
			words = sorted(words)
			for word in words:
				but3 = Button(text = word,  background_color = [0, 1, 1, 0.5], on_press = self.brute)
				fr.add_widget(but3)
				
			self.large_box.add_widget(fr)
			
				
	def brute(self, instance):
	
		self.popup = Popup(title= instance.text, content= Label(text= words[instance.text], text_size = (450, 400)), size_hint=(None, None), size=(650, 800), auto_dismiss=True)
		
		self.popup.open()
				
	def __init__(self, **kwargs):
		super(Board, self).__init__(**kwargs)
		
		self.orientation = 'vertical'
		self.spacing = 10
		with self.canvas.before:
			Color(1, .7, 0.3, .41)
			self.rect = Rectangle(size=self.size, pos=self.pos)

		self.bind(size=self._update_rect, pos=self._update_rect)

	def _update_rect(self, instance, value):
		self.rect.pos = instance.pos
		self.rect.size = instance.size
		
	
		self.grid = GridLayout(cols = 3,size_hint_y = None)
		self.label_list = ['Input Letters', 'No. of Word Letters', '']
		for label in self.label_list:
			self.grid.add_widget(Label(text = label, color = [0,1,1,1]))
		self.txn = TextInput(text = '', multiline = False, background_color = [1,1,1,8], size_hint_y = None, height = 60)
		#self.txn1 = TextInput(text = '', multiline = False, background_color = [1,1,1,1])
		self.btn = Button (text = 'Find words', background_color = (0.2,1,.2,.9), size_hint_y = None, height =60)
		
		self.clear = Button(text = 'Clear', size_hint_y = None, background_color = [0,1,0,1])
		self.dropdown = DropDown()
		for i in range(len(self.txn.text)):
		 	btn = Button(text= str(i), size_hint_y=None, height = 60)
		 	btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
		 	self.dropdown.add_widget(btn)
		self.mainbutton = Button(text='find all', size_hint_y = None, height = 60)
		self.mainbutton.bind(on_release= self.dropdown.open)
		self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
		#self.title = getattr(btn, 'text')
		self.grid.add_widget(self.txn)
		self.grid.add_widget(self.mainbutton)
		self.grid.add_widget(self.btn)
		
		self.large_box = BoxLayout(orientation = 'vertical', size_hint_y = None, height = self.minimum_height, spacing = 30, padding = [15, 10,15,0])

		self.large_box.bind(minimum_height = self.large_box.setter('height'))
		
		self.scroll = ScrollView(effect_cls = 'ScrollEffect', bar_color = (1, 0, .5, .4))
		self.scroll.add_widget(self.large_box)
		
		self.tittle = Label(text = 'My Word Finder', size_hint_y = None, color = (0,1,0,1))
		
		self.add_widget(self.tittle, canvas = 'before')
		self.add_widget(self.grid)
		self.add_widget(self.scroll)
		self.add_widget(self.clear)
		
		self.btn.bind(on_press = self.but_press)
		self.clear.bind(on_press = self.clear_press)

class WordFinder(App):
    def build(self):
        return Board()

if __name__ == "__main__":
    WordFinder().run()