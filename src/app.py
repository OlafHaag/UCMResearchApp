""" Research application aimed at studying uncontrolled manifold and optimal feedback control paradigms. """

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import global_idmap, Builder
from kivy.properties import ObjectProperty
from kivy.utils import platform

from .utility import create_user_identifier, switch_language, get_app_details
from .datamanager import DataManager
from .i18n import _, DEFAULT_LANGUAGE
from .settings import SettingsContainer
from .widgets import SettingsWithTabbedPanels
from .settingsjson import LANGUAGE_CODE, LANGUAGE_SECTION, get_settings_general_json, get_settings_circle_task_json


# i18n
global_idmap['_'] = _


class NeuroPsyResearchApp(MDApp):
    manager = ObjectProperty(None, allownone=True)
    use_kivy_settings = False
    settings_cls = SettingsWithTabbedPanels

    def build(self):
        """ Initializes the application; it will be called only once.
        If this method returns a widget (tree), it will be used as the root widget and added to the window.
        """
        self.title = get_app_details()['appname']
        # Theme.
        self.icon = 'res/icons/mipmap-xxhdpi/npsy-icon.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        # Settings.
        self.settings = SettingsContainer()
        self.update_language_from_config()
        self.data_mgr = DataManager()
        self.data_mgr.bind(on_data_processing_failed=lambda instance, msg: self.manager.dispatch('on_error', msg),
                           on_data_upload=lambda instance, status, msg: self.manager.dispatch('on_upload_response',
                                                                                              status,
                                                                                              msg),
                           )
        
        root = Builder.load_file('src/widgets/navigation.kv')
        self.manager = root.ids.mgr
        self.set_orientation_from_config()
        return root
    
    def set_orientation_from_config(self):
        """ Set screen orientation from saved config value. """
        orientation = self.config.get('General', 'orientation')
        self.manager.orientation = orientation

    def get_application_config(self, defaultpath='%(appdir)s/%(appname)s.ini'):
        """ Override path to application configuration. """
        if platform == 'win':
            return super(NeuroPsyResearchApp, self).get_application_config('~/.%(appname)s.ini')  # User directory.
        else:
            return super(NeuroPsyResearchApp, self).get_application_config()  # Use default.
    
    def build_config(self, config):
        """ This method is called before the application is initialized to construct the ConfigParser object.
        The configuration will be automatically saved in the file returned by get_application_config().
        """
        # setdefault doesn't work here for single keys. Can't find section if no config yet. NoSectionError
        app_details = get_app_details()
        config.setdefaults(LANGUAGE_SECTION, {LANGUAGE_CODE: DEFAULT_LANGUAGE})
        config.setdefaults('General', {'is_first_run': 1,
                                       'orientation': 'portrait',
                                       'current_user': create_user_identifier(),
                                       'sound_enabled': 1,
                                       'vibration_enabled': 1,
                                       })
        config.setdefaults('DataCollection',
                           {
                               'is_local_storage_enabled': 0,
                               'is_upload_enabled': 1,
                               'webserver': app_details['webserver'],
                               'is_email_enabled': 0,
                           })
        config.setdefaults('CircleTask',
                           {
                               'n_trials': 30,
                               'n_blocks': 3,
                               'constrained_block': 2,
                               'warm_up_time': 1.0,
                               'trial_duration': 2.0,
                               'cool_down_time': 0.5,
                               'email_recipient': app_details['contact'],
                               'researcher': app_details['author'],
                           })
        # To set aliases for user ids we need to schedule it next frame, we can't retrieve current_user yet.
        Clock.schedule_once(lambda dt: self.set_configdefaults_user(config), 1)
    
    def set_configdefaults_user(self, config):
        """ Set default alias for first user. """
        # We allow multiple users on the same device.
        user_id = config.get('General', 'current_user')
        config.setdefaults('UserData', {user_id: 'Standard'})

    def build_settings(self, settings):
        """ Populate settings panel. """
        settings.add_json_panel(_('General'),
                                self.config,
                                data=get_settings_general_json())
        settings.add_json_panel(_('Circle Task'),
                                self.config,
                                data=get_settings_circle_task_json())
    
    def display_settings(self, settings):
        """ Display the settings panel. """
        if self.manager.current == 'Settings':
            return False
        self.manager.display_settings(settings)
        return True
    
    def close_settings(self, *args):
        """ Close the settings screen. """
        self.manager.close_settings()
        
    def _on_keyboard_settings(self, window, *largs):
        """ Disable the kivy built-in keyboard handling.
        We don't want people calling the settings while running a study.
        """
        pass
    
    def on_config_change(self, config, section, key, value):
        """ Fired when the section's key-value pair of a ConfigParser changes. """
        if section == 'Localization' and key == 'language':
            switch_language(value)
            s = self.manager.get_screen('Settings')
            if s:
                self.manager.remove_widget(s)
                self.destroy_settings()
                self.open_settings()

    def update_language_from_config(self):
        """Set the current language of the application from the configuration.
        """
        config_language = self.config.get(LANGUAGE_SECTION, LANGUAGE_CODE)
        switch_language(lang=config_language)
    
    def get_upload_route(self):
        """ Generate the destination URI dependent on the current task.
        
        :return: Destination URI for data upload.
        :rtype: str
        """
        # Upload address depends on current task. One dash application per task.
        if self.settings.current_task == 'Circle Task':
            upload_route = '/circletask/_dash-update-component'
        # Map other tasks to their respective dash-app here.
        else:
            upload_route = ''
        server_uri = self.settings.server_uri.strip('/') + upload_route
        return server_uri
    
    # ToDo pause App.on_pause(), App.on_resume()
    def on_pause(self):
        # Here you can save data if needed
        return True
    
    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass
