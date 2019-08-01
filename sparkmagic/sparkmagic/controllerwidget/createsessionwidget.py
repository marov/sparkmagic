# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.
import json

import sparkmagic.utils.configuration as conf
from sparkmagic.utils.constants import LANG_SCALA, LANG_PYTHON, LANG_R
from sparkmagic.controllerwidget.abstractmenuwidget import AbstractMenuWidget


class CreateSessionWidget(AbstractMenuWidget):
    def __init__(self, spark_controller, ipywidget_factory, ipython_display, endpoints_dropdown_widget, refresh_method):
        # This is nested
        super(CreateSessionWidget, self).__init__(spark_controller, ipywidget_factory, ipython_display, True)

        self.refresh_method = refresh_method

        self.endpoints_dropdown_widget = endpoints_dropdown_widget

        self.session_widget = self.ipywidget_factory.get_text(
            description='Name:',
            value='session-name'
        )
        self.lang_widget = self.ipywidget_factory.get_toggle_buttons(
            description='Language:',
            options=[LANG_PYTHON, LANG_SCALA, LANG_R], max_width="100%"
        )
        self.properties = self.ipywidget_factory.get_text(
            description='Properties:',
            value=json.dumps(conf.session_configs())
        )
        self.submit_widget = self.ipywidget_factory.get_submit_button(
            description='Create Session'
        )

        self.children = [self.ipywidget_factory.get_hbox(children=
                        [self.ipywidget_factory.get_vbox(children=[self.endpoints_dropdown_widget, self.session_widget], max_width="100%"),
                         self.ipywidget_factory.get_vbox(children=[self.lang_widget], max_width="100%"),
                         self.ipywidget_factory.get_vbox(children=[self.properties, self.submit_widget], max_width="100%")]
                        )]

        for child in self.children:
            child.parent_widget = self

        self.submit_widget.parent_widget = self

    def run(self):
        try:
            properties_json = self.properties.value
            if properties_json.strip() != "":
                conf.override(conf.session_configs.__name__, json.loads(self.properties.value))
        except ValueError as e:
            self.ipython_display.send_error("Session properties must be a valid JSON string. Error:\n{}".format(e))
            return

        endpoint = self.endpoints_dropdown_widget.value
        language = self.lang_widget.value
        alias = self.session_widget.value
        skip = False
        properties = conf.get_session_properties(language)

        try:
            self.spark_controller.add_session(alias, endpoint, skip, properties)
        except ValueError as e:
            self.ipython_display.send_error("""Could not add session with
name:
    {}
properties:
    {}

due to error: '{}'""".format(alias, properties, e))
            return

        self.refresh_method()
