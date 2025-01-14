#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Wed Jul 27 17:52:15 2022
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from neumodvb import positioner_dialog
from neumodvb.neumowidgets import BarGauge
from neumodvb.neumoplot import ConstellationPlot
from neumodvb.positioner_muxgrid import PositionerDvbsMuxGrid
from neumodvb.muxlist_combo import DvbsMuxListComboCtrl
from neumodvb.satlist_combo import SatListComboCtrl
from neumodvb.lnblist_combo import LnbListComboCtrl
from neumodvb.neumowidgets import DiseqcChoice
# end wxGlade


class SignalPanel_(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SignalPanel_.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.SetMinSize((480, -1))

        signal_panel_sizer = wx.GridBagSizer(8, 8)

        indicators_sizer = wx.FlexGridSizer(3, 3, 2, 4)
        signal_panel_sizer.Add(indicators_sizer, (0, 0), (1, 1), wx.ALL | wx.EXPAND, 0)

        label_2 = wx.StaticText(self, wx.ID_ANY, _("RF Level"), style=wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE)
        indicators_sizer.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)

        self.rf_level_gauge = BarGauge(self, wx.ID_ANY, 100)
        indicators_sizer.Add(self.rf_level_gauge, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 4)

        self.rf_level_text = wx.StaticText(self, wx.ID_ANY, _("-48.1 dB"))
        indicators_sizer.Add(self.rf_level_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 4)

        self.label_6 = wx.StaticText(self, wx.ID_ANY, _("SNR"))
        indicators_sizer.Add(self.label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)

        self.snr_gauge = BarGauge(self, wx.ID_ANY, 100)
        indicators_sizer.Add(self.snr_gauge, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 4)

        self.snr_text = wx.StaticText(self, wx.ID_ANY, _("-48.1 dB"))
        indicators_sizer.Add(self.snr_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 4)

        label_8 = wx.StaticText(self, wx.ID_ANY, _("BER"))
        indicators_sizer.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)

        self.ber_gauge = BarGauge(self, wx.ID_ANY, 100)
        indicators_sizer.Add(self.ber_gauge, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 4)

        self.ber_text = wx.StaticText(self, wx.ID_ANY, _("-48.1 dB"))
        indicators_sizer.Add(self.ber_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        self.freq_sr_sizer = wx.FlexGridSizer(1, 2, 0, 0)
        signal_panel_sizer.Add(self.freq_sr_sizer, (1, 0), (1, 1), wx.EXPAND, 0)

        self.sat_pos_text = wx.StaticText(self, wx.ID_ANY, "")
        self.sat_pos_text.SetFont(wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Sans"))
        self.freq_sr_sizer.Add(self.sat_pos_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 2)

        self.freq_sr_modulation_text = wx.StaticText(self, wx.ID_ANY, "")
        self.freq_sr_sizer.Add(self.freq_sr_modulation_text, 2, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)

        status_sizer = wx.FlexGridSizer(1, 7, 0, 5)
        signal_panel_sizer.Add(status_sizer, (2, 0), (1, 1), wx.EXPAND, 0)

        self.has_carrier = wx.StaticText(self, wx.ID_ANY, _("carrier"))
        self.has_carrier.SetForegroundColour(wx.Colour(255, 0, 0))
        status_sizer.Add(self.has_carrier, 0, 0, 0)

        self.has_timing_lock = wx.StaticText(self, wx.ID_ANY, _("tmg"))
        self.has_timing_lock.SetForegroundColour(wx.Colour(255, 0, 0))
        status_sizer.Add(self.has_timing_lock, 0, 0, 0)

        self.has_fec = wx.StaticText(self, wx.ID_ANY, _("fec"))
        self.has_fec.SetForegroundColour(wx.Colour(255, 0, 0))
        status_sizer.Add(self.has_fec, 0, 0, 0)

        self.has_lock = wx.StaticText(self, wx.ID_ANY, _("lock"))
        self.has_lock.SetForegroundColour(wx.Colour(255, 0, 0))
        status_sizer.Add(self.has_lock, 0, 0, 0)

        self.has_sync = wx.StaticText(self, wx.ID_ANY, _("sync"))
        self.has_sync.SetForegroundColour(wx.Colour(255, 0, 0))
        status_sizer.Add(self.has_sync, 0, 0, 0)

        label_14 = wx.StaticText(self, wx.ID_ANY, _("LNB LOF offset:"), style=wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE)
        status_sizer.Add(label_14, 0, wx.EXPAND | wx.LEFT, 10)

        self.lnb_lof_offset_text = wx.StaticText(self, wx.ID_ANY, "")
        status_sizer.Add(self.lnb_lof_offset_text, 0, wx.LEFT, 5)

        grid_sizer_16 = wx.FlexGridSizer(1, 2, 4, 0)
        signal_panel_sizer.Add(grid_sizer_16, (3, 0), (1, 1), wx.EXPAND, 0)

        label_15 = wx.StaticText(self, wx.ID_ANY, _("MATYPE:"))
        grid_sizer_16.Add(label_15, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.matype_pls_text = wx.StaticText(self, wx.ID_ANY, "")
        grid_sizer_16.Add(self.matype_pls_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        isi_sizer = wx.FlexGridSizer(1, 2, 4, 0)
        signal_panel_sizer.Add(isi_sizer, (4, 0), (1, 1), wx.EXPAND, 0)

        label_16 = wx.StaticText(self, wx.ID_ANY, _("ISI:"))
        isi_sizer.Add(label_16, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.isi_list_text = wx.StaticText(self, wx.ID_ANY, "")
        isi_sizer.Add(self.isi_list_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        grid_sizer_6 = wx.FlexGridSizer(1, 3, 0, 3)
        signal_panel_sizer.Add(grid_sizer_6, (5, 0), (1, 1), wx.EXPAND, 0)

        grid_sizer_6.Add((0, 0), 0, 0, 0)

        grid_sizer_6.Add((0, 0), 0, 0, 0)

        self.speak_toggle = wx.ToggleButton(self, wx.ID_ANY, _("Speak"))
        self.speak_toggle.SetToolTip(_("Speak and thy mouth will open"))
        grid_sizer_6.Add(self.speak_toggle, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 0)

        grid_sizer_6.AddGrowableCol(0)
        grid_sizer_6.AddGrowableCol(1)

        self.freq_sr_sizer.AddGrowableCol(0)
        self.freq_sr_sizer.AddGrowableCol(1)

        indicators_sizer.AddGrowableCol(0)
        indicators_sizer.AddGrowableCol(1)
        indicators_sizer.AddGrowableCol(2)

        signal_panel_sizer.AddGrowableCol(0)
        self.SetSizer(signal_panel_sizer)

        self.Layout()

        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleSpeak, self.speak_toggle)
        # end wxGlade

    def OnToggleSpeak(self, event):  # wxGlade: SignalPanel_.<event_handler>
        print("Event handler 'OnToggleSpeak' not implemented!")
        event.Skip()

# end of class SignalPanel_

class Panel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wx.Panel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.Layout()
        # end wxGlade

# end of class wx.Panel

class TuneMuxPanel_(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: TuneMuxPanel_.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)

        sizer_19 = wx.FlexGridSizer(2, 1, 10, 0)

        grid_sizer_3 = wx.FlexGridSizer(1, 3, 0, 10)
        sizer_19.Add(grid_sizer_3, 1, 0, 0)

        self.panel_3 = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_3.Add(self.panel_3, 1, wx.EXPAND, 0)

        sizer_6 = wx.FlexGridSizer(2, 1, 0, 0)

        label_22 = wx.StaticText(self.panel_3, wx.ID_ANY, _("LNB and Sat"))
        label_22.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_6.Add(label_22, 0, wx.BOTTOM, 5)

        grid_sizer_7 = wx.FlexGridSizer(4, 2, 10, 5)
        sizer_6.Add(grid_sizer_7, 0, 0, 0)

        label_1b = wx.StaticText(self.panel_3, wx.ID_ANY, _("LNB:"), style=wx.ALIGN_LEFT)
        label_1b.SetToolTip(_("LNB controlling positioner"))
        grid_sizer_7.Add(label_1b, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.positioner_lnb_sel = LnbListComboCtrl(self.panel_3, wx.ID_ANY, "", style=wx.TE_DONTWRAP | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.positioner_lnb_sel.SetToolTip(_("LNB to control positioner and to tune mux"))
        grid_sizer_7.Add(self.positioner_lnb_sel, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_1c = wx.StaticText(self.panel_3, wx.ID_ANY, _("Sat:"))
        label_1c.SetToolTip(_("Satellite for saving dseqcs data (USALS correction and diseqc12 position)"))
        grid_sizer_7.Add(label_1c, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.positioner_sat_sel = SatListComboCtrl(self.panel_3, wx.ID_ANY, "", style=wx.TE_DONTWRAP | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.positioner_sat_sel.SetToolTip(_("Satellite position for which to edit LNB usals position"))
        grid_sizer_7.Add(self.positioner_sat_sel, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_1c1 = wx.StaticText(self.panel_3, wx.ID_ANY, _("Lnb:"))
        label_1c1.SetToolTip(_("Save the currently selected LNB data, and set the currently selected mux as reference mux"))
        grid_sizer_7.Add(label_1c1, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.ok_button = wx.Button(self.panel_3, wx.ID_SAVE, "")
        self.ok_button.SetToolTip(_("Save Control type, usals correction, diseqc12 position and reference mux for this satellite and LNB."))
        grid_sizer_7.Add(self.ok_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 0)

        grid_sizer_7.Add((0, 0), 0, 0, 0)

        self.reset_lof_offset_button = wx.Button(self.panel_3, wx.ID_ANY, _("Reset LOF"))
        self.reset_lof_offset_button.SetToolTip(_("Reset Local oscillator offset"))
        grid_sizer_7.Add(self.reset_lof_offset_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 0)

        self.si_info_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        self.si_info_panel.SetMinSize((480, -1))
        self.si_info_panel.SetToolTip(_("Information retrieved from driver and from SI stream on mux"))
        grid_sizer_3.Add(self.si_info_panel, 1, wx.EXPAND, 0)

        sizer_190 = wx.FlexGridSizer(2, 1, 10, 0)

        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_190.Add(sizer_7, 1, wx.EXPAND, 0)

        label_9 = wx.StaticText(self.si_info_panel, wx.ID_ANY, _("Service Information"))
        label_9.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_7.Add(label_9, 1, wx.EXPAND, 0)

        grid_sizer_15 = wx.FlexGridSizer(6, 2, 3, 20)
        sizer_190.Add(grid_sizer_15, 1, wx.EXPAND, 0)

        label_10 = wx.StaticText(self.si_info_panel, wx.ID_ANY, _("SI:"), style=wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE)
        grid_sizer_15.Add(label_10, 0, wx.RIGHT, 10)

        si_status_sizer = wx.FlexGridSizer(1, 5, 0, 10)
        grid_sizer_15.Add(si_status_sizer, 0, wx.EXPAND, 0)

        self.status_pat = wx.StaticText(self.si_info_panel, wx.ID_ANY, _("PAT"))
        self.status_pat.SetForegroundColour(wx.Colour(192, 192, 192))
        si_status_sizer.Add(self.status_pat, 0, 0, 0)

        self.status_nit = wx.StaticText(self.si_info_panel, wx.ID_ANY, _("NIT"))
        self.status_nit.SetForegroundColour(wx.Colour(192, 192, 192))
        si_status_sizer.Add(self.status_nit, 0, 0, 0)

        self.status_sdt = wx.StaticText(self.si_info_panel, wx.ID_ANY, _("SDT"))
        self.status_sdt.SetForegroundColour(wx.Colour(192, 192, 192))
        si_status_sizer.Add(self.status_sdt, 0, 0, 0)

        self.status_fail = wx.StaticText(self.si_info_panel, wx.ID_ANY, "")
        self.status_fail.SetForegroundColour(wx.Colour(255, 0, 0))
        si_status_sizer.Add(self.status_fail, 0, 0, 0)

        self.status_si_done = wx.StaticText(self.si_info_panel, wx.ID_ANY, "")
        self.status_si_done.SetForegroundColour(wx.Colour(0, 0, 255))
        si_status_sizer.Add(self.status_si_done, 0, 0, 0)

        label_7 = wx.StaticText(self.si_info_panel, wx.ID_ANY, _("NIT:"), style=wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE)
        grid_sizer_15.Add(label_7, 0, wx.RIGHT, 10)

        self.grid_sizer_14 = wx.FlexGridSizer(1, 2, 5, 0)
        grid_sizer_15.Add(self.grid_sizer_14, 0, wx.EXPAND, 0)

        self.si_freq_text = wx.StaticText(self.si_info_panel, wx.ID_ANY, "")
        self.grid_sizer_14.Add(self.si_freq_text, 0, wx.EXPAND, 0)

        self.si_symbolrate_text = wx.StaticText(self.si_info_panel, wx.ID_ANY, "")
        self.grid_sizer_14.Add(self.si_symbolrate_text, 0, wx.EXPAND, 0)

        self.si_nit_ids_text = wx.StaticText(self.si_info_panel, wx.ID_ANY, "")
        grid_sizer_15.Add(self.si_nit_ids_text, 0, wx.LEFT, 5)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        grid_sizer_15.Add((0, 0), 0, 0, 0)

        self.constellation_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_3.Add(self.constellation_panel, 0, wx.EXPAND, 0)

        sizer_3333 = wx.BoxSizer(wx.VERTICAL)

        label_2345 = wx.StaticText(self.constellation_panel, wx.ID_ANY, _("Constellation"))
        label_2345.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_3333.Add(label_2345, 0, 0, 0)

        self.constellation_plot = ConstellationPlot(self.constellation_panel, wx.ID_ANY)
        sizer_3333.Add(self.constellation_plot, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.SHAPED, 0)

        self.constellation_toggle = wx.ToggleButton(self.constellation_panel, wx.ID_ANY, _("Update"))
        self.constellation_toggle.SetToolTip(_("Update constellation plot"))
        sizer_3333.Add(self.constellation_toggle, 0, wx.ALL | wx.FIXED_MINSIZE, 0)

        self.panel_1 = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        sizer_19.Add(self.panel_1, 1, wx.EXPAND, 0)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_21 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Tune mux"))
        label_21.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_1.Add(label_21, 0, wx.BOTTOM, 3)

        grid_sizer_11 = wx.FlexGridSizer(2, 1, 0, 0)
        sizer_1.Add(grid_sizer_11, 0, 0, 0)

        grid_sizer_12 = wx.FlexGridSizer(1, 7, 0, 5)
        grid_sizer_11.Add(grid_sizer_12, 1, wx.EXPAND, 0)

        self.positioner_mux_sel = DvbsMuxListComboCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_DONTWRAP | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        grid_sizer_12.Add(self.positioner_mux_sel, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.tune_reset_button = wx.Button(self.panel_1, wx.ID_ANY, _("Reset"), style=wx.BU_EXACTFIT)
        self.tune_reset_button.SetToolTip(_("Reset mux data to the values from the mux selected in the dropdown list"))
        grid_sizer_12.Add(self.tune_reset_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        grid_sizer_12.Add((20, 20), 0, 0, 0)

        self.tune_button = wx.Button(self.panel_1, wx.ID_ANY, _("Tune"), style=wx.BU_EXACTFIT)
        self.tune_button.SetToolTip(_("Tune the mux using the tuning parameters below"))
        grid_sizer_12.Add(self.tune_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.blind_toggle = wx.ToggleButton(self.panel_1, wx.ID_ANY, _("Blind"), style=wx.BU_EXACTFIT)
        self.blind_toggle.SetToolTip(_("Blindscan - if set, only frequency and polarisation need to be entered"))
        grid_sizer_12.Add(self.blind_toggle, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.tune_abort_button = wx.Button(self.panel_1, wx.ID_ANY, _("Abort"), style=wx.BU_EXACTFIT)
        self.tune_abort_button.SetToolTip(_("Stop tuning and go to idle"))
        grid_sizer_12.Add(self.tune_abort_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.pls_search_button = wx.Button(self.panel_1, wx.ID_ANY, _("PLS. Srch."), style=wx.BU_EXACTFIT)
        self.pls_search_button.SetToolTip(_("Search pls codes (can take long time)"))
        grid_sizer_12.Add(self.pls_search_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        grid_sizer_13 = wx.FlexGridSizer(1, 1, 16, 0)
        grid_sizer_11.Add(grid_sizer_13, 1, wx.EXPAND, 0)

        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        grid_sizer_13.Add(self.panel_2, 1, wx.EXPAND, 0)

        sizer_20 = wx.BoxSizer(wx.VERTICAL)

        self.muxedit_grid = PositionerDvbsMuxGrid(self.panel_2, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_VRULES)
        self.muxedit_grid.SetFocus()
        sizer_20.Add(self.muxedit_grid, 0, wx.EXPAND, 0)

        self.panel_2.SetSizer(sizer_20)

        grid_sizer_12.AddGrowableRow(0)
        grid_sizer_12.AddGrowableCol(0)

        grid_sizer_11.AddGrowableRow(1)
        grid_sizer_11.AddGrowableCol(0)

        self.panel_1.SetSizer(sizer_1)

        self.constellation_panel.SetSizer(sizer_3333)

        self.grid_sizer_14.AddGrowableCol(0)
        self.grid_sizer_14.AddGrowableCol(1)

        grid_sizer_15.AddGrowableCol(1)

        sizer_190.AddGrowableRow(1)
        sizer_190.AddGrowableCol(0)
        self.si_info_panel.SetSizer(sizer_190)

        self.panel_3.SetSizer(sizer_6)

        grid_sizer_3.AddGrowableCol(1)
        grid_sizer_3.AddGrowableCol(2)

        sizer_19.AddGrowableCol(0)
        self.SetSizer(sizer_19)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.OnSave, self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.OnResetLof, self.reset_lof_offset_button)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleConstellation, self.constellation_toggle)
        self.Bind(wx.EVT_BUTTON, self.OnResetTune, self.tune_reset_button)
        self.Bind(wx.EVT_BUTTON, self.OnTune, self.tune_button)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleBlindscan, self.blind_toggle)
        self.Bind(wx.EVT_BUTTON, self.OnAbortTune, self.tune_abort_button)
        self.Bind(wx.EVT_BUTTON, self.OnSearchPls, self.pls_search_button)
        # end wxGlade

    def OnSave(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnSave' not implemented!")
        event.Skip()

    def OnResetLof(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnResetLof' not implemented!")
        event.Skip()

    def OnToggleConstellation(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnToggleConstellation' not implemented!")
        event.Skip()

    def OnResetTune(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnResetTune' not implemented!")
        event.Skip()

    def OnTune(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnTune' not implemented!")
        event.Skip()

    def OnToggleBlindscan(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnToggleBlindscan' not implemented!")
        event.Skip()

    def OnAbortTune(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnAbortTune' not implemented!")
        event.Skip()

    def OnSearchPls(self, event):  # wxGlade: TuneMuxPanel_.<event_handler>
        print("Event handler 'OnSearchPls' not implemented!")
        event.Skip()

# end of class TuneMuxPanel_

class PositionerDialog_(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PositionerDialog_.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1280, 835))
        self.SetTitle(_("Positioner"))

        grid_sizer_1 = wx.FlexGridSizer(3, 1, 5, 0)

        label_5 = wx.StaticText(self, wx.ID_ANY, _("Positioner control"))
        label_5.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_4 = wx.FlexGridSizer(1, 4, 5, 10)
        grid_sizer_1.Add(grid_sizer_4, 1, wx.ALL, 8)

        grid_sizer_18 = wx.FlexGridSizer(2, 1, 5, 0)
        grid_sizer_4.Add(grid_sizer_18, 1, wx.EXPAND, 0)

        self.motor_control_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_18.Add(self.motor_control_panel, 1, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.VERTICAL)

        label_24 = wx.StaticText(self.motor_control_panel, wx.ID_ANY, _("Motor control"))
        label_24.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_5.Add(label_24, 0, wx.BOTTOM, 3)

        self.diseqc_type_choice = DiseqcChoice(self.motor_control_panel, wx.ID_ANY, choices=[_("Disabled"), _("USALS"), _("DISEQC2"), ""])
        self.diseqc_type_choice.SetToolTip(_("Enable/disable positioner for this LNB and select control type"))
        self.diseqc_type_choice.SetSelection(0)
        sizer_5.Add(self.diseqc_type_choice, 0, wx.ALL, 10)

        self.direct_motor_control_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_18.Add(self.direct_motor_control_panel, 1, wx.EXPAND | wx.RIGHT, 2)

        grid_sizer2 = wx.FlexGridSizer(3, 3, 4, 4)

        self.step_east_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("Step East"))
        self.step_east_button.SetToolTip(_("Step east by motor command"))
        self.step_east_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, (16, 16)))
        grid_sizer2.Add(self.step_east_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.halt_motor_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("Halt"))
        self.halt_motor_button.SetToolTip(_("Stop USALS if it is moving"))
        grid_sizer2.Add(self.halt_motor_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.FIXED_MINSIZE, 0)

        self.step_west_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("Step West"))
        self.step_west_button.SetToolTip(_("Step west by motor command"))
        self.step_west_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_OTHER, (16, 16)), dir=wx.RIGHT)
        grid_sizer2.Add(self.step_west_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.goto_east_toggle = wx.ToggleButton(self.direct_motor_control_panel, wx.ID_ANY, _("Go East"))
        self.goto_east_toggle.SetToolTip(_("Move east continously"))
        self.goto_east_toggle.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GOTO_FIRST, wx.ART_FRAME_ICON, (16, 16)))
        grid_sizer2.Add(self.goto_east_toggle, 0, 0, 0)

        self.goto_ref_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("Go Ref"))
        self.goto_ref_button.SetToolTip(_("Goto  motor's reference (due south)"))
        self.goto_ref_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_FRAME_ICON, (16, 16)))
        grid_sizer2.Add(self.goto_ref_button, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.goto_west_toggle = wx.ToggleButton(self.direct_motor_control_panel, wx.ID_ANY, _("Go West"))
        self.goto_west_toggle.SetToolTip(_("Move west continously"))
        self.goto_west_toggle.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GOTO_LAST, wx.ART_OTHER, (16, 16)))
        grid_sizer2.Add(self.goto_west_toggle, 0, wx.ALIGN_RIGHT, 0)

        self.set_east_limit_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("Set East"))
        self.set_east_limit_button.SetToolTip(_("Set east limit"))
        self.set_east_limit_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, (16, 16)))
        grid_sizer2.Add(self.set_east_limit_button, 0, 0, 0)

        self.no_limits_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("No limits"))
        self.no_limits_button.SetToolTip(_("Disable limits"))
        self.no_limits_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_REMOVABLE, wx.ART_FRAME_ICON, (16, 16)))
        grid_sizer2.Add(self.no_limits_button, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.set_west_limit_button = wx.Button(self.direct_motor_control_panel, wx.ID_ANY, _("Set West"))
        self.set_west_limit_button.SetToolTip(_("Set west limit"))
        self.set_west_limit_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_FRAME_ICON, (16, 16)), dir=wx.RIGHT)
        grid_sizer2.Add(self.set_west_limit_button, 0, wx.ALIGN_RIGHT, 0)

        self.diseqc12_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_4.Add(self.diseqc12_panel, 1, wx.EXPAND, 0)

        sizer_9 = wx.BoxSizer(wx.VERTICAL)

        label_19 = wx.StaticText(self.diseqc12_panel, wx.ID_ANY, _("Diseqc1.2"))
        label_19.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_9.Add(label_19, 0, wx.BOTTOM, 3)

        grid_sizer_9 = wx.FlexGridSizer(3, 1, 5, 10)
        sizer_9.Add(grid_sizer_9, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 8)

        self.store_position_button = wx.Button(self.diseqc12_panel, wx.ID_ANY, _("Store pos."))
        self.store_position_button.SetToolTip(_("Store the current position at the specified diseqc1.2 index"))
        self.store_position_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, (16, 16)))
        grid_sizer_9.Add(self.store_position_button, 1, 0, 0)

        self.diseqc_position_spin_ctrl = positioner_dialog.Diseqc12SpinCtrl(self.diseqc12_panel, wx.ID_ANY , style=wx.SP_ARROW_KEYS | wx.SP_VERTICAL)
        self.diseqc_position_spin_ctrl.SetToolTip(_("Diseqc1.2 index for current position"))
        grid_sizer_9.Add(self.diseqc_position_spin_ctrl, 1, wx.ALIGN_CENTER, 0)

        self.goto_position_button = wx.Button(self.diseqc12_panel, wx.ID_ANY, _("Goto pos."))
        self.goto_position_button.SetToolTip(_("Goto sat at Diseqc1.2 position"))
        self.goto_position_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16)))
        grid_sizer_9.Add(self.goto_position_button, 1, 0, 0)

        self.usals_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_4.Add(self.usals_panel, 1, wx.EXPAND, 0)

        sizer_11 = wx.BoxSizer(wx.VERTICAL)

        label_23 = wx.StaticText(self.usals_panel, wx.ID_ANY, _("USALS control"))
        label_23.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_11.Add(label_23, 0, wx.BOTTOM, 3)

        grid_sizer2b = wx.FlexGridSizer(4, 3, 4, 4)
        sizer_11.Add(grid_sizer2b, 1, wx.EXPAND, 4)

        self.usals_step_east_button = wx.Button(self.usals_panel, wx.ID_ANY, _("East"))
        self.usals_step_east_button.SetToolTip(_("Step east by the specified amount"))
        self.usals_step_east_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, (16, 16)), dir=wx.RIGHT)
        grid_sizer2b.Add(self.usals_step_east_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE, 0)

        self.rotor_position_text_ctrl = wx.TextCtrl(self.usals_panel, wx.ID_ANY, _("28.2E"), style=wx.TE_CENTRE | wx.TE_PROCESS_ENTER)
        self.rotor_position_text_ctrl.SetToolTip(_("Current USALS position; press ENTER to change"))
        grid_sizer2b.Add(self.rotor_position_text_ctrl, 0, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)

        self.usals_step_west_button = wx.Button(self.usals_panel, wx.ID_ANY, _("West"))
        self.usals_step_west_button.SetToolTip(_("Step west by specified amount"))
        self.usals_step_west_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_OTHER, (16, 16)))
        grid_sizer2b.Add(self.usals_step_west_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.usals_reset_button = wx.Button(self.usals_panel, wx.ID_ANY, _("Reset"))
        self.usals_reset_button.SetToolTip(_("Reset USALS position to its original version"))
        self.usals_reset_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, (16, 16)))
        grid_sizer2b.Add(self.usals_reset_button, 0, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)

        self.rotor_step_spin_ctrl = positioner_dialog.UsalsPosSpinCtrl(self.usals_panel, wx.ID_ANY, initial=0.1, min=0.0, max=5.0, style=wx.ALIGN_CENTRE_HORIZONTAL | wx.SP_ARROW_KEYS)
        self.rotor_step_spin_ctrl.SetToolTip(_("Amount to step by"))
        self.rotor_step_spin_ctrl.SetIncrement(0.1)
        self.rotor_step_spin_ctrl.SetDigits(2)
        grid_sizer2b.Add(self.rotor_step_spin_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)

        self.usals_set_button = wx.Button(self.usals_panel, wx.ID_ANY, _("Set"))
        self.usals_set_button.SetToolTip(_("Go to current USALS position (same as ENTER)"))
        self.usals_set_button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, (16, 16)))
        grid_sizer2b.Add(self.usals_set_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)

        label_3 = wx.StaticText(self.usals_panel, wx.ID_ANY, _("Location"))
        grid_sizer2b.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)

        self.lattitude_text_ctrl = wx.TextCtrl(self.usals_panel, wx.ID_ANY, _("0.0N"), style=wx.TE_CENTRE | wx.TE_PROCESS_ENTER)
        self.lattitude_text_ctrl.SetToolTip(_("Latitude of location where dish is installed"))
        grid_sizer2b.Add(self.lattitude_text_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE | wx.RIGHT, 0)

        self.lattitude_north_south_choice = wx.Choice(self.usals_panel, wx.ID_ANY, choices=[_("North"), _("South")])
        self.lattitude_north_south_choice.SetSelection(0)
        grid_sizer2b.Add(self.lattitude_north_south_choice, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 0)

        grid_sizer2b.Add((0, 0), 0, 0, 0)

        self.longitude_text_ctrl = wx.TextCtrl(self.usals_panel, wx.ID_ANY, _("0.0E"), style=wx.TE_CENTRE | wx.TE_PROCESS_ENTER)
        self.longitude_text_ctrl.SetToolTip(_("Longitude of location where dish is installed"))
        grid_sizer2b.Add(self.longitude_text_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE | wx.LEFT, 0)

        self.longitude_east_west_choice = wx.Choice(self.usals_panel, wx.ID_ANY, choices=[_("East"), _("West")])
        self.longitude_east_west_choice.SetSelection(0)
        grid_sizer2b.Add(self.longitude_east_west_choice, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.signal_info_panel = wx.Panel(self, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        grid_sizer_4.Add(self.signal_info_panel, 0, wx.EXPAND, 0)

        sizer_2 = wx.FlexGridSizer(2, 1, 5, 0)

        label_1 = wx.StaticText(self.signal_info_panel, wx.ID_ANY, _("Signal"))
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_2.Add(label_1, 0, 0, 0)

        self.signal_panel = positioner_dialog.SignalPanel(self.signal_info_panel, wx.ID_ANY)
        sizer_2.Add(self.signal_panel, 1, wx.EXPAND, 8)

        grid_sizer_2 = wx.FlexGridSizer(1, 1, 5, 6)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.ALL | wx.EXPAND, 8)

        self.tune_mux_panel = positioner_dialog.TuneMuxPanel(self, wx.ID_ANY)
        grid_sizer_2.Add(self.tune_mux_panel, 1, wx.EXPAND, 0)

        grid_sizer_2.AddGrowableCol(0)

        sizer_2.AddGrowableRow(1)
        sizer_2.AddGrowableCol(0)
        self.signal_info_panel.SetSizer(sizer_2)

        self.usals_panel.SetSizer(sizer_11)

        self.diseqc12_panel.SetSizer(sizer_9)

        self.direct_motor_control_panel.SetSizer(grid_sizer2)

        self.motor_control_panel.SetSizer(sizer_5)

        grid_sizer_4.AddGrowableRow(0)

        grid_sizer_1.AddGrowableCol(0)
        self.SetSizer(grid_sizer_1)

        self.Layout()

        self.Bind(wx.EVT_CHOICE, self.OnDiseqcTypeChoice, self.diseqc_type_choice)
        self.Bind(wx.EVT_BUTTON, self.OnStepEast, self.step_east_button)
        self.Bind(wx.EVT_BUTTON, self.OnStopPositioner, self.halt_motor_button)
        self.Bind(wx.EVT_BUTTON, self.OnStepWest, self.step_west_button)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleGotoEast, self.goto_east_toggle)
        self.Bind(wx.EVT_BUTTON, self.OnGotoRef, self.goto_ref_button)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleGotoWest, self.goto_west_toggle)
        self.Bind(wx.EVT_BUTTON, self.OnSetEastLimit, self.set_east_limit_button)
        self.Bind(wx.EVT_BUTTON, self.OnDisableLimits, self.no_limits_button)
        self.Bind(wx.EVT_BUTTON, self.OnSetWestLimit, self.set_west_limit_button)
        self.Bind(wx.EVT_BUTTON, self.OnStorePosition, self.store_position_button)
        self.Bind(wx.EVT_BUTTON, self.OnGotoPosition, self.goto_position_button)
        self.Bind(wx.EVT_BUTTON, self.OnUsalsStepEast, self.usals_step_east_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnPositionChanged, self.rotor_position_text_ctrl)
        self.Bind(wx.EVT_BUTTON, self.OnUsalsStepWest, self.usals_step_west_button)
        self.Bind(wx.EVT_BUTTON, self.OnGotoSat, self.usals_reset_button)
        self.Bind(wx.EVT_BUTTON, self.OnGotoUsals, self.usals_set_button)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnLattitudeChanged, self.lattitude_text_ctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnLattitudeChanged, self.lattitude_text_ctrl)
        self.Bind(wx.EVT_CHOICE, self.OnLattitudeNorthSouthSelect, self.lattitude_north_south_choice)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnLongitudeChanged, self.longitude_text_ctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnLongitudeChanged, self.longitude_text_ctrl)
        self.Bind(wx.EVT_CHOICE, self.OnLongitudeEastWestSelect, self.longitude_east_west_choice)
        # end wxGlade

    def OnDiseqcTypeChoice(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnDiseqcTypeChoice' not implemented!")
        event.Skip()

    def OnStepEast(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnStepEast' not implemented!")
        event.Skip()

    def OnStopPositioner(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnStopPositioner' not implemented!")
        event.Skip()

    def OnStepWest(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnStepWest' not implemented!")
        event.Skip()

    def OnToggleGotoEast(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnToggleGotoEast' not implemented!")
        event.Skip()

    def OnGotoRef(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnGotoRef' not implemented!")
        event.Skip()

    def OnToggleGotoWest(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnToggleGotoWest' not implemented!")
        event.Skip()

    def OnSetEastLimit(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnSetEastLimit' not implemented!")
        event.Skip()

    def OnDisableLimits(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnDisableLimits' not implemented!")
        event.Skip()

    def OnSetWestLimit(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnSetWestLimit' not implemented!")
        event.Skip()

    def OnStorePosition(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnStorePosition' not implemented!")
        event.Skip()

    def OnGotoPosition(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnGotoPosition' not implemented!")
        event.Skip()

    def OnUsalsStepEast(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnUsalsStepEast' not implemented!")
        event.Skip()

    def OnPositionChanged(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnPositionChanged' not implemented!")
        event.Skip()

    def OnUsalsStepWest(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnUsalsStepWest' not implemented!")
        event.Skip()

    def OnGotoSat(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnGotoSat' not implemented!")
        event.Skip()

    def OnGotoUsals(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnGotoUsals' not implemented!")
        event.Skip()

    def OnLattitudeChanged(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnLattitudeChanged' not implemented!")
        event.Skip()

    def OnLattitudeNorthSouthSelect(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnLattitudeNorthSouthSelect' not implemented!")
        event.Skip()

    def OnLongitudeChanged(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnLongitudeChanged' not implemented!")
        event.Skip()

    def OnLongitudeEastWestSelect(self, event):  # wxGlade: PositionerDialog_.<event_handler>
        print("Event handler 'OnLongitudeEastWestSelect' not implemented!")
        event.Skip()

# end of class PositionerDialog_

class PositionerDialogs(wx.App):
    def OnInit(self):
        self.positioner_dialog = PositionerDialog_(None, wx.ID_ANY, "")
        self.SetTopWindow(self.positioner_dialog)
        self.positioner_dialog.Show()
        return True

# end of class PositionerDialogs

if __name__ == "__main__":
    gettext.install("positioner_dialog") # replace with the appropriate catalog name

    positioner_dialog = PositionerDialogs(0)
    positioner_dialog.MainLoop()
