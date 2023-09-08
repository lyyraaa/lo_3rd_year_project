import pyglet
from pyglet.window import key
from pyglet.gl import *
import math

import pyglet_gui
from pyglet_gui.theme import Theme
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton
from pyglet_gui.containers import VerticalContainer, HorizontalContainer, Spacer, GridContainer
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.gui import Label
from pyglet_gui.text_input import TextInput
from pyglet_gui.constants import ANCHOR_BOTTOM

from pyglet_gui.override import Label as Lbl

from colourdict import colourdict
import ca_dict

import numpy as np

import copy
import sys
import argparse

################################################################################
### Editor to quickly create cell layouts for the viewer program ###############
################################################################################

# Defining a new kind of button that makes up the editor panel
# This kind of button can take the color defined by the cell it represents
class ColourChangeButton(Button):
    def __init__(self, fontsize, colourdict,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fontsize = fontsize # This might need changing to scale better
        self.colourdict = colourdict
        self.colour = 0
        self.label = "0"

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        colourvec = self.colourdict.getColour(self.colour)
        colourvec = list(colourvec[:3])+[255,]

        self._button = theme['image'].generate(colourvec, **self.get_batch('background'))

        self._label = Lbl(self.label,
                            font_name=theme['font'],
                            font_size=self.fontsize,
                            color=theme['text_color'],
                            **self.get_batch('foreground'))


class WindowUI(pyglet.window.Window):

    def __init__(self, arglist, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.arglist = arglist

        self.batch = pyglet.graphics.Batch()

        self.theme = Theme(
            {"font": "Lucida Grande",
            "font_size": 12,
            "text_color": [255, 255, 255, 255],
            "gui_color": [255, 255, 255, 255],
            "button": {
                "text_color": [0, 0, 0, 255],
                "down": {
                    "image": {
                        "source": "editorbutton0-down.png",
                        "frame": [2,2,2,2],
                        "padding": [2,2,2,2]
                        },
                    },
                "up": {
                    "image": {
                        "source": "editorbutton0.png",
                        "frame": [2,2,2,2],
                        "padding": [2,2,2,2]
                        }
                    }
                },
                "input": {
                    "image": {
                        "source": "input.png",
                        "frame": [3, 3, 2, 2],
                        "padding": [3, 3, 2, 3]
                    },
                    # need a focus color
                    "focus_color": [255, 255, 255, 64],
                    "focus": {
                        "image": {
                            "source": "input-highlight.png"
                        }
                    }
                }
            }, resources_path='theme/')

        # Processes arguments to see if it needs to load a pattern,
        # or use some different set of colours
        # If there is a supplied CA to use, the colour dictionary for that CA is loaded
        # If there is a pattern supplied, then the editing_existing flag is set
        self.editing_existing = False
        if self.arglist.get("automata")[0] != "Default":
            if self.arglist.get("pattern")[0]:
                self.ca = CA_dict.get(self.arglist.get("automata")[0])("patterns/"+self.arglist.get("pattern")[0])
                self.editing_existing = True
            else:
                blankmap = np.full((*self.arglist.get("dimension"),1),[0,]).tolist()
                self.ca = CA_dict.get(self.arglist.get("automata")[0])(None)
            self.colourdict = colourdict(self.ca.get_colour_alias())
        else:
            self.ca = None
            self.colourdict = colourdict()


        # Setting the labels at the top
        if self.editing_existing:
            self.label_cells = Label('Cell Editor - editing '+self.arglist.get("pattern")[0])
        else:
            self.label_cells = Label('Cell Editor')
        self.ca_label = Label("Using CA: "+self.arglist.get("automata")[0])


        self.button_export = OneTimeButton(label="Export pattern", on_release=self.export_cells)
        # FOR TOGGLE BUTTONS USE Button not OneTimeButton, and on_release -> on_press

        # Taking parameters of how many rows and columns to create
        if self.editing_existing:
            self.rowC,self.colC = self.ca.getDimensions()
        elif self.arglist.get("dimension"):
            self.rowC,self.colC = self.arglist.get("dimension")
        else:
            self.rowC = self.colC = 10

        # setting up the array of buttons
        self.buttonarr = []
        self.setup_grid()

        self.container_buttons = GridContainer(self.buttonarr,padding=5)

        # Label of the current state, and the input to change current state
        self.colour_label = Label("")
        self.color_input = TextInput("0")

        if self.editing_existing:
            self.filename_input = TextInput(self.arglist.get("pattern")[0])
        else:
            self.filename_input = TextInput("exportfile.txt")

        self.manager = Manager(\
            content=VerticalContainer([Spacer(10),self.label_cells, Spacer(5), self.ca_label,Spacer(5),self.container_buttons, Spacer(40), self.button_export, Spacer(10), self.colour_label]),
            window=self,
            theme=self.theme,
            batch=self.batch,
            is_movable=False,
            offset=[0,120])

        # For some reason the text inputs require their own manager, else they crash
        # when interacted with.
        # I looked but could not find a reason nor solution, so unique managers for now
        self.manager_input_colour = Manager(\
            self.color_input,
            window=self,
            theme=self.theme,
            batch=self.batch,
            is_movable=False,
            anchor=ANCHOR_BOTTOM,
            offset=[0,120])

        self.manager_input_filename = Manager(\
            self.filename_input,
            window=self,
            theme=self.theme,
            batch=self.batch,
            is_movable=False,
            anchor=ANCHOR_BOTTOM,
            offset=[0,60])

    # Sets up an array of color change buttons
    def setup_grid(self):
        # unused font scaling thing
        #fontsize = int((1/6 * 900)/self.rowC + 5)
        fontsize = 10
        for row in range(self.rowC):
            buttonrow = []
            for col in range(self.colC):
                b = ColourChangeButton(fontsize, self.colourdict, on_press = self.change_col)
                buttonrow.append(b)
            self.buttonarr.append(buttonrow)

        # giving each button an attribute to remember where they are
        for row in range(self.rowC):
            for col in range(self.colC):
                self.buttonarr[row][col].row = row
                self.buttonarr[row][col].col = col
                if self.editing_existing:
                    self.buttonarr[row][col].colour = self.ca.init_cell_state((row,col))[0]
                    self.buttonarr[row][col].label = str(self.ca.init_cell_state((row,col))[0])


    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.update_colour_label()

    def update_colour_label(self):
        text = self.color_input.get_text()
        if self.ca and text:
            if text == "-1":
                self.colour_label.set_text("Wildcard")
            elif text.isdigit():
                self.colour_label.set_text(self.ca.getStatename(int(text)) if self.ca.getStatename(int(text)) else "State"+str(text))
            else:
                self.colour_label.set_text("Enter integer state or -1")

    # Changes the colour of a clicked button
    # It does this by the really ugly way of checking the entire button array for a pressed button
    # This is because it was seemingly impossible to call a function
    # while also passing the button who called it
    def change_col(self,x):
        for row in range(self.rowC):
            for col in range(self.colC):
                if self.buttonarr[row][col].is_pressed:
                    self.buttonarr[row][col].row = row
                    self.buttonarr[row][col].col = col
                    self.buttonarr[row][col].colour = int(self.color_input.get_text())
                    self.buttonarr[row][col].label = str(int(self.color_input.get_text()))
                    self.buttonarr[row][col].change_state() # This unpresses the button

    # Exports the current cell layout into a file
    def export_cells(self,is_pressed):
        buttonarr = []
        rowC = len(self.container_buttons.content)
        colC = len(self.container_buttons.content[0])
        outstr = str(rowC) + " " + str(colC) + "\n"
        for row in self.container_buttons.content:
            outstr += " ".join([str(button.colour) for button in row])
            outstr += "\n"

        f = open("patterns/"+self.filename_input.get_text(), "w")
        f.write(outstr)
        f.close()
        self.button_export.label = "Exported!"
        # Making sure the button goes back to normal, it had some issues otherwise,
        # since the label text changes on click
        self.button_export.change_state()
        self.button_export.change_state()



CA_dict = ca_dict.ca_dict

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="An editor to create and edit starting states for the cellular automata viewer")

    parser.add_argument("automata", metavar='A', type=str, nargs=1,
        choices=["Default"]+list(CA_dict.keys()),
        help="Cellular automata states and colours to use")
    parser.add_argument("-d","--dimension", nargs=2, type=int, default=[10,10],
        help="The number of rows,columns in pattern")
    parser.add_argument("-p","--pattern", type=str, nargs=1, default=[None],
        help="Existing pattern to edit, overrides -d dimensions")

    arglist = vars(parser.parse_args())

    windowUI = WindowUI(arglist, width=800, height=900, caption='UI',resizable=True)
    pyglet.app.run()
