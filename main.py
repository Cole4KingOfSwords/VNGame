#Top of VNGame
#------------------------------------------------------------------------------------------
#   Imports
#-------------------------------------------------------------------------------------------
import json #For reading save and bulk logic files
#Gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from game.locations.locations import location_handler
from game.events.events import event_handler

#------------------------------------------------------------------------------------------
#   Main
#-------------------------------------------------------------------------------------------
class main(Gtk.Application):

#---------------------------------------------------------------------------------
#   Game Classes
#----------------------------------------------------------------------------------
    class sidebar: # Depreciated(move to other file)
        #---------------------------------------------------------------------------------    
        #   SideBar Classes | hold gui elements for the sidebar(and their logic)
        #-----------------------------------------------------------------------------------
        class default_paperdoll: #Unmodded Paperdoll
            def __init__(self, parent):
                self.parent = parent
                self.object = Gtk.Box()
                self.object.add(Gtk.Label(label="Default Paperdoll Placeholder"))
        class foward_back_buttons: # Navs Foward/Backward in time
            def __init__(self, parent):
                self.parent = parent
                self.object = Gtk.Box()

        #---------------------------------------------------------------------------------
        #   SideBar Init
        #-----------------------------------------------------------------------------------
        enable = False
        def __init__(self, parent):
            self.parent = parent

            #get the sidebar object from the builder
            self.object = parent.build.get_object("sidebar")
            self.object.add(Gtk.Label(label="Sidebar Placeholder"))

            #Initialize default paperdoll
            self.paperdoll = self.default_paperdoll(self)
        
        #---------------------------------------------------------------------------------
        #   SideBar Functions
        #-----------------------------------------------------------------------------------
        def show_hide_logic(self): #Hides the sidebar when nessary
            if self.enable:
                pass
            else:
                return #if sidebar is enabled, do nothing
            disallowed_menus = ['startMenu', 'settingsMenu']
            if self.parent.build.get_object("contentBox").get_children()[0].get_name() in disallowed_menus:
                self.object.hide()
            else:
                self.object.show_all()
    class mod_handler: # Depreciated(move to other file)
        def __init__(self, parent):
            self.parent = parent
            self.mods = []
            self.load_mods()
        def load_mods(self):
            pass
        def register_mod_items(self, mod):
            """
            Register items from a mod.
            This is a placeholder for the actual implementation.
            """
            pass

    class window_manager:
        class menu(Gtk.Box):
            class sub_menu(Gtk.Box):
                def __init__(self):
                    super().__init__()
            def __init__(self, *args, **kwargs):
                super().__init__()
                self.parent = kwargs['parent']
                if 'object' in kwargs:
                    self.object = kwargs['object']
                self.add(self.object)
            def connect_signals(self):
                pass
            def switch_sub(self):
                for child in self.content_box.get_children():
                    self.content_box.remove(child)

        #Functions
        def __init__(self, parent):
            #menu list
            self.menus = {}
            self.current_menu = None

            #Build
            self.build = Gtk.Builder()
            self.build.add_from_file("main.xml")
            
            #Window
            self.window = self.build.get_object("win")
            self.window.set_title("VNGame")
            self.window.connect("destroy", Gtk.main_quit)
            self.window.present()
            
            #start
            self.get_menus()
            self.switch_menu(menuname="startMenu")

            for menu in self.menus:
                print(menu, self.menus[menu])
        def switch_menu(self, **kwargs):
            #Remove all children from content box
            self.window.remove(self.window.get_child())
            self.window.add(self.menus[kwargs['menuname']])

            self.window.show_all()

        def get_menus(self, **kwargs):
            if len(self.menus) == 0 or 'startMenu' not in self.menus:
                #Get start menu
                start_menu = self.menu(parent=self, object=self.build.get_object("startMenu"))
                self.menus['startMenu'] = start_menu
                #Get settings menu
                settings_menu = self.menu(parent=self, object=self.build.get_object("settingsMenu"))
                self.menus['settingsMenu'] = settings_menu

#------------------------------------------------------------------------------------------
#   Main Class Init
#------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__(application_id='org.cole4king.vngame')
        #Init
        self.window_manager = self.window_manager(self)
        #Initialize event handler
        self.event_handler = event_handler(self)

        #Initialize Location Handler
        self.location_handler = location_handler(self)

        #finish and show window


#------------------------------------------------------------------------------------------
#   Main Logic
#------------------------------------------------------------------------------------------

    def switch_menu(self, callback=None, menuname='startMenu'):
        
        #Add new menu
        self.content_box.add(self.get_menus(menuname))
        self.content_box.show_all()
        #Update sidebar visibility
        self.sidebar.show_hide_logic()
        #Connect signals
        match menuname : #this is fine 
            case 'startMenu':
                self.build.get_object("startButton").connect("clicked", self.start_game)
                self.build.get_object("settingsButton").connect("clicked", self.switch_menu, 'settingsMenu')
                self.build.get_object("exitButton").connect("clicked", Gtk.main_quit)
            
            case 'settingsMenu':
                self.build.get_object("backButton").connect("clicked", self.switch_menu, 'startMenu')
            
            case _:
                pass


#------------------------------------------------------------------------------------------
#   Game Logic
#------------------------------------------------------------------------------------------
    def start_game(self, callBack): #callback is unused because it has no use
        self.event_handler.call_event('start')

#------------------------------------------------------------------------------------------
#   Main
#------------------------------------------------------------------------------------------
main = main()
Gtk.main()