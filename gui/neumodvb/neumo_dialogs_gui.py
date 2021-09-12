#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0pre on Fri Aug 13 17:57:14 2021
#

import wx

# begin wxGlade: dependencies
import gettext
import wx.adv
# end wxGlade

# begin wxGlade: extracode
from neumodvb.neumowidgets import DurationTextCtrl
from neumodvb.neumowidgets import TimeTextCtrl
from neumodvb.neumowidgets import DatePickerCtrl
# end wxGlade


class ChannelNoDialog_(wx.Dialog):
				def __init__(self, *args, **kwds):
								# begin wxGlade: ChannelNoDialog_.__init__
								kwds["style"] = kwds.get("style", 0) | wx.MINIMIZE_BOX | wx.STAY_ON_TOP
								wx.Dialog.__init__(self, *args, **kwds)
								self.SetTitle(_("Neumo"))
								self.SetBackgroundColour(wx.Colour(0, 0, 0))
								self.SetForegroundColour(wx.Colour(255, 255, 0))
								self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))

								sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Channel number")), wx.HORIZONTAL)

								sizer_6.Add((0, 0), 0, 0, 0)

								self.chno = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
								self.chno.SetBackgroundColour(wx.Colour(0, 0, 0))
								self.chno.SetForegroundColour(wx.Colour(255, 255, 0))
								sizer_6.Add(self.chno, 2, 0, 0)

								self.SetSizer(sizer_6)
								sizer_6.Fit(self)

								self.Layout()

								self.Bind(wx.EVT_TEXT, self.OnText, self.chno)
								self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter, self.chno)
								# end wxGlade

				def OnText(self, event):  # wxGlade: ChannelNoDialog_.<event_handler>
								print("Event handler 'OnText' not implemented!")
								event.Skip()

				def OnTextEnter(self, event):  # wxGlade: ChannelNoDialog_.<event_handler>
								print("Event handler 'OnTextEnter' not implemented!")
								event.Skip()

# end of class ChannelNoDialog_

class LnbNetworkDialog_(wx.Dialog):
				def __init__(self, *args, **kwds):
								# begin wxGlade: LnbNetworkDialog_.__init__
								kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
								wx.Dialog.__init__(self, *args, **kwds)
								self.SetSize((1200, 400))
								self.SetTitle(_("Networks"))

								sizer_1 = wx.BoxSizer(wx.VERTICAL)

								self.lnbnetworklist_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_RAISED | wx.CLIP_CHILDREN)
								sizer_1.Add(self.lnbnetworklist_panel, 1, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

								self.lnbnetworkgrid_sizer = wx.BoxSizer(wx.VERTICAL)

								self.lnbnetworkgrid_sizer.Add((0, 0), 0, 0, 0)

								sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
								sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.FIXED_MINSIZE, 0)

								self.New = wx.Button(self, wx.ID_ANY, _("New"))
								sizer_2.Add(self.New, 1, 0, 0)

								self.Delete = wx.Button(self, wx.ID_ANY, _("Delete"))
								sizer_2.Add(self.Delete, 1, 0, 0)

								self.Cancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
								sizer_2.Add(self.Cancel, 0, wx.ALL, 1)

								self.Done = wx.Button(self, wx.ID_OK, _("Done"))
								sizer_2.Add(self.Done, 0, wx.ALL, 1)

								self.lnbnetworklist_panel.SetSizer(self.lnbnetworkgrid_sizer)

								self.SetSizer(sizer_1)

								self.Layout()

								self.Bind(wx.EVT_BUTTON, self.OnNew, self.New)
								self.Bind(wx.EVT_BUTTON, self.OnDelete, self.Delete)
								self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)
								self.Bind(wx.EVT_BUTTON, self.OnDone, self.Done)
								# end wxGlade

				def OnNew(self, event):  # wxGlade: LnbNetworkDialog_.<event_handler>
								print("Event handler 'OnNew' not implemented!")
								event.Skip()

				def OnDelete(self, event):  # wxGlade: LnbNetworkDialog_.<event_handler>
								print("Event handler 'OnDelete' not implemented!")
								event.Skip()

				def OnCancel(self, event):  # wxGlade: LnbNetworkDialog_.<event_handler>
								print("Event handler 'OnCancel' not implemented!")
								event.Skip()

				def OnDone(self, event):  # wxGlade: LnbNetworkDialog_.<event_handler>
								print("Event handler 'OnDone' not implemented!")
								event.Skip()

# end of class LnbNetworkDialog_

class ErrorDialog_(wx.Dialog):
				def __init__(self, *args, **kwds):
								# begin wxGlade: ErrorDialog_.__init__
								kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
								wx.Dialog.__init__(self, *args, **kwds)
								self.SetSize((800, 300))
								self.SetTitle(_("dialog_2"))

								sizer_3 = wx.BoxSizer(wx.VERTICAL)

								self.title = wx.StaticText(self, wx.ID_ANY, _("The title"), style=wx.ALIGN_CENTER_HORIZONTAL)
								self.title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
								sizer_3.Add(self.title, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

								static_line_1 = wx.StaticLine(self, wx.ID_ANY)
								sizer_3.Add(static_line_1, 0, wx.EXPAND, 0)

								sizer_3.Add((20, 20), 0, 0, 0)

								self.message = wx.StaticText(self, wx.ID_ANY, _("This is a message This is a message This is a message This is a message This is a message This is a message This is a message This is a message This is a message This is a message This is a message This is a message This is a message "))
								self.message.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Sans"))
								sizer_3.Add(self.message, 2, wx.EXPAND | wx.FIXED_MINSIZE, 0)

								sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ""), wx.HORIZONTAL)
								sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT | wx.FIXED_MINSIZE, 0)

								self.cancel = wx.Button(self, wx.ID_ANY, _("Cancel"))
								sizer_4.Add(self.cancel, 1, 0, 0)

								self.ok = wx.Button(self, wx.ID_ANY, _("OK"))
								sizer_4.Add(self.ok, 1, 0, 0)

								self.SetSizer(sizer_3)

								self.Layout()

								self.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.ID_CANCEL), self.cancel)
								self.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.ID_OK), self.ok)
								# end wxGlade

