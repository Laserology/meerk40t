# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Fri Jun 28 16:25:14 2019
#

import wx

from CH341DriverBase import *
from LhystudiosDevice import get_code_string_from_code

from Kernel import *
from icons import *

_ = wx.GetTranslation

# TODO: Issue #53 ( https://github.com/meerk40t/meerk40t/issues/53 ) Lacks mouseover hints.


class Controller(wx.Frame, Module):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Controller.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP
        wx.Frame.__init__(self, *args, **kwds)
        Module.__init__(self)
        self.SetSize((507, 507))
        self.button_controller_control = wx.ToggleButton(self, wx.ID_ANY, _("Start Controller"))
        self.text_controller_status = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_usb_connect = wx.ToggleButton(self, wx.ID_ANY, _("Connect Usb"))
        self.text_usb_status = wx.TextCtrl(self, wx.ID_ANY, "")
        self.gauge_buffer = wx.Gauge(self, wx.ID_ANY, 10)
        self.text_buffer_length = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_buffer_viewer = wx.BitmapButton(self, wx.ID_ANY, icons8_comments_50.GetBitmap())
        self.packet_count_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.rejected_packet_count_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.packet_text_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.last_packet_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_0 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_desc = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_3 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_4 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_byte_5 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_stop = wx.BitmapButton(self, wx.ID_ANY, icons8_stop_sign_50.GetBitmap())

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_button_start_controller, self.button_controller_control)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_button_start_usb, self.button_usb_connect)
        self.Bind(wx.EVT_BUTTON, self.on_button_emergency_stop, self.button_stop)
        self.Bind(wx.EVT_BUTTON, self.on_button_bufferview, self.button_buffer_viewer)
        # end wxGlade
        self.Bind(wx.EVT_CLOSE, self.on_close, self)
        self.uid = None
        self.dirty = False
        self.status_data = None
        self.packet_data = None
        self.packet_string = b''
        self.buffer_size = 0
        self.buffer_max = 0
        self.control_state = None
        self.usb_state = None

        self.update_packet_string = False
        self.update_packet_data = False
        self.update_status_data = False
        self.update_buffer_size = False
        self.update_control_state = False
        self.update_usb_status = False
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_controller_menu, self)

    def initialize(self):
        self.device.close('window', self.name)
        self.Show()

        if self.device.is_root():
            for attr in dir(self):
                value = getattr(self, attr)
                if isinstance(value, wx.Control):
                    value.Enable(False)
            dlg = wx.MessageDialog(None, _("You do not have a selected device."),
                                   _("No Device Selected."), wx.OK | wx.ICON_WARNING)
            result = dlg.ShowModal()
            dlg.Destroy()
            return

        self.device.listen("pipe;status", self.update_status)
        self.device.listen("pipe;packet", self.update_packet)
        self.device.listen("pipe;packet_text", self.update_packet_text)
        self.device.listen("pipe;buffer", self.on_buffer_update)
        self.device.listen("pipe;usb_state", self.on_usb_state)
        self.device.listen("pipe;thread", self.on_control_state)
        self.set_controller_button_by_state()

    def shutdown(self,  channel):
        self.Close()
        self.device = None

    def on_close(self, event):
        self.device.remove('window', self.name)
        try:
            if self.device is not None:
                self.device.unlisten("pipe;status", self.update_status)
                self.device.unlisten("pipe;packet", self.update_packet)
                self.device.unlisten("pipe;packet_text", self.update_packet_text)
                self.device.unlisten("pipe;buffer", self.on_buffer_update)
                self.device.unlisten("pipe;usb_state", self.on_usb_state)
                self.device.unlisten("pipe;thread", self.on_control_state)
        except KeyError:
            pass  # Must have not registered at start because of no device.
        event.Skip()  # delegate destroy to super

    def device_execute(self, control_name):
        def menu_element(event):
            self.device.execute(control_name)

        return menu_element

    def on_controller_menu(self, event):
        gui = self
        menu = wx.Menu()
        path_scale_sub_menu = wx.Menu()
        for control_name, control in self.device.instances['control'].items():
            gui.Bind(wx.EVT_MENU, self.device_execute(control_name),
                     path_scale_sub_menu.Append(wx.ID_ANY, control_name, "", wx.ITEM_NORMAL))
        menu.Append(wx.ID_ANY, _("Kernel Force Event"), path_scale_sub_menu)
        if menu.MenuItemCount != 0:
            gui.PopupMenu(menu)
            menu.Destroy()

    def __set_properties(self):
        # begin wxGlade: Controller.__set_properties
        self.SetTitle(_("Controller"))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_usb_connector_50.GetBitmap())
        self.SetIcon(_icon)
        self.button_controller_control.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_controller_control.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.button_controller_control.SetBitmap(icons8_play_50.GetBitmap())
        self.button_controller_control.SetBitmapPressed(icons8_pause_50.GetBitmap())
        self.button_usb_connect.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_usb_connect.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        self.button_usb_connect.SetBitmap(icons8_connected_50.GetBitmap())
        self.button_usb_connect.SetBitmapPressed(icons8_disconnected_50.GetBitmap())
        self.text_buffer_length.SetMinSize((165, 23))
        self.button_buffer_viewer.SetSize(self.button_buffer_viewer.GetBestSize())
        self.packet_count_text.SetMinSize((77, 23))
        self.rejected_packet_count_text.SetMinSize((77, 23))
        self.text_byte_0.SetMinSize((77, 23))
        self.text_byte_1.SetMinSize((77, 23))
        self.text_desc.SetMinSize((75, 23))
        self.text_byte_2.SetMinSize((77, 23))
        self.text_byte_3.SetMinSize((77, 23))
        self.text_byte_4.SetMinSize((77, 23))
        self.text_byte_5.SetMinSize((77, 23))
        self.button_stop.SetBackgroundColour(wx.Colour(127, 0, 0))
        self.button_stop.SetSize(self.button_stop.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Controller.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        byte_data_sizer = wx.BoxSizer(wx.HORIZONTAL)
        byte5sizer = wx.BoxSizer(wx.VERTICAL)
        byte4sizer = wx.BoxSizer(wx.VERTICAL)
        byte3sizer = wx.BoxSizer(wx.VERTICAL)
        byte2sizer = wx.BoxSizer(wx.VERTICAL)
        byte1sizer = wx.BoxSizer(wx.VERTICAL)
        byte0sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9.Add(self.button_controller_control, 0, wx.EXPAND, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, _("Controller"))
        label_12.SetMinSize((80, 16))
        sizer_17.Add(label_12, 1, 0, 0)
        sizer_17.Add(self.text_controller_status, 0, wx.EXPAND, 0)
        sizer_9.Add(sizer_17, 0, 0, 0)
        sizer_1.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_18.Add(self.button_usb_connect, 0, wx.EXPAND, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, _("Usb Status"))
        label_7.SetMinSize((80, 16))
        sizer_15.Add(label_7, 1, 0, 0)
        sizer_15.Add(self.text_usb_status, 0, 0, 0)
        sizer_18.Add(sizer_15, 0, 0, 0)
        sizer_1.Add(sizer_18, 0, wx.EXPAND, 0)
        static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)
        sizer_1.Add(self.gauge_buffer, 0, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, _("Buffer"))
        sizer_5.Add(label_8, 0, 0, 0)
        sizer_5.Add(self.text_buffer_length, 10, 0, 0)
        sizer_5.Add(self.button_buffer_viewer, 1, 0, 0)
        sizer_1.Add(sizer_5, 0, 0, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, _("Packet Count  "))
        sizer_2.Add(label_11, 0, 0, 0)
        sizer_2.Add(self.packet_count_text, 0, 0, 0)
        sizer_16.Add(sizer_2, 10, wx.EXPAND, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, _("Rejected Packets"))
        sizer_3.Add(label_13, 0, 0, 0)
        sizer_3.Add(self.rejected_packet_count_text, 0, 0, 0)
        sizer_16.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_16, 0, 0, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, _("Packet Text  "))
        sizer_14.Add(label_10, 1, 0, 0)
        sizer_14.Add(self.packet_text_text, 11, 0, 0)
        sizer_1.Add(sizer_14, 0, 0, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, _("Last Packet  "))
        sizer_13.Add(label_9, 1, 0, 0)
        sizer_13.Add(self.last_packet_text, 11, 0, 0)
        sizer_1.Add(sizer_13, 0, 0, 0)
        byte0sizer.Add(self.text_byte_0, 0, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, _("Byte 0"))
        byte0sizer.Add(label_1, 0, 0, 0)
        byte_data_sizer.Add(byte0sizer, 1, wx.EXPAND, 0)
        byte1sizer.Add(self.text_byte_1, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, _("Byte 1"))
        byte1sizer.Add(label_2, 0, 0, 0)
        byte1sizer.Add(self.text_desc, 0, 0, 0)
        byte_data_sizer.Add(byte1sizer, 1, wx.EXPAND, 0)
        byte2sizer.Add(self.text_byte_2, 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, _("Byte 2"))
        byte2sizer.Add(label_3, 0, 0, 0)
        byte_data_sizer.Add(byte2sizer, 1, wx.EXPAND, 0)
        byte3sizer.Add(self.text_byte_3, 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, _("Byte 3"))
        byte3sizer.Add(label_4, 0, 0, 0)
        byte_data_sizer.Add(byte3sizer, 1, wx.EXPAND, 0)
        byte4sizer.Add(self.text_byte_4, 0, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, _("Byte 4"))
        byte4sizer.Add(label_5, 0, 0, 0)
        byte_data_sizer.Add(byte4sizer, 1, wx.EXPAND, 0)
        byte5sizer.Add(self.text_byte_5, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, _("Byte 5"))
        byte5sizer.Add(label_6, 0, 0, 0)
        byte_data_sizer.Add(byte5sizer, 1, wx.EXPAND, 0)
        sizer_1.Add(byte_data_sizer, 0, wx.EXPAND, 0)
        sizer_1.Add(self.button_stop, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def post_update(self):
        if not self.dirty:
            self.dirty = True
            wx.CallAfter(self.post_update_on_gui_thread)

    def post_update_on_gui_thread(self):
        if self.device is None:
            return  # was closed this is just a leftover update.
        update = False
        if self.update_packet_string:
            string_data = self.packet_string
            if string_data is not None and len(string_data) != 0:
                self.packet_text_text.SetValue(str(string_data))
            self.packet_string = b''
            update = True

        if self.update_packet_data:
            self.update_packet_data = False
            self.last_packet_text.SetValue(str(self.packet_data))
            update = True

        if self.update_status_data:
            self.update_status_data = False
            status_data = self.status_data
            if status_data is not None:
                if isinstance(status_data, int):
                    self.text_desc.SetValue(str(status_data))
                    self.text_desc.SetValue(get_code_string_from_code(status_data))
                else:
                    if len(status_data) == 6:
                        self.text_byte_0.SetValue(str(status_data[0]))
                        self.text_byte_1.SetValue(str(status_data[1]))
                        self.text_byte_2.SetValue(str(status_data[2]))
                        self.text_byte_3.SetValue(str(status_data[3]))
                        self.text_byte_4.SetValue(str(status_data[4]))
                        self.text_byte_5.SetValue(str(status_data[5]))
                        self.text_desc.SetValue(get_code_string_from_code(status_data[1]))
            self.packet_count_text.SetValue(str(self.device.packet_count))
            self.rejected_packet_count_text.SetValue(str(self.device.rejected_count))
            update = True
        if self.update_buffer_size:
            self.update_buffer_size = False
            self.text_buffer_length.SetValue(str(self.buffer_size))
            self.gauge_buffer.SetRange(self.buffer_max)
            max = self.gauge_buffer.GetRange()
            value = min(self.buffer_size, max)
            self.gauge_buffer.SetValue(value)
            update = True
        if self.update_control_state:
            self.update_control_state = False
            self.text_controller_status.SetValue(self.device.get_text_thread_state(self.control_state))
            self.set_controller_button_by_state()
            update = True
        if self.update_usb_status:
            self.update_usb_status = False
            self.text_usb_status.SetValue(get_name_for_status(self.usb_state, translation=_))
            self.set_usb_button_by_state()
            update = True
        if update:
            pass
        self.dirty = False

    def on_button_start_controller(self, event):  # wxGlade: Controller.<event_handler>
        if self.device is not None:
            state = self.device.interpreter.pipe.state
            if state == THREAD_STATE_UNSTARTED or state == THREAD_STATE_FINISHED:
                self.device.interpreter.pipe.start()
            elif state == THREAD_STATE_PAUSED:
                self.device.interpreter.pipe.resume()
            elif state == THREAD_STATE_STARTED:
                self.device.interpreter.pipe.pause()
            elif state == THREAD_STATE_ABORT:
                self.device.interpreter.pipe.buffer = b''
                self.device.interpreter.pipe.queue = b''
                self.device.interpreter.pipe.reset()

    def on_button_emergency_stop(self, event):  # wxGlade: Controller.<event_handler>
        self.device.execute("Emergency Stop")

    def on_button_bufferview(self, event):  # wxGlade: Controller.<event_handler>
        self.device.open('window', "BufferView", None, -1, "")

    def update_status(self, data):
        self.update_status_data = True
        self.status_data = data
        self.post_update()

    def update_packet(self, data):
        self.update_packet_data = True
        self.packet_data = data
        self.post_update()

    def update_packet_text(self, string_data):
        self.update_packet_string = True
        self.packet_string = string_data
        self.post_update()

    def on_usb_state(self, status):
        self.update_usb_status = True
        self.usb_state = status
        self.post_update()

    def on_buffer_update(self, value, *args):
        self.update_buffer_size = True
        self.buffer_size = value
        if self.buffer_size > self.buffer_max:
            self.buffer_max = self.buffer_size
        self.post_update()

    def on_control_state(self, state):
        self.update_control_state = True
        self.control_state = state
        self.post_update()

    def on_button_start_usb(self, event):  # wxGlade: Controller.<event_handler>
        state = self.device.interpreter.pipe.usb_state
        if state in (STATE_USB_DISCONNECTED, STATE_UNINITIALIZED, STATE_CONNECTION_FAILED, STATE_DRIVER_MOCK):
            try:
                self.device.execute("Connect_USB")
            except ConnectionRefusedError:
                dlg = wx.MessageDialog(None, _("Connection Refused. See USB Log for detailed information."),
                                       _("Manual Connection"), wx.OK | wx.ICON_WARNING)
                result = dlg.ShowModal()
                dlg.Destroy()
        elif state in (STATE_CONNECTED, STATE_USB_CONNECTED):
            self.device.execute("Disconnect_USB")

    def set_usb_button_by_state(self):
        state = self.usb_state
        status = get_name_for_status(state, translation=_)
        if state == STATE_CONNECTION_FAILED or state == STATE_DRIVER_NO_BACKEND:
            self.button_usb_connect.SetBackgroundColour("#dfdf00")
            self.button_usb_connect.SetLabel(status)
            self.button_usb_connect.SetValue(True)
            self.button_usb_connect.Enable()
        elif state == STATE_UNINITIALIZED or state == STATE_USB_DISCONNECTED:
            self.button_usb_connect.SetBackgroundColour("#ffff00")
            self.button_usb_connect.SetLabel("Connect")
            self.button_usb_connect.SetValue(True)
            self.button_usb_connect.Enable()
        elif state == STATE_USB_SET_DISCONNECTING:
            self.button_usb_connect.SetBackgroundColour("#ffff00")
            self.button_usb_connect.SetLabel("Disconnecting...")
            self.button_usb_connect.SetValue(True)
            self.button_usb_connect.Disable()
        elif state == STATE_USB_CONNECTED or state == STATE_CONNECTED:
            self.button_usb_connect.SetBackgroundColour("#00ff00")
            self.button_usb_connect.SetLabel("Disconnect")
            self.button_usb_connect.SetValue(False)
            self.button_usb_connect.Enable()
        elif status == STATE_CONNECTING:
            self.button_usb_connect.SetBackgroundColour("#ffff00")
            self.button_usb_connect.SetLabel("Connecting...")
            self.button_usb_connect.SetValue(False)
            self.button_usb_connect.Disable()
        # print(status)

    def set_controller_button_by_state(self):
        state = self.control_state
        if state == THREAD_STATE_UNSTARTED or state == THREAD_STATE_FINISHED:
            self.button_controller_control.SetBackgroundColour("#009900")
            self.button_controller_control.SetLabel(_("Start Controller"))
            self.button_controller_control.SetValue(False)
        elif state == THREAD_STATE_PAUSED:
            self.button_controller_control.SetBackgroundColour("#00dd00")
            self.button_controller_control.SetLabel(_("Resume Controller"))
            self.button_controller_control.SetValue(False)
        elif state == THREAD_STATE_STARTED:
            self.button_controller_control.SetBackgroundColour("#00ff00")
            self.button_controller_control.SetLabel(_("Pause Controller"))
            self.button_controller_control.SetValue(True)
        elif state == THREAD_STATE_ABORT:
            self.button_controller_control.SetBackgroundColour("#00ffff")
            self.button_controller_control.SetLabel(_("Manual Reset"))
            self.button_controller_control.SetValue(True)

# end of class Controller
