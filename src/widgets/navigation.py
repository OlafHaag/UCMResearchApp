from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineIconListItem


class NavigationDrawer(MDNavigationDrawer):
    """ Hide the navigation drawer and disable swipe when it's disabled. """
    
    def set_disabled(self, value):
        super(NavigationDrawer, self).set_disabled(value)
        if value:
            self.swipe_edge_width = -10
            self.elevation = 0
        else:
            self.swipe_edge_width = 20
            self.elevation = 10
    
    
class ContentNavigationDrawer(BoxLayout):
    def on_kv_post(self, base_widget):
        self.register_event_type('on_home')
        self.register_event_type('on_users')
        self.register_event_type('on_settings')
        self.register_event_type('on_website')
        self.register_event_type('on_about')
        self.register_event_type('on_terms')
        self.register_event_type('on_exit')

    def on_home(self, *_):
        pass
    
    def on_users(self, *_):
        pass
    
    def on_settings(self, *_):
        pass
        
    def on_website(self, *_):
        pass
        
    def on_about(self, *_):
        pass
        
    def on_terms(self, *_):
        pass
    
    def on_exit(self, *_):
        pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()  # Icon name.

    def on_kv_post(self, base_widget):
        # When the icon is clicked, trigger on_release of parent.
        self.ids.icon.bind(on_release=lambda x: self.dispatch('on_release'))
