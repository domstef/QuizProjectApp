from tkinter import *
from functools import partial
import html

import requests
from PIL import ImageTk, Image
from tkinter import font

BACKGROUND_COLOR = "#FAF3F0"
FONT = "#a77ecc" #"#DBC4F0"
GREEN = "#D4E2D4"
RED = "#FFCACC"

FONT_STYLE = "Helvetica"

class Quiz:

    def __init__(self):
        self.window = Tk()
        self.window.config(width=520, heigh=600, padx= 50, pady=50, bg = BACKGROUND_COLOR)
        self.num = 1

        self.score = 0


        self.title_canvas = Canvas(width=200,height=100, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.title = self.title_canvas.create_text(100, 50, text="Trivia Quiz", fill=FONT, font=(FONT_STYLE, 30, "italic"))
        self.title_canvas.grid(row=0, column=0)




        self.starting_screen()

        self.window.mainloop()


    def get_random_question(self):
        self.quiz_panel.itemconfig(self.question_num_text, text="Question {}/{}".format(self.num, self.radio_state.get()))

        self.change_color(BACKGROUND_COLOR)
        if self.num <= self.radio_state.get():
            response = requests.get(url="https://opentdb.com/api.php?amount=1&type=boolean")
            response.raise_for_status()
            data = response.json()['results'][0]
            self.correct_answer = 1 if data['correct_answer']=="True" else 0
            self.quiz_panel.itemconfig(self.question_text, text = html.unescape(data['question']))
        else:
            self.quiz_panel.itemconfig(self.question_num_text,
                                       text="".format(self.num, self.radio_state.get()))
            self.quiz_panel.itemconfig(self.question_text, text="You've got {}/{}!".format(self.score, self.radio_state.get()), font=(FONT_STYLE, 30, "italic"))


    def start_quiz(self):
        self.get_random_question()


    def verify_answer(self, answer):
        self.num += 1
        if self.correct_answer == answer:
            print("This is correct!")
            self.score += 1


            self.change_color(GREEN)
        else:
            print("This is wrong")
            self.change_color(RED)

        self.score_board.itemconfig(self.score_text, text="score: {}".format( self.score))
        self.window.after(500, self.get_random_question)


    def starting_screen(self):

        self.window.config(width=520, heigh=600, padx= 50, pady=50 )
        self.window.minsize(width=520, height=600)
        self.true_image = ImageTk.PhotoImage(Image.open("../images\\right_button.png").resize((50, 50)))
        self.false_image = ImageTk.PhotoImage(file=r"../images\\wrong_button.png")

        self.q_num_label = Canvas(width=200, height=100, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.q_num_label.create_text(100, 50, text="Number of questions:", fill=FONT, font=(FONT_STYLE, 14, "italic"))
        self.q_num_label.grid(row=1, column=0)
        self.radio_state = IntVar()

        self.q_num_button_10 = Radiobutton( text="10",value=10,indicatoron=0, variable=self.radio_state, font=(FONT_STYLE, 14, "italic"), image=self.true_image,
                                       compound= CENTER,   highlightthicknes=0, borderwidth=1, command=self.button, bg=BACKGROUND_COLOR)
        self.q_num_button_10.grid(row=1, column=2)
        self.q_num_button_10.invoke()

        self.q_num_button_20 = Radiobutton(text="20", value=20,indicatoron=0, variable=self.radio_state,font=(FONT_STYLE, 14, "italic"), image=self.true_image,
                                      compound=CENTER, highlightthicknes=0, borderwidth=1, command=self.button, bg=BACKGROUND_COLOR)
        self.q_num_button_20.grid(row=1, column=3)

        self.q_num_button_30 = Radiobutton(text="30", value=30,indicatoron=0, variable=self.radio_state,font=(FONT_STYLE, 14, "italic"), image=self.true_image,
                                      compound=CENTER, highlightthicknes=0, borderwidth=1, command=self.button, bg=BACKGROUND_COLOR)
        self.q_num_button_30.grid(row=1, column=4)

        self.start_image = ImageTk.PhotoImage(Image.open("../images\\right_button.png").resize((100, 50)))
        self.start_button = Button(text="Start!", font=(FONT_STYLE, 18, "italic"), image=self.start_image,
                                      compound=CENTER, highlightthicknes=0, borderwidth=0, command=self.quiz_window, bg=BACKGROUND_COLOR)
        self.start_button.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)


    def clear(self, root):
        list = root.grid_slaves()
        for l in list:
            l.destroy()

    def quiz_window(self):
        self.clear(self.window)
        self.start_button.destroy()
        #self.window = Tk()

        self.window.config(width=520, heigh=600, padx= 50, pady=50, bg = BACKGROUND_COLOR)

        self.title_canvas = Canvas(width=200, height=100, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.title = self.title_canvas.create_text(100, 50, text="Trivia Quiz", fill=FONT,
                                                   font=(FONT_STYLE, 30, "italic"))
        self.title_canvas.grid(row=0, column=0)
        self.score_board = Canvas(width=201, height=101, bg=BACKGROUND_COLOR, highlightthickness=0)
        img = Image.open("../images\score_board.png")
        self.score_image = ImageTk.PhotoImage(img.resize((100, 50)))
        self.score_board.create_image(150, 50, image=self.score_image)
        self.score_text = self.score_board.create_text(150,50, text="score: {}".format(self.score), fill=FONT, font =(FONT_STYLE, 15, "italic", "bold"))
        self.score_board.grid(row=0, column=1)

        self.quiz_panel = Canvas(width=405, height=305, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.panel_image = ImageTk.PhotoImage(Image.open("../images\panel_image.png"))
        self.quiz_panel.create_image(200.5, 150.5, image=self.panel_image)
        self.quiz_panel.grid(row=1, column=0, columnspan=2)
        self.question_text = self.quiz_panel.create_text(200.5, 150.5, width=400, text="", fill=FONT, font=20)
        self.question_num_text = self.quiz_panel.create_text(200.5, 50, anchor=N, width=400, text="", fill=FONT,
                                                             font=20)

        self.true_image = ImageTk.PhotoImage(Image.open("../images\\right_button.png"))
        self.false_image = ImageTk.PhotoImage(Image.open("../images\\wrong_button.png"))

        self.true_button = Button(image= self.true_image, bg=BACKGROUND_COLOR, highlightthicknes=0, borderwidth=0,
                                  command=partial(self.verify_answer, 1))
        self.true_button.grid(padx=50, pady=20, row=2, column=0)
        self.false_button = Button(image= self.false_image, bg=BACKGROUND_COLOR, highlightthicknes=0, borderwidth=0,
                                   command=partial(self.verify_answer, 0))
        self.false_button.config(padx=50, pady=100)
        self.false_button.grid(row=2, column=1)

        self.start_quiz()

    def button(self):
        print("A")





    def change_color(self, color):
        self.window.config(bg=color)
        self.quiz_panel.config(bg=color)
        self.title_canvas.config(bg=color)
        self.score_board.config(bg=color)
        self.false_button.config(bg=color)
        self.true_button.config(bg=color)
        print("Color {} changed".format(color))


Quiz()
