#!/usr/bin/python3
# Neumo dvb (C) 2019-2021 deeptho@gmail.com
# Copyright notice:
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
import wx
import wx.grid
import sys
import os
import copy
from collections import namedtuple, OrderedDict
import numbers
import datetime
from dateutil import tz
import regex as re

from neumodvb import neumodbutils
from neumodvb.util import setup, lastdot
from neumodvb.neumolist import NeumoTable, NeumoGridBase, IconRenderer, MyColLabelRenderer, lnb_network_str
from neumodvb.neumo_dialogs import ShowMessage, ShowOkCancel
from neumodvb.util import dtdebug, dterror
from neumodvb.lnbnetwork_dialog import  LnbNetworkDialog
from neumodvb.lnbnetworklist import LnbNetworkGrid

import pychdb


def has_network(lnb, sat_pos):
    for n in lnb.networks:
        if n.sat_pos == sat_pos:
            return True
    return False

def has_network_with_usals(lnb, usals_pos):
    for n in lnb.networks:
        if n.usals_pos == usals_pos:
            return True
    return False

def get_network(lnb, sat_pos):
    for n in lnb.networks:
        if n.sat_pos == sat_pos:
            return n
    return None

def get_current_network(lnb):
    for n in lnb.networks:
        if n.usals_pos == lnb.usals_pos:
            return n
    return None

