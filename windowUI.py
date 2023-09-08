import pyglet
from pyglet.window import key
from pyglet.gl import *
import math

import pyglet_gui
from pyglet_gui.theme import Theme
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, GroupButton
from pyglet_gui.containers import VerticalContainer, HorizontalContainer, Spacer
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.constants import HALIGN_LEFT, HALIGN_CENTER, VALIGN_CENTER,ANCHOR_TOP_LEFT
from pyglet_gui.gui import Label

# Necessary for opening a file dialog to select pattern files
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
# Prevents window from being drawn
root.withdraw()

import os

from projecttheme import projecttheme

from automata.cellloader import CellLoader


################################################################################
### Window UI class, holds the controls for changing the view of the model #####
################################################################################

# Window class for the UI
class WindowUI(pyglet.window.Window):

    def __init__(self, window3D, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Holds a reference to the window for the model, so the model variables can be accessed
        self.window3D = window3D

        # A single batch holding all the UI elements
        self.batch = pyglet.graphics.Batch()

        # Theme JSON describes the style for pyglet-gui elements
        self.theme = Theme(*projecttheme)

        # I cant really explain any reason why some UI elements I define as class variables and some not
        # Only the ones needing to be changed later are necessary to do so for
        # Setting up labels for cellular automaton details
        label_CAdt = Label('CA Details',bold=True)
        label_ca_type = Label("CA Type: "+self.window3D.model.ca.name)
        label_dimensions = Label("Dimensions: "+str(self.window3D.model.dimensions))
        label_evolutions = Label("Evolutions: "+str(self.window3D.model.evolution_steps))
        label_neighborhoods = Label(f"Unique neighborhoods: {self.window3D.model.neighborhood_count}")
        blank_label = Label("")
        label_observed = Label("Observed state:")
        self.label_observed_state = Label("None ")

        self.selected_rowcount_label = Label("Rows selected: 0")
        self.selected_colcount_label = Label("Columns selected: 0")
        self.selected_rackcount_label = Label("Racks selected: 0")
        self.selected_total_label = Label("Cells selected: 0")

        # Setting up objects for changing the time window displayed
        self.label_timeslice = Label("Displayed steps: "+str(0)+" - "+str(self.window3D.model.evolution_steps-1))
        self.button_timeslice = OneTimeButton('Select time window', on_release=self.timeslice)
        # Sliders can take any integer value from 0 to number of steps -1
        self.slider_start = HorizontalSlider(value=0, min_value=0, max_value=self.window3D.model.evolution_steps-1, steps=self.window3D.model.evolution_steps-1)
        self.slider_end = HorizontalSlider(value=self.window3D.model.evolution_steps-1, min_value=0, max_value=self.window3D.model.evolution_steps-1, steps=self.window3D.model.evolution_steps-1)

        # Following block concerns state/colour details
        # Sets up an array of checkbox buttons corresponding to states in the CA
        # Labels for the boxes are either Show colour X, or Show Y,
        # If colour X has a defined name Y in the CA
        self.highlight_checkbox_arr = [Checkbox(
            label= f"{x}: {self.window3D.model.ca.getStatename(x)}",
            on_press=self.highlight_colour) for x in range(self.window3D.model.ca.stateC)]
        # All boxes initially ticked
        for box in self.highlight_checkbox_arr: box._is_pressed = True
        # Buttons to show or hide all states
        self.hideall_button = OneTimeButton("Hide all",on_release=self.hide_all_highlights)
        self.showall_button = OneTimeButton("Show all",on_release=self.show_all_highlights)

        # Very similar to colours, following block for matches
        # Sets up an array of checkbox buttons corresponding to matched patterns
        self.match_checkbox_arr = [Checkbox(
            label= "Pattern " + str(pattern) + " ",
            on_press=self.highlight_match) for pattern in range(self.window3D.model.max_patterns)]
        # All boxes initially ticked
        for box in self.match_checkbox_arr: box._is_pressed = True
        # Buttons for showing or hiding all patterns
        self.hideall_match = OneTimeButton("Hide all",on_release=self.hide_all_matches)
        self.showall_match = OneTimeButton("Show all",on_release=self.show_all_matches)
        # Buttons for adding a pattern from a file, and for removing last match
        self.addmatch_button = OneTimeButton("Match Pattern",on_release=self.add_pattern_from_file)
        self.removematch_button = OneTimeButton("Remove Pattern",on_release=self.remove_last_pattern)
        # Zipping a list of pattern names and how often they're matched
        matches_strings_arr = zip(self.window3D.model.match_names,[str(match_count) for match_count in self.window3D.model.match_counts])
        # Creating a series of labels to demonstrate above info
        self.match_labels_list = [Label(pair[0]+": "+pair[1]+" matches     ") for pair in matches_strings_arr]
        # Putting these series of labels into a container vertically
        matches_labels = Scrollable(height=150, width=400, content=VerticalContainer(content=self.match_labels_list))

        # UI elements for changing the pattern window size
        match_window_label = Label("Pattern neighborhood size:")
        self.match_window_size_label = Label(" 0 ")
        self.match_window_plusbutton = OneTimeButton("+",on_release=self.increment_pattern_window)
        self.match_window_minusbutton = OneTimeButton("-",on_release=self.decrement_pattern_window)
        match_window_change_container = HorizontalContainer([self.match_window_minusbutton,self.match_window_size_label,self.match_window_plusbutton],align=HALIGN_CENTER)
        self.pattern_window_size = 0

        # This block concerns the different view modes for the system
        self.steplock_button = Button("Toggle Step-lock",on_press=self.toggle_steplock)

        self.mouseconnect_button = Button("Mouse/Crosshair",on_press=self.toggle_mouseconnect)

        self.save_pos_orient_button = OneTimeButton("Save position",on_release=self.save_pos_orient)
        self.load_pos_orient_button = OneTimeButton("Load position",on_release=self.load_pos_orient)
        # The lenses correspond to buttons with sets of mutual exclusivity
        # Lenses with the same group ID cannot be set at the same time
        # Default is pushed by default
        self.lensmodes = [
            Button(label="Crosshair", on_press = self.change_lens, is_pressed=True),
            Button(label="Default", on_press = self.change_lens, is_pressed=True),
            Button(label="Ghosts", on_press = self.change_lens),
            Button(label="Activity", on_press = self.change_lens),
            Button(label="Causal Analysis", on_press = self.change_lens),
            GroupButton(group_id=1, label="Cell-Specific CA", on_press = self.change_lens),
            Button(label="Light Cone", on_press = self.change_lens),
            Button(label="Pattern Matches", on_press = self.change_lens),
            Button(label="Neighborhoods", on_press = self.change_lens),
            Button(label="Lightcone-CA", on_press = self.change_lens),
            GroupButton(group_id=1, label="LightconeCA cubes", on_press = self.change_lens)
        ]

        self.backgroundbuttons = [
            GroupButton(group_id="1",label="Blue", on_press = self.change_background, is_pressed=True),
            GroupButton(group_id="1",label="Beige", on_press = self.change_background),
            GroupButton(group_id="1",label="Black", on_press = self.change_background),
            GroupButton(group_id="1",label="White", on_press = self.change_background)
        ]
        bg_button_label = Label("Background colour")
        bg_button_container_0 = HorizontalContainer([self.backgroundbuttons[0],self.backgroundbuttons[1]])
        bg_button_container_1 = HorizontalContainer([self.backgroundbuttons[2],self.backgroundbuttons[3]])
        bg_button_container_2 = VerticalContainer([bg_button_container_0,bg_button_container_1])


        self.causal_checkbox_arr = [Checkbox(
            label= f"{self.window3D.model.get_neighbor_count()}choose{pattern}",
            on_press=self.highlight_causal) for pattern in range(1,self.window3D.model.get_neighbor_count()+1)]
        # All boxes initially ticked
        for box in self.causal_checkbox_arr: box._is_pressed = True
        self.hideall_causal = OneTimeButton("Hide all",on_release=self.hide_all_causal)
        self.showall_causal = OneTimeButton("Show all",on_release=self.show_all_causal)


        self.causal_label_light_depth = Label("Press ; for CA")
        self.causal_label_rel_cells = Label("")

        causal_depth_label = Label("Causal analysis depth:")
        self.causal_depth_size_label = Label(" 3 ")
        self.causal_depth_plusbutton = OneTimeButton("+",on_release=self.increment_causal_depth)
        self.causal_depth_minusbutton = OneTimeButton("-",on_release=self.decrement_causal_depth)
        causal_depth_container = HorizontalContainer([self.causal_depth_minusbutton,self.causal_depth_size_label,self.causal_depth_plusbutton],align=HALIGN_CENTER)
        self.causal_depth = 3
        container_lightcone_causal = VerticalContainer([
            causal_depth_label,
            Spacer(5),
            causal_depth_container,
            self.causal_label_light_depth,
            self.causal_label_rel_cells,
            Spacer(10),
            bg_button_label,
            bg_button_container_2,
            Spacer(5),
            Label("Step with arrow keys"),
            self.steplock_button,
            Label("Disconnect mouse from crosshair"),
            self.mouseconnect_button,
            Spacer(5),
            self.save_pos_orient_button,
            self.load_pos_orient_button])


        container_causal_boxes = Scrollable(height=300, width=200, content=VerticalContainer(content=self.causal_checkbox_arr,align=HALIGN_CENTER))
        container_causal = VerticalContainer([
            Label("Choice tier filtering"),
            self.hideall_causal,
            self.showall_causal,
            container_causal_boxes],align=HALIGN_CENTER)

        # Next I define containers to hold UI elements together
        container_highlight_boxes = Scrollable(height=300, width=200, content=VerticalContainer(content=self.highlight_checkbox_arr,align=HALIGN_LEFT))
        container_highlight = VerticalContainer([
            Label("Show/hide states"),
            Spacer(),
            self.hideall_button,
            self.showall_button,
            container_highlight_boxes],align=HALIGN_CENTER)



        container_match_boxes = Scrollable(height=140, width=200, content=VerticalContainer(content=self.match_checkbox_arr,align=HALIGN_LEFT))
        container_match_add = HorizontalContainer([
            self.addmatch_button,
            self.removematch_button],align=HALIGN_CENTER)
        container_match = VerticalContainer([
            Label("Pattern matching"),
            self.hideall_match,
            self.showall_match,
            container_match_boxes,
            Spacer(5),
            match_window_label,
            match_window_change_container,
            Spacer(5),
            container_match_add,
            Spacer(5),
            matches_labels])

        container_details = VerticalContainer([
            label_CAdt,
            label_ca_type,
            label_dimensions,
            label_evolutions,
            label_neighborhoods,
            blank_label,
            label_observed,
            self.label_observed_state,
            Label(""),
            self.selected_rowcount_label,
            self.selected_colcount_label,
            self.selected_rackcount_label,
            self.selected_total_label],align=HALIGN_LEFT)

        container_slice = VerticalContainer([
            self.label_timeslice,
            self.slider_start,
            self.slider_end,
            self.button_timeslice])

        container_options = VerticalContainer([
            Label("View modes"),
            Spacer(5),
            *self.lensmodes,
            Spacer(5)
            ])

        UI_toprow = HorizontalContainer([
            container_details,
            Spacer(10),
            container_slice,
            Spacer(10),
            container_highlight,
            Spacer(10),
            container_options,
            Spacer(10)
            ])

        UI_bottomrow = HorizontalContainer([Spacer(),container_causal,container_lightcone_causal,container_match,Spacer()],padding=20)

        # High level container holding the other containers horizontally
        self.manager = Manager(\
            content=VerticalContainer([Spacer(),UI_toprow,Spacer(),Label("-"*150),Spacer(),UI_bottomrow],padding=10),
            window=self,
            theme=self.theme,
            batch=self.batch,
            is_movable=False)

    # Changes the projection in the model from 3D to 2D
    # AT the moment this just changes the view angle and locks movement/mouse
    def toggle_steplock(self,is_pressed):
        self.window3D.steplock = is_pressed

    def toggle_mouseconnect(self,is_pressed):
        self.window3D.mouse_connect = not is_pressed


    # passes details of lenses to the model
    def change_lens(self,pressed):
        self.window3D.model.change_lens([b.is_pressed for b in self.lensmodes])

    # calls the time slice function in the model with the current slider values
    def timeslice(self,_):
        self.window3D.model.set_nodraw(int(self.slider_start.value),int(self.slider_end.value))

    # Passes details of which colours to draw to the model
    def highlight_colour(self,_):
        self.window3D.model.update_highlight([box.is_pressed for box in self.highlight_checkbox_arr])

    # Passes details of which patterns to draw to the model
    def highlight_match(self,_):
        self.window3D.model.update_match_highlight([box.is_pressed for box in self.match_checkbox_arr])

    def show_all_highlights(self,_):
        for box in self.highlight_checkbox_arr:
            if not box.is_pressed:
                box.change_state()

    def hide_all_highlights(self,_):
        for box in self.highlight_checkbox_arr:
            if box.is_pressed:
                box.change_state()

    def show_all_matches(self,_):
        for box in self.match_checkbox_arr:
            if not box.is_pressed:
                box.change_state()

    def hide_all_matches(self,_):
        for box in self.match_checkbox_arr:
            if box.is_pressed:
                box.change_state()

    def highlight_causal(self,_):
        self.window3D.model.update_causal_draw([box.is_pressed for box in self.causal_checkbox_arr])

    def show_all_causal(self,_):
        for box in self.causal_checkbox_arr:
            if not box.is_pressed:
                box.change_state()

    def hide_all_causal(self,_):
        for box in self.causal_checkbox_arr:
            if box.is_pressed:
                box.change_state()


    def remove_last_pattern(self,_):
        self.window3D.model.remove_last_pattern()

    def decrement_pattern_window(self,_):
        if self.pattern_window_size > 0:
            self.pattern_window_size -= 1
        self.window3D.pattern_window_size = self.pattern_window_size

    def increment_pattern_window(self,_):
        self.pattern_window_size += 1
        self.window3D.pattern_window_size = self.pattern_window_size

    def decrement_causal_depth(self,_):
        if self.causal_depth > 1:
            self.causal_depth -= 1
        self.window3D.causal_depth = self.causal_depth

    def increment_causal_depth(self,_):
        self.causal_depth += 1
        self.window3D.causal_depth = self.causal_depth

    def change_background(self,_):
        self.window3D.change_background([button.is_pressed for button in self.backgroundbuttons])

    def save_pos_orient(self,_):
        self.window3D.save_pos_orient()

    def load_pos_orient(self,_):
        self.window3D.load_pos_orient()

    # Opens a dialog window to allow user to load a pattern from a file
    def add_pattern_from_file(self,_):
        # Opens a tkinter file dialogue
        # does dialogue have a ue at the end, im not going to look it up
        pattern = filedialog.askopenfilename(filetypes = (("Pattern files", "*.txt"),("All files","*.*")))
        # Will exit function if user did not select anything
        if not pattern:
            return None
        # Might be worth testing if this works on a linux file browser
        # Getting just the file name from the path
        pattern = os.path.basename(pattern)
        # Using a cell loader to convert the pattern to an array of cells
        cell_loader = CellLoader("patterns/"+pattern)
        match_cell_pattern = cell_loader.get_cells()
        # Passing this cell array to the model to match
        self.window3D.model.add_pattern_match(match_cell_pattern,match_name=pattern)

    # Function called to draw the UI
    def on_draw(self):
        # Clears previous elements
        self.clear()
        # Draws everything
        self.batch.draw()
        # On every frame the labels are updated for the CA details
        # This is done because my code structure doesnt allow information to easily
        # be sent updward from the model to the window3d to the windowui
        self.update_labels()

    # Updates the labels with uptodate info on the CA such as the observed state
    # and the time slices currently displayed
    def update_labels(self):
        # Updating the time slice label to document which regions of the CA are being displayed
        self.label_timeslice.set_text("Displayed steps: "+str(self.window3D.model.start)+" - "+str(self.window3D.model.end))
        self.label_observed_state.set_text(self.window3D.model.observed_state)

        self.match_window_size_label.set_text(" "+str(self.pattern_window_size)+" ")

        self.causal_depth_size_label.set_text(" "+str(self.causal_depth)+" ")

        self.causal_label_light_depth.set_text(f"With lightcone depth: {self.causal_depth}")
        self.causal_label_rel_cells.set_text(f"Found {self.window3D.model.responsible_cells} responsible cells")

        region_data = self.window3D.model.selection_region_size
        self.selected_rowcount_label.set_text(f"Rows selected: {region_data[0]}")
        self.selected_colcount_label.set_text(f"Columns selected: {region_data[2]}")
        self.selected_rackcount_label.set_text(f"Racks selected: {region_data[1]}")
        self.selected_total_label.set_text(f"Cells selected: {region_data[0]*region_data[1]*region_data[2]}")

        # Only updates match info if the model flag says theres anything new, since this rarely changes
        if self.window3D.model.updated_matches:
            for ind,label in enumerate(self.match_labels_list):
                label.set_text(f"{self.window3D.model.match_names[ind]}: {self.window3D.model.match_counts[ind]} matches     ")

            self.window3D.model.updated_matches = False

    # Closing the UI also closes the 3d model
    def on_close(self):
        self.window3D.close()
        self.close()
