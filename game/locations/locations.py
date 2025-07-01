import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import json

#------------------------------------------------------------------------------------------------------------
#
#----
class location_handler: # Handles locations in the game
    class location_view_type:
        def __init__(self):
            pass
    class location:
        def __init__(self):
            pass

        def connect_buttons(self):
            pass
            


    def __init__(self, parent):
        #vars
        self.parent = parent
        self.ignore_objects = []

        #get ignore objects
        ########### This is a placeholder for the actual ignore objects

        #get locations
        with open("game/locations/locations.json", "r") as file:
            location_data = json.load(file)
            for location in location_data:
                tmp_location = self.location()
                tmp_location.name = location["name"]
                
                if 'background' in location.keys():
                    pass

        #Check if mod handler has locaions

        #Make menu
        
        self.menu = Gtk.Box()

    #Goto
    def goto(self, *args, **kwargs):
        pass
