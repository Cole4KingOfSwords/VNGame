#--Imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import json #For reading save and bulk logic files
import os
#--Game
class game(Gtk.Application):
    # --Classes
    class source:
        def __getitem__(self, key):
            return getattr(self, key)
        def __init__(self):
            SrcPath = './game/engine/'
            files = os.listdir(SrcPath)
            for file in files:
                setattr(self, file.split('.')[0], SrcPath+file)


    class window_manager(Gtk.Window):
        #--Window Classes
        class menu(Gtk.Box):
            # --Menu Funcs
            def __init__(self, *args, **kwargs):
                super().__init__()

                self.data = data = kwargs['menu_data']
                self.name = data['name']
                
                self.build = build = Gtk.Builder()
                if 'manager' in data:
                    self.build.add_from_string(getattr(getattr(window_manager.game, data['manager']), 'model'))
                elif 'model' in data:
                    self.build.add_from_string(data['model'])
                else:
                    raise ValueError("No Object")
                self.add(build.get_object(self.name))
                if 'xtions' in self.data:
                    self.connect()
            def connect(self):
                xtions = self.data['xtions']
                for xtion in xtions:
                    self.build.get_object(xtion[0]).connect(xtion[1], getattr(event_manager, xtion[2]) )
        #--Window Funcs
        def __init__(self, *args, **kwargs):
            super().__init__()

            #Build
            self.build = Gtk.Builder()
            self.build.add_from_file("main.xml")

            #MenuVars
            self.menus = {}
            self.current_menu = None

            #Window
            self.window = self.build.get_object("win")
            self.window.set_title("VNGame")
            self.window.connect("destroy", Gtk.main_quit)
            self.window.present()

            #Start
            self.get_menus()

            #Debug
            for menu in self.menus:
                pass
        def get_menus(self):
            with open('game/engine/menus.json', 'r') as file:
                menu_data  = json.load(file)
                for menu in menu_data:
                    menus = self.menus
                    menu_name = menu['name']
                    try:
                        menus[menu_name] = self.menu(menu_data=menu, manager=self)
                    except ValueError:
                        continue
        def switch(self, *args, **kwargs):
            #--Vars
            current_menu = self.current_menu
            next_menu = kwargs['menuName']
            window = self.window

            #--Do
            window.remove(window.get_child())
            window.add(self.menus[next_menu])
            window.show_all() #End And Show
    class event_manager:
        class event:
            class dialog(Gtk.Box):
                def __init__(self, *args, **kwargs):
                    super().__init__()

                    self.label = [] #['name', 'image']
                    self.text = ""
                def __getitem__(self, key):
                    match key:
                        case 'text':
                            return self.text
                        case 'label':
                            return self.label[0]
                        case 'picture':
                            return self.label[1]
                def __setitem__(self, key, value):
                    match key:
                        case 'text':
                            self.text = value
                        case 'label':
                            self.label[0] = value
                        case 'picture':
                            self.label[1] = value
                def show(self):
                    self.textBox = Gtk.TextView()
                    self.textBox.set_editable(False)
                    self.textBox.set_cursor_visible(False)
                    self.textBox.set_wrap_mode(Gtk.WrapMode.WORD)

                    #Check if label, create GtkLabel if one exists
                    if self.dialogLabel[0] is not None:
                        self.dialogLabel[0] = Gtk.Label(label=self.dialogLabel[1])
                        self.prepend(child=self.dialogLabel[0])
                    
                    self.textBox.get_buffer().set_text(self.dialogtext)

                    #add portrait if any
                    if self.dialogLabel[2] is not None:
                        self.dialogLabel[2] = Gtk.Image()
                        self.pack_end(child=self.dialogLabel[2])
                    self.show_all()

            def __init__(self, **kwargs):
                #--Event Vars
                self.times_triggered = 0
                self.event_handler = kwargs['parent']
                self.data = data = kwargs['data']
                self.name = data['name']
                self.conditions =  data['conditions']
                self.type = data['type']
                self.actions = data['actions']
                print(self.name)
                setattr(self.event_handler, self.name, self)
            def __call__(self, *args, **kwargs):
                #--Vars
                actions = self.actions
                #--Do
                for action in actions:
                    match action['type']:
                        case 'goto':
                            pass
                        case 'switch':
                            window_manager.switch(menuName=action['value'])
                        case 'modify':
                            pass
                        case 'dialog':
                            dialog_menu = None
                            for dialog in action['value']:
                                tmp = self.dialog()
                                tmp['text'] = dialog[1]
                                

                                
                            window_manager.switch(menuName='dialogMenu')
                        case 'DEBUG':
                            print(action['value'])
                        case _:
                            exec(str(action['value']))
                    self.actions.remove(action)
                    break

        #--Funcs
        def __init__(self, *args, **kwargs):
            pass

            self.read_events()
        def read_events(self):
            with open(getattr(source, 'events'), 'r') as file:
                events_data = json.load(file)
                for event in events_data:
                    self.event(parent=self, data=event)
    class location_manager:
        model = "<interface><object class='GtkBox'></object>" #placeHolder
        # --Location Manager Funcs
        def __init__(self, *args, **kwargs):
            pass

    # --Funcs
    def __init__(self, *args, **kwargs):
        super().__init__(application_id='org.cole4king.vngame')

        global source, event_manager, window_manager, location_manager
        source = self.source()
        event_manager = self.event_manager()
        window_manager = self.window_manager()
        location_manager = self.location_manager()

        event_manager.start()
    
game = game()
for item in window_manager.menus:
    print(item, window_manager.menus[item])
Gtk.main()
# TODO: Add a debug window for runtime diagnostics and logging
# TODO: Change events to dynamicy load in. IE:events which are imposible do not get loaded