# end of class ErrorDialog_

class LanguageDialog_(wx.Dialog):
				def __init__(self, *args, **kwds):
								# begin wxGlade: LanguageDialog_.__init__
								kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
								wx.Dialog.__init__(self, *args, **kwds)
								self.SetSize((200, 400))
								self.SetTitle(_("Networks"))

								sizer_1 = wx.BoxSizer(wx.VERTICAL)

								self.languagelist_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_RAISED | wx.CLIP_CHILDREN)
								sizer_1.Add(self.languagelist_panel, 1, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

								self.languagegrid_sizer = wx.BoxSizer(wx.VERTICAL)

								self.languagegrid_sizer.Add((0, 0), 0, 0, 0)

								sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
								sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.FIXED_MINSIZE, 0)

								self.Done = wx.Button(self, wx.ID_OK, _("Done"))
								sizer_2.Add(self.Done, 0, wx.ALL, 1)

								self.languagelist_panel.SetSizer(self.languagegrid_sizer)

								self.SetSizer(sizer_1)

								self.Layout()

								self.Bind(wx.EVT_BUTTON, self.OnDone, self.Done)
								# end wxGlade

				def OnDone(self, event):  # wxGlade: LanguageDialog_.<event_handler>
								print("Event handler 'OnDone' not implemented!")
								event.Skip()

# end of class LanguageDialog_

class RecordDialog_(wx.Dialog):
				def __init__(self, *args, **kwds):
								# begin wxGlade: RecordDialog_.__init__
								kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
								wx.Dialog.__init__(self, *args, **kwds)
								self.SetTitle(_("Neumo Recording"))

								sizer_1 = wx.FlexGridSizer(1, 1, 20, 20)

								self.panel_1 = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
								sizer_1.Add(self.panel_1, 1, wx.ALL | wx.EXPAND, 5)

								sizer_2 = wx.BoxSizer(wx.VERTICAL)

								self.title_label = wx.StaticText(self.panel_1, wx.ID_ANY, _("New recording"))
								self.title_label.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
								sizer_2.Add(self.title_label, 0, wx.BOTTOM, 5)

								grid_sizer_2 = wx.FlexGridSizer(3, 2, 0, 5)
								sizer_2.Add(grid_sizer_2, 1, wx.EXPAND, 0)

								label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Event:"))
								grid_sizer_2.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

								self.event_name_text = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_LEFT)
								grid_sizer_2.Add(self.event_name_text, 1, wx.EXPAND, 0)

								label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Service:"))
								grid_sizer_2.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.FIXED_MINSIZE, 0)

								self.service_name_text = wx.TextCtrl(self.panel_1, wx.ID_ANY, _("test"), style=wx.TE_READONLY)
								grid_sizer_2.Add(self.service_name_text, 1, wx.EXPAND, 0)

								label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Start:"))
								grid_sizer_2.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)

								grid_sizer_3 = wx.FlexGridSizer(1, 4, 0, 5)
								grid_sizer_2.Add(grid_sizer_3, 1, wx.FIXED_MINSIZE, 0)

								self.startdate_datepicker = DatePickerCtrl(self.panel_1, wx.ID_ANY)
								grid_sizer_3.Add(self.startdate_datepicker, 1, wx.ALIGN_CENTER_VERTICAL, 0)

								self.starttime_text = TimeTextCtrl(self.panel_1, wx.ID_ANY, "")
								grid_sizer_3.Add(self.starttime_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)

								label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Duration:"))
								grid_sizer_3.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)

								self.duration_text = DurationTextCtrl(self.panel_1, wx.ID_ANY, "")
								grid_sizer_3.Add(self.duration_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)

								sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
								sizer_2.Add(sizer_4, 0, wx.ALIGN_RIGHT | wx.FIXED_MINSIZE | wx.TOP, 20)

								self.cancel = wx.Button(self.panel_1, wx.ID_ANY, _("Cancel"))
								sizer_4.Add(self.cancel, 1, 0, 0)

								self.ok = wx.Button(self.panel_1, wx.ID_ANY, _("OK"))
								self.ok.SetFocus()
								sizer_4.Add(self.ok, 1, 0, 0)

								grid_sizer_3.AddGrowableCol(0)
								grid_sizer_3.AddGrowableCol(1)

								grid_sizer_2.AddGrowableRow(0)
								grid_sizer_2.AddGrowableCol(0)
								grid_sizer_2.AddGrowableCol(1)

								self.panel_1.SetSizer(sizer_2)

								sizer_1.AddGrowableCol(0)
								self.SetSizer(sizer_1)
								sizer_1.Fit(self)

								self.Layout()

								self.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.ID_CANCEL), self.cancel)
								self.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.ID_OK), self.ok)
								# end wxGlade

# end of class RecordDialog_

class NeumoDialogs(wx.App):
				def OnInit(self):
								self.record_dialog = RecordDialog_(None, wx.ID_ANY, "")
								self.SetTopWindow(self.record_dialog)
								self.record_dialog.ShowModal()
								self.record_dialog.Destroy()
								return True

# end of class NeumoDialogs

if __name__ == "__main__":
				gettext.install("neumo_dialogs") # replace with the appropriate catalog name

				neumo_dialogs = NeumoDialogs(0)
				neumo_dialogs.MainLoop()
