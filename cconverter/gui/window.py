# -*- coding: utf-8 -*-
"""
:Date: Fri Jul 22 16:21:58 CEST 2011
:Authors: Einar Uvsløkk <einar.uvslokk@linux.com>
:Copyright: (c) 2011 Einar Uvsløkk
:License: GNU General Public License (GPL) version 3 or later

vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
from __future__ import division
import ConfigParser
import os

import pango
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from xdg import BaseDirectory

from ..core import currency
from ..core import app_info


class CConverterGui:
    """Ebethron currency converter is a simple gtk application for
    converting different currencies to another currency.
    """
    def __init__(self, config):
        builder = Gtk.Builder()
        filename = os.path.join(config['PKG_DATA_DIR'], 'ui', 'cconverter.ui')
        builder.add_from_file(filename)
        builder.connect_signals(self)

        self.config = Config()

        self.from_value = builder.get_object('from_value')
        self.value_buffer = builder.get_object('value_buffer')
        self.from_combo = builder.get_object('from_combo')
        self.to_value = builder.get_object('to_value')
        self.to_value_info = builder.get_object('to_value_info')
        self.to_combo = builder.get_object('to_combo')
        self.convert_button = builder.get_object('convert_button')
        self.equal_button = builder.get_object('button_equal')
        self.calculator = builder.get_object('calculator')

        self._init_comboboxes()

        attr = pango.AttrList()
        attr.insert(pango.AttrSize(30000, 0, -1))
        self.to_value.set_attributes(attr)

        table = builder.get_object('table')
        self.infobar = Gtk.InfoBar()
        self.info = Gtk.Label()
        self.infobar.get_content_area().pack_start(self.info, True, True, 0)
        self.infobar.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.infobar.connect('response', self.on_info_hide)
        table.attach(self.infobar, 0, 1, 1, 2,
                     Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                     0, 0, 0)

        self.window = builder.get_object('window')
        actiongroup = builder.get_object('AppActions')
        accelgroup = Gtk.AccelGroup()
        self.window.add_accel_group(accelgroup)
        for action in actiongroup.list_actions():
            action.set_accel_group(accelgroup)

        toolbar = builder.get_object('toolbar')
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.window.connect('destroy', self.on_destroy)
        self.window.connect('key-press-event', self.on_keypress_event)
        self.window.set_default_icon_name('cconverter')

    def _set_info_text(self, text, value=2):
        self.info.set_text(text)
        self.infobar.set_message_type(Gtk.MessageType(value))
        self.infobar.show()

    def _init_comboboxes(self):
        """Initialize the comboboxes with the supported currencies,
        which are defined in the currencies module.
        """
        cboxes = [self.from_combo, self.to_combo]
        for cbox in cboxes:
            cbox.set_model(self._get_currency_store())
            cell = Gtk.CellRendererText()
            cbox.pack_start(cell, True)
            cbox.add_attribute(cell, 'text', 1)

    def _get_currency_store(self):
        """Initialize the currency dropdown options."""
        store = Gtk.ListStore(str, str)
        for k, v in sorted(currency.currencies.iteritems()):
            store.append((k, v))

        return store

    def _calculate(self):
        """Returns a string corrosponding to the the avaulation of the
        input text buffer. If the evaluation fails, a infomessage is
        displayed, and None is returned.
        """
        expr = self.value_buffer.get_text()
        try:
            return str(eval(expr))
        except Exception as e:
            if len(expr) < 1:
                msg = 'Please enter a valid value to convert!'
                value = Gtk.MessageType.WARNING
            else:
                msg = 'Error: ' + str(e)
                value = Gtk.MessageType.ERROR

            self._set_info_text(msg, value)
            return None

    def _prepare_calculation(self, operand):
        """Appends an `operand` to the input text buffer."""
        tmp = self.from_value.get_text()

        if tmp == '':
            if operand == '-':
                self._update_buffer_text(operand)
        else:
            try:
                int(tmp[-1])
            except ValueError:
                tmp = tmp[:-1]

            self._update_buffer_text(tmp + operand)

    def _update_buffer_text(self, text):
        """Utility method for updating the input text buffer."""
        self.value_buffer.set_text(text, len(text))
        self.from_value.set_position(len(text))

    def _get_current_from_currency(self):
        """Utility method that returns the currently selected currency
        code to convert from.
        """
        model = self.from_combo.get_model()
        iter_from = model.get_iter(self.from_combo.get_active())
        return model.get_value(iter_from, 1)

    def _get_current_to_currency(self):
        """Utility method that returns the currently selected currency
        code to convert to.
        """
        model = self.to_combo.get_model()
        iter_from = model.get_iter(self.to_combo.get_active())
        return model.get_value(iter_from, 1)

    def run(self):
        """Main application entry point."""
        self.window.show_all()
        self.config.read()
        self.from_combo.set_active(self.config.from_currency)
        self.to_combo.set_active(self.config.to_currency)
        Gtk.Widget.hide(self.infobar)
        Gtk.main()

    def on_keypress_event(self, widget, event):
        if event.keyval == Gdk.KEY_q:
            if event.state == Gdk.ModifierType.CONTROL_MASK:
                self.on_destroy()
        if event.keyval == Gdk.KEY_Return:
            if event.state == Gdk.ModifierType.CONTROL_MASK:
                self.equal_button.emit('activate')
            else:
                if self.infobar.get_visible():
                    self.on_info_hide(self.infobar)
                else:
                    self.convert_button.emit('activate')
        elif event.keyval == Gdk.KEY_F12:
            self.on_about()
        elif event.keyval == Gdk.KEY_Delete:
            self.on_clear()

    def on_destroy(self, widget=None):
        self.config.from_currency = self.from_combo.get_active()
        self.config.to_currency = self.to_combo.get_active()
        self.config.write()
        Gtk.main_quit()

    def on_input_changed(self, widget):
        pass

    def on_about(self, widget=None):
        app = AboutDialog(self.window)
        app.show()

    def on_clear(self, widget=None):
        self.value_buffer.set_text('', -1)

    def on_convert(self, widget=None):
        value = self._calculate()
        if not value is None:
            _from = self._get_current_from_currency()
            _to = self._get_current_to_currency()
            response = currency.convert(value, _from, _to)
            info = currency.exchangerate(_from, _to)
            self.to_value.set_text(response)
            self.to_value_info.set_text('Exhangerate: {}'.format(info))

    def on_info_hide(self, widget, data=None):
        Gtk.Widget.hide(widget)

    def on_calc_toggled(self, widget):
        if widget.get_active():
            self.calculator.set_visible(True)
        else:
            self.calculator.set_visible(False)

    def on_calc_button_activate(self, widget):
        """Callback for the various buttons in the calculator widget."""
        txt = widget.get_label()
        try:
            int(txt)
            from_value = self.value_buffer.get_text()
            self._update_buffer_text(from_value + txt)
        except ValueError:
            if txt == '=':
                value = self._calculate()
                if not value is None:
                    self._update_buffer_text(value)
            else:
                self._prepare_calculation(txt)


class AboutDialog(Gtk.AboutDialog):
    """Simple about dialog for the application."""
    def __init__(self, parent, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.set_program_name(app_info.name)
        self.set_version(app_info.version)
        self.set_comments(app_info.description)
        self.set_copyright(app_info.copyright)
        self.set_website(app_info.website)
        self.set_authors(app_info.authors)
        self.set_logo_icon_name('cconverter')
        self.set_license(app_info.license)
        self.set_wrap_license(True)
        self.connect('response', self.on_response)
        self.set_transient_for(parent)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

    def on_response(self, widget, data):
        self.destroy()


class Config(object):
    """A simple Config object."""
    def __init__(self):
        self._from_currency = 0
        self._to_currency = 0
        self._check_location()

    def _check_location(self):
        """Basic check to ensure we have a valid fileobject to work with
        for the `ConfigParser` object.
        """
        try:
            prefix = os.path.join(BaseDirectory.xdg_config_home, 'cconverter')
        except ImportError:
            prefix = os.path.join(os.environ['HOME'], '.config', 'cconverter')

        if not os.path.exists(prefix):
            try:
                os.mkdir(prefix)
            except (IOError, OSError):
                # TODO Do some logging. We should load the application, but
                #      provide information to user that no settings will be
                #      saved due to (most likely) file permission issues.
                #      Maybe prompt for a user spesific folder?
                import tempfile
                prefix = tempfile.gettempdir()

        self.filename = os.path.join(prefix, 'config.ini')

    def write(self):
        config = ConfigParser.ConfigParser()
        config.add_section('currency')
        config.set('currency', 'from', self._from_currency)
        config.set('currency', 'to', self._to_currency)
        config.write(open(self.filename, 'w'))

    def read(self):
        config = ConfigParser.ConfigParser()
        config.read(self.filename)
        if config.has_section('currency'):
            self._from_currency = int(config.get('currency', 'from'))
            self._to_currency = int(config.get('currency', 'to'))

    def get_from_currency(self):
        return self._from_currency

    def set_from_currency(self, value):
        self._from_currency = value

    from_currency = property(get_from_currency, set_from_currency)

    def get_to_currency(self):
        return self._to_currency

    def set_to_currency(self, value):
        self._to_currency = value

    to_currency = property(get_to_currency, set_to_currency)


def register_stock_icon(config):
    iconsdir = os.path.join(config['PKG_DATA_DIR'], 'icons')
    icontheme = Gtk.IconTheme.get_default()
    icontheme.append_search_path(iconsdir)


def main(config):
    register_stock_icon(config)
    CConverterGui(config).run()