class LnbTable(NeumoTable):
    CD = NeumoTable.CD
    datetime_fn =  lambda x: datetime.datetime.fromtimestamp(x[1], tz=tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    lnbnetwork_fn =  lambda x: '; '.join([ pychdb.sat_pos_str(network.sat_pos) for network in x[1]])
    lof_offset_fn =  lambda x: '; '.join([ f'{int(x[0].lof_offsets[i])}kHz' for i in range(len(x[0].lof_offsets))]) if len(x[0].lof_offsets)>0 else ''
    all_columns = \
        [CD(key='k.adapter_no',  label='adapter', basic=True),
         CD(key='k.dish_id',  label='dish', basic=True, readonly=False),
         CD(key='k.lnb_id',  label='ID', basic=False, readonly=True),
         CD(key='usals_pos',  label='usals_pos', basic=True, no_combo = True, #allow entering sat_pos
            dfn= lambda x: pychdb.sat_pos_str(x[1])),
         CD(key='enabled',   label='enabled', basic=False),
         CD(key='rotor_control',  label='rotor', basic=False, dfn=lambda x: lastdot(x), example='ROTOR TYPE USALS'),
         CD(key='diseqc_10',  label='diseqc 10'),
         CD(key='diseqc_11',  label='diseqc 11'),
         CD(key='diseqc_mini',  label='diseqc mini'),
         CD(key='tune_string',  label='tune_string'),
         CD(key='k.lnb_type',  label='LNB type', dfn=lambda x: lastdot(x)),
         CD(key='priority',  label='priority'),
         CD(key='lof_offsets',  label='lof_offset', dfn=lof_offset_fn, example='-2000kHz; -20000kHz'),
         CD(key='networks',   label='Networks', dfn=lnbnetwork_fn, example='19.0E; '*16),
         CD(key='freq_low',   label='low', basic=False),
         CD(key='freq_high',   label='high', basic=False),
        ]

    dvbt_columns =  \
        [CD(key='LP_code_rate', label='LP_code_rate'),
         CD(key='bandwidth', label='bandwidth'),
         CD(key='guard_interval', label='guard_interval'),
         CD(key='hierarchy', label='hierarchy'),
         CD(key='rolloff', label='rolloff'),
         CD(key='transmission_mode', label='transmission_mode')]

    def __init__(self, parent, basic=False, *args, **kwds):
        initial_sorted_column = 'k.adapter_no'
        data_table= pychdb.lnb
        super().__init__(*args, parent=parent, basic=basic, db_t=pychdb, data_table = data_table,
                         record_t=pychdb.lnb.lnb,
                         initial_sorted_column = initial_sorted_column,
                         **kwds)

    def matching_sat(self, txn, sat_pos):
        sats = wx.GetApp().get_sats()
        if len(sats) == 0:
            from neumodvb.init_db import load_sats
            dtdebug("Empty database; adding sats")
            load_sats(txn)
        for sat in sats:
            if sat.sat_pos == sat_pos:
                return sat_pos
        return pychdb.sat.sat_pos_none

    def __save_record__(self, txn, lnb):
        if lnb.k.adapter_no <0:
            ShowMessage("Bad data", "Enter a valid adapter number before saving")
            return
            dtdebug("Will not save invalid lnb!")
            return
        if lnb.usals_pos !=  pychdb.sat.sat_pos_none and len(lnb.networks)==0:
            #shortcut: a single network can be created by entering sat_pos
            network = pychdb.lnb_network.lnb_network()
            network.sat_pos = lnb.usals_pos
            network.usals_pos = lnb.usals_pos
            pychdb.lnb.add_network(lnb, network)
        for n in lnb.networks:
            if self.matching_sat(txn, n.sat_pos) == pychdb.sat.sat_pos_none:
                ss = pychdb.sat_pos_str(n.sat_pos)
                add = ShowOkCancel("Add satellite?", f"No sat yet for position={ss}; add one?")
                if not add:
                    return
                sat = pychdb.sat.sat()
                sat.sat_pos = n.sat_pos;
                pychdb.put_record(txn, sat)
        if len(lnb.networks) == 0:
            dtdebug (f"No network defined on this lnb; silently skip saving")
        else:
            pychdb.lnb.make_unique_if_template(txn, lnb)
            pychdb.put_record(txn, lnb)
        return lnb

    def __new_record__(self):
        ret=self.record_t()
        return ret

class LnbGridBase(NeumoGridBase):
    def __init__(self, basic, readonly, *args, **kwds):
        table = LnbTable(self, basic)
        self.lnb = None #lnb for which networks will be edited
        super().__init__(basic, readonly, table, *args, **kwds)
        self.sort_order = 0
        self.sort_column = None
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClicked)

    def CheckShowNetworkDialog(self, evt, rowno, colno):
        if self.table.columns[colno].key == 'networks' and \
                    self.GetGridCursorRow() == rowno:
            if not hasattr(self, 'dlg'):
                readonly = not  self.GetParent().GetParent().edit_mode
                basic = False
                self.dlg = LnbNetworkDialog(self.GetParent(), title="Networks", basic=basic, readonly=readonly)
            else:
                pass
            self.dlg.Prepare(self)
            self.dlg.ShowModal()
            self.dlg.Destroy()
            del self.dlg
            return True
        else:
            return False

    def OnKeyDown(self, evt):
        """
        After editing, move cursor right
        """
        keycode = evt.GetKeyCode()
        if keycode == wx.WXK_RETURN  and not evt.HasAnyModifiers():
            rowno = self.GetGridCursorRow()
            colno = self.GetGridCursorCol()
            self.CheckShowNetworkDialog(evt, rowno, colno)
        else:
            evt.Skip(True)

    def OnLeftClicked(self, evt):
        """
        Create and display a popup menu on right-click event
        """
        colno = evt.GetCol()
        rowno = evt.GetRow()
        if self.CheckShowNetworkDialog(evt, rowno, colno):
            evt.Skip(False)
        else:
            evt.Skip(True)

    def CmdTune(self, evt):
        row = self.GetGridCursorRow()
        lnb = self.table.screen.record_at_row(row)
        network = get_current_network(lnb)
        if network is None:
            ShowMessage("No ref mux", "Cannot find a ref mux")
            return
        txn = self.table.db.wtxn()
        mux = pychdb.dvbs_mux.find_by_key(txn, network.ref_mux)
        txn.abort()
        mux_name= f"{int(mux.frequency/1000)}{lastdot(mux.pol).replace('POL','')}"
        dtdebug(f'CmdTune requested for row={row}: PLAY mux={mux_name}')
        self.table.SaveModified()
        self.app.MuxTune(mux)

    def OnPositioner(self, evt):
        """
        todo: mux,sat can be incompatible with lnb, in case lnb has no diseqc enabled
        This should be discovered by checking if sat is present in lnb.networks.
        We should NOT check for lnb.sat_id, as this will be removed later. lnb.sat_id
        only serves to distinghuish multiple lnbs on the same (usually fixed) dish
        """
        row = self.GetGridCursorRow()
        lnb = self.table.screen.record_at_row(row)
        dtdebug(f'Positioner requested for lnb={lnb}')
        from neumodvb.positioner_dialog import show_positioner_dialog
        show_positioner_dialog(self, lnb=lnb)
        self.table.SaveModified()
        #self.app.MuxTune(mux)

    def CmdSpectrum(self, evt):
        """
        todo: mux,sat can be incompatible with lnb, in case lnb has no diseqc enabled
        This should be discovered by checking if sat is present in lnb.networks.
        We should NOT check for lnb.sat_id, as this will be removed later. lnb.sat_id
        only serves to distinghuish multiple lnbs on the same (usually fixed) dish
        """
        row = self.GetGridCursorRow()
        lnb = self.table.screen.record_at_row(row)
        dtdebug(f'Spectrum requested for lnb={lnb}')
        self.table.SaveModified()
        from neumodvb.spectrum_dialog import show_spectrum_dialog
        show_spectrum_dialog(self, lnb=lnb)

    def OnRowSelectOFF(self, rowno):
        self.selected_row = rowno

    def CurrentLnb(self):
        assert self.selected_row is not None
        assert self.selected_row < self.table.GetNumberRows()
        lnb = self.table.GetRow(self.selected_row)
        dtdebug(f'CURRENT LNB: sel={self.selected_row} {lnb}  {len(lnb.networks)}')
        return lnb

    def set_networks(self, networks):
        """ Called from lnbnetworklist after editing
        """
        rowno =self.GetGridCursorRow()
        rec =  self.table.CurrentlySelectedRecord()
        oldrecord = rec.copy()
        rec.networks = networks
        # be careful: self.data[rowno].field will operate on a copy of self.data[rowno]
        # we cannot use return value policy reference for vectors (data moves in memory on resize)
        self.table.Backup("edit", rowno, oldrecord, rec)
        dtdebug("SET NETWORKS {}= {} => {}".format(rowno, lnb_network_str(oldrecord.networks), lnb_network_str(rec.networks)))


class BasicLnbGrid(LnbGridBase):
    def __init__(self, *args, **kwds):
        super().__init__(True, True, *args, **kwds)
        if False:
            self.SetSelectionMode(wx.grid.Grid.GridSelectionModes.GridSelectRows)
        else:
            self.SetSelectionMode(wx.grid.Grid.SelectRows)


class LnbGrid(LnbGridBase):
    def __init__(self, *args, **kwds):
        super().__init__(False, False, *args, **kwds)
