





class event_handler: # Handles events in the game
    class event: # Represents an event in the game
        #---Event Init---

        #---Event Logic------------------------------------------------
        def trigger(self, *args, **kwargs):
            if self.type == 'onetime' and self.times_triggered > 0:
                raise ValueError("Change in event type after triggering, check version")
            #self.end() this will be called later
            for action in self.actions:
                print(action)
                content_box = self.event_handler.parent.content_box
                game = self.event_handler.parent
                match action['type']:
                    case 'dialog':
                        game.switch_menu(menuname="dialogMenu")
                        content_box.show_all()
                        dialog_menu = game.get_menus('dialogMenu')

                        #Dialog Box Class definition
                        class dialog_box(Gtk.Box):
                            def __init__(self):
                                super().__init__(orientation=Gtk.Orientation.VERTICAL)
                                self.dialogtext = None
                                self.dialogLabel = [ None, "", None ]#[has_name, name, portrait]
                                self.textBox = Gtk.TextView()
                                self.textBox.set_editable(False)
                                self.textBox.set_cursor_visible(False)
                                self.textBox.set_wrap_mode(Gtk.WrapMode.WORD)
                            def display(self):
                                #add the label if any
                                if self.dialogLabel[0] is not None:
                                    self.dialogLabel[0] = Gtk.Label(label=self.dialogLabel[1])
                                    self.prepend(child=self.dialogLabel[0])
                                #add content (will always have content)
                                self.textBox.get_buffer().set_text(self.dialogtext)
                                if self.dialogLabel[0] is not None:
                                    self.add_after(child=self.textBox, sibling=self.dialogLabel[0])
                                else:
                                    self.add(self.textBox)
                                #add portrait if any
                                if self.dialogLabel[2] is not None:
                                    self.dialogLabel[2] = Gtk.Image()
                                    self.pack_end(child=self.dialogLabel[2])
                                self.show_all()

                        for dialog in action['value']:
                            this_dialog = dialog_box()
                            if dialog[0] != "":
                                this_dialog.dialogLabel[2] = dialog[0]
                                if dialog[0] in game.characters :
                                    pass
                            this_dialog.dialogtext = dialog[1]
                            dialog_menu.add(this_dialog)
                            this_dialog.display()
                        else:
                            dialog_menu.add(Gtk.Label(label="End of Dialog"))
                            continue_button = Gtk.Button(label="Continue")
                            continue_button.connect("clicked", self.trigger)
                            dialog_menu.add(continue_button)
                            dialog_menu.show_all()
                        self.actions.remove(action) # Remove action after processing
                        return
                    case 'goto':
                        print(f"Going to {action['value']}")
                        self.event_handler.parent.location_handler.goto(action['value']) # End the event before switching menus
                    case _:
                        raise ValueError(f"Unknown action type: {action['type']}")
        def end(self, *args, **kwargs):
            match self.type:
                case 'called':
                    self.event_handler.called_events.remove(self)
                case 'onetime':
                    self.event_handler.events.remove(self)
                case 'repeat':
                    self.times_triggered += 1
                case 'special':
                    if 'special_condition' in self.local():
                        pass # Handle special condition
                    #eventually
                case _:
                    raise ValueError("Unknown event type")
        
    #Initialize event handler
    def __init__(self, parent):
        self.parent = parent
        self.events = []
        self.called_events = []
        self.mod_events = None
        self.read_events()


    def get_event(self, event_name):
        for event in self.events:
            if event.name == event_name:
                if event.conditions == True:
                    return event
        return None
    def call_event(self, event_name):
        for event in self.called_events:
            if event.name == event_name:
                event.trigger()
        return None
