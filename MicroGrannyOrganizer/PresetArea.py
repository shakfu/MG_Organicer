from Knob import Knob
from Preset import Preset
from CanvasButton import CanvasButton
from CanvasButton import SwitchModes
from ButtonBar import ButtonBar
from SettingsBar import SettingsBar
from KnobButton import KnobButton

class PresetArea(object):
    """right side of the screen showing buttons and knobs for editing presets"""
    root = 0            ## TKinter root object
    canvas = 0          ## TKinter Canvas
    file_list = 0       ## List of all files, presets and samples
    knobs = []          ## Contains nobs in order: Attack, Release, Start, End, Rate, Crush, Grain, Shift

    knob_offs_x=770
    knob_offs_y=100
    knob_space_x=80
    knob_space_y=110

    preset = 0 ##contains the currently displayed preset
    active_slot = 0 ##contains the index of the currently selected slot of the preset (0-5)
    button_bar = 0 ##stores the buttonbar object containing knobs and BIGBUTTONS
    settings_bar = 0 ## the leds to toggle the 5 boolean settings

    def __init__(self, root, canvas, file_list):
        self.file_list=file_list
        self.root = root
        self.canvas = canvas
        # Create Knobs
        sizes = ((0,127), (0,127), (0,1023), (0,1023), (0,1023), (0,127), (0,127),(-127,128))
        names = ("ATTACK", "RELEASE","START","END","SAMPLE\nRATE","CRUSH","GRAIN\nSIZE","SHIFT\nSPEED")
        tags = ("Attack", "Release","Start","End","Rate","Crush","Loop_Length","Shift_Speed")
        self.knobs = []
        rows=4
        cols=2
        for y in range(cols):
            for x in range(rows):
                cor_x = self.knob_offs_x + x*self.knob_space_x
                cor_y = self.knob_offs_y + y*self.knob_space_y
                #knob = Knob(self.root, self.canvas, cor_x, cor_y, size[0], size[1], names[y][x])

                knob = KnobButton(min=sizes[y*cols+x][0],
                                max=sizes[y*cols+x][1],
                                label=names[y*cols+x],
                                x=cor_x,
                                y=cor_y,
                                root=self.root,
                                canvas=self.canvas,
                                width=80,
                                height=80,
                                on_img='images\\knob_on.png',
                                off_img='images\\knob_off.png',
                                disabled_img='images\\knob_dis.png',
                                highlight_img='images\\knob_high.png',
                                label_dock='down',
                                label_font='Courier 14 bold')
                knob.tag=tags[y*cols+x]
                knob.new_value_callback = self.value_update
                self.knobs.append(knob)

        self.button_bar = ButtonBar(canvas = self.canvas, root=self.root, file_list = self.file_list, x=459, y=497)
        self.button_bar.new_slot_callback = self.new_slot_selected
        self.button_bar.retrigger_callback = self.button_bar_retriggered
        self.settings_bar = SettingsBar(canvas = self.canvas, root=self.root, x=459, y=415)
        self.settings_bar.new_setting_callback = self.new_setting
        return super().__init__()

    def new_slot_selected(self, index):
        ## called when new slot is selected via one of the 6 buttons
        self.active_slot = index
        self.display_slot(index, self.preset)
        ##select sample in sample view
        self.root.sample_tree.select_file(self.preset.get_param(index, 'Name')+'.wav')

    def button_bar_retriggered(self, index):
        self.root.sample_tree.select_file(self.preset.get_param(index, 'Name')+'.wav')

    def new_setting(self, setting):
        ## called when setting bar was changed
        self.value_update("Setting", setting)

    def display_preset(self, preset):
        self.preset=preset
        self.active_slot = 0
        self.display_slot(0, preset)

    def value_update(self, tag, value):
        ## new value from knob, update preset-object with new value
        self.preset.slots[self.active_slot][self.preset.get_name_index(tag)] = value

    def display_slot(self, index, preset):
        if preset:
            self.button_bar.set_labels(self.preset)
            self.button_bar.set_slot(index)
            self.knobs[0].set_num_value(preset.slots[index][self.preset.get_name_index("Attack")])
            self.knobs[1].set_num_value(preset.slots[index][self.preset.get_name_index("Release")])
            self.knobs[2].set_num_value(preset.slots[index][self.preset.get_name_index("Start")])
            self.knobs[3].set_num_value(preset.slots[index][self.preset.get_name_index("End")])
            self.knobs[4].set_num_value(preset.slots[index][self.preset.get_name_index("Rate")])
            self.knobs[5].set_num_value(preset.slots[index][self.preset.get_name_index("Crush")])
            self.knobs[6].set_num_value(preset.slots[index][self.preset.get_name_index("Loop_Length")])
            self.knobs[7].set_num_value(preset.slots[index][self.preset.get_name_index("Shift_Speed")])
            self.settings_bar.set_setting(preset.slots[index][self.preset.get_name_index("Setting")])

    def redraw(self):
        self.display_slot(self.button_bar.get_slot_index(), self.preset)