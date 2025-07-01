#--Imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import json #For reading save and bulk logic files

#--Game
class game(Gtk.Application):
    # --Classes
    class window_manager(Gtk.Window):
        #--Window Classes
        class menu(Gtk.Box):
            # --Menu Funcs
            def __init__(self, *args, **kwargs):
                super().__init__()

                self.window_manager = kwargs['manager']
                self.data = data = kwargs['menu_data']

                self.name = data['name']
                
                self.build = build = Gtk.Builder()
                if 'manager' in data:
                    self.build.add_from_string(getattr(getattr(self.window_manager.game, data['manager']), 'model'))
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
                    self.build.get_object(xtion[0]).connect(xtion[1], getattr(self.window_manager.game.event_manager, xtion[2]) )
        #--Window Funcs
        def __init__(self, *args, **kwargs):
            super().__init__()
            #Game
            self.game = kwargs['game']

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
                            self.event_handler.game.window_manager.switch(menuName=action['value'])
                        case 'modify':
                            pass
                        case 'dialog':
                            for dialog in action['value']:
                                print(dialog[0], dialog[1])
                                self.event_handler.game.window_manager.switch(menuName='dialogMenu')
                        case 'DEBUG':
                            print(action['value'])
                        case _:
                            exec(str(action['value']))
                    self.actions.remove(action)
                    break

        #--Funcs
        def __init__(self, *args, **kwargs):
            self.game = kwargs['game']

            self.read_events()
        def read_events(self):
            with open('game/engine/events.json', 'r') as file:
                events_data = json.load(file)
                for event in events_data:
                    self.event(parent=self, data=event)
    class location_manager:
        model = "<interface><object class='GtkBox'></object>" #placeHolder
        # --Location Manager Funcs
        def __init__(self, *args, **kwargs):
            self.game = kwargs['game']

    # --Funcs
    def __init__(self, *args, **kwargs):
        super().__init__(application_id='org.cole4king.vngame')

        #Window
        self.event_manager = self.event_manager(game=self)

        self.window_manager = self.window_manager(game=self)

        self.location_manager = self.location_manager(game=self)

        self.event_manager.start()
    
game = game()
for item in game.window_manager.menus:
    print(item, game.window_manager.menus[item])
Gtk.main()
