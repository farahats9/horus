#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------#
#                                                                       #
# This file is part of the Horus Project                                #
#                                                                       #
# Copyright (C) 2014 Mundo Reader S.L.                                  #
#                                                                       #
# Date: June 2014                                                       #
# Author: Jesús Arroyo Torrens <jesus.arroyo@bq.com>                    #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                       #
#-----------------------------------------------------------------------#

__author__ = "Jesús Arroyo Torrens <jesus.arroyo@bq.com>"
__license__ = "GNU General Public License v3 http://www.gnu.org/licenses/gpl.html"

import wx
import wx.lib.scrolledpanel

from horus.util import profile

from horus.engine.scanner import *

class VideoPanel(wx.Panel):
    """
    """
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, size=(270, 0))
        
        self.scanner = Scanner.Instance()
        
        #-- Graphic elements
        imgProcStaticText = wx.StaticText(self, wx.ID_ANY, _("Image Processing"), style=wx.ALIGN_CENTRE)
        imgProcStaticText.SetFont((wx.Font(wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT).GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)))
        self.openCheckBox = wx.CheckBox(self, label=_("Open"), size=(67, -1))
        self.openSlider = wx.Slider(self, wx.ID_ANY, 0, 1, 10, size=(150, -1), style=wx.SL_LABELS)
        self.thresholdCheckBox = wx.CheckBox(self, label=_("Threshold"), size=(67, -1))
        self.thresholdSlider = wx.Slider(self, wx.ID_ANY, 20, 0, 255, size=(150, -1), style=wx.SL_LABELS)

        #roiStaticText = wx.StaticText(self, -1, _("ROI Selection"), style=wx.ALIGN_CENTRE)
        #rhoStaticText = wx.StaticText(self, -1, _("radius"), size=(45, -1), style=wx.ALIGN_CENTRE)
        #rhoSlider = wx.Slider(self, -1, 0, 0, 639, size=(150, -1), style=wx.SL_LABELS)
        #rhoSlider.Bind(wx.EVT_SLIDER, self.onROIChanged)
        #rhoSlider.Disable()
        #hStaticText = wx.StaticText(self, -1, " hight", size=(45, -1), style=wx.ALIGN_CENTRE)
        #hSlider = wx.Slider(self, -1, 0, 0, 479, size=(150, -1), style=wx.SL_LABELS)
        #hSlider.Bind(wx.EVT_SLIDER, self.OnROIChanged)
        #hSlider.Disable()

        #-- Bind
        self.Bind(wx.EVT_CHECKBOX, self.onOpenChanged, self.openCheckBox)
        self.Bind(wx.EVT_SLIDER, self.onOpenChanged, self.openSlider)
        self.Bind(wx.EVT_CHECKBOX, self.onThresholdChanged, self.thresholdCheckBox)
        self.Bind(wx.EVT_SLIDER, self.onThresholdChanged, self.thresholdSlider)

        #-- Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        vbox.Add(imgProcStaticText, 0, wx.ALL, 10)
        vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.openCheckBox, 0, wx.ALL^wx.RIGHT, 15)
        hbox.Add(self.openSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.thresholdCheckBox, 0, wx.ALL^wx.RIGHT, 15)
        hbox.Add(self.thresholdSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        
        #vbox.Add(roiStaticText, 0, wx.ALL, 10)
        #hbox = wx.BoxSizer(wx.HORIZONTAL)
        #hbox.Add(rhoStaticText, 0, wx.ALL^wx.BOTTOM, 18)
        #hbox.Add(rhoSlider, 0, wx.ALL, 0)
        #vbox.Add(hbox)
        #hbox = wx.BoxSizer(wx.HORIZONTAL)
        #hbox.Add(hStaticText, 0, wx.ALL, 18)
        #hbox.Add(hSlider, 0, wx.ALL, 0)
        #vbox.Add(hbox)
        
        self.SetSizer(vbox)
        self.Centre()

    def onOpenChanged(self, event):
        enable = self.openCheckBox.IsChecked()
        value = self.openSlider.GetValue()
        self.scanner.core.setOpen(enable, value)
        profile.putProfileSetting('open', enable)
        profile.putProfileSetting('open_value', value)

    def onThresholdChanged(self, event):
        enable = self.thresholdCheckBox.IsChecked()
        value = self.thresholdSlider.GetValue()
        self.scanner.core.setThreshold(enable, value)
        profile.putProfileSetting('threshold', enable)
        profile.putProfileSetting('threshold_value', value)

    def onROIChanged(self, event):
        pass

    def updateProfileToAllControls(self):
        self.openCheckBox.SetValue(profile.getProfileSettingBool('open'))
        self.openSlider.SetValue(profile.getProfileSettingInteger('open_value'))
        self.thresholdCheckBox.SetValue(profile.getProfileSettingBool('threshold'))
        self.thresholdSlider.SetValue(profile.getProfileSettingInteger('threshold_value'))


class ScenePanel(wx.Panel):
    """
    """
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, size=(270, 0))

        self.scanner = Scanner.Instance()
        
        #-- Graphic elements
        algorithmStaticText = wx.StaticText(self, label=_("Algorithm"))
        algorithmStaticText.SetFont((wx.Font(wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT).GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)))
        self.compactAlgRadioButton = wx.RadioButton(self, label=_("Compact"), size=(100,-1))
        self.completeAlgRadioButton = wx.RadioButton(self, label=_("Complete"), size=(100,-1))
        filterStaticText = wx.StaticText(self, label=_("Filter"))
        filterStaticText.SetFont((wx.Font(wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT).GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)))
        minRadiousStaticText = wx.StaticText(self, wx.ID_ANY, _("min R"), size=(45, -1), style=wx.ALIGN_CENTRE)
        self.minRadiousSlider = wx.Slider(self, wx.ID_ANY, 0, -200, 200, size=(150, -1), style=wx.SL_LABELS)
        maxRadiousStaticText = wx.StaticText(self, wx.ID_ANY, _("max R"), size=(45, -1), style=wx.ALIGN_CENTRE)
        self.maxRadiousSlider = wx.Slider(self, wx.ID_ANY, 0, -200, 200, size=(150, -1), style=wx.SL_LABELS)
        minHeightStaticText = wx.StaticText(self, wx.ID_ANY, _("min H"), size=(45, -1), style=wx.ALIGN_CENTRE)
        self.minHeightSlider = wx.Slider(self, wx.ID_ANY, 0, -100, 200, size=(150, -1), style=wx.SL_LABELS)
        maxHeightStaticText = wx.StaticText(self, wx.ID_ANY, _("max H"), size=(45, -1), style=wx.ALIGN_CENTRE)
        self.maxHeightSlider = wx.Slider(self, wx.ID_ANY, 0, -100, 200, size=(150, -1), style=wx.SL_LABELS)

        moveStaticText = wx.StaticText(self, wx.ID_ANY, _("Move"), style=wx.ALIGN_CENTRE)
        moveStaticText.SetFont((wx.Font(wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT).GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)))
        zStaticText = wx.StaticText(self, wx.ID_ANY, _("z"), size=(45, -1), style=wx.ALIGN_CENTRE)
        self.zSlider = wx.Slider(self, wx.ID_ANY, 0, -50, 50, size=(150, -1), style=wx.SL_LABELS)

        #-- Bind
        self.Bind(wx.EVT_RADIOBUTTON, self.onAlgChanged, self.compactAlgRadioButton)
        self.Bind(wx.EVT_RADIOBUTTON, self.onAlgChanged, self.completeAlgRadioButton)
        self.Bind(wx.EVT_SLIDER, self.onRadiousChanged, self.minRadiousSlider)
        self.Bind(wx.EVT_SLIDER, self.onRadiousChanged, self.maxRadiousSlider)
        self.Bind(wx.EVT_SLIDER, self.onHeightChanged, self.minHeightSlider)
        self.Bind(wx.EVT_SLIDER, self.onHeightChanged, self.maxHeightSlider)
        self.Bind(wx.EVT_SLIDER, self.onZChanged, self.zSlider)
        
        #-- Layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(algorithmStaticText, 0, wx.ALL, 10)
        vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL^wx.TOP, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.compactAlgRadioButton, 0, wx.ALL, 15);
        hbox.Add(self.completeAlgRadioButton, 0, wx.ALL, 15);
        vbox.Add(hbox) 
        vbox.Add(filterStaticText, 0, wx.ALL, 10)
        vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(minRadiousStaticText, 0, wx.ALL^wx.BOTTOM, 18)
        hbox.Add(self.minRadiousSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(maxRadiousStaticText, 0, wx.ALL^wx.BOTTOM, 18)
        hbox.Add(self.maxRadiousSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(minHeightStaticText, 0, wx.ALL^wx.BOTTOM, 18)
        hbox.Add(self.minHeightSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(maxHeightStaticText, 0, wx.ALL, 18)
        hbox.Add(self.maxHeightSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        vbox.Add(moveStaticText, 0, wx.ALL, 10)
        vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(zStaticText, 0, wx.ALL^wx.BOTTOM, 18)
        hbox.Add(self.zSlider, 0, wx.ALL, 0)
        vbox.Add(hbox)
        self.SetSizer(vbox)
        self.Centre()

    def onAlgChanged(self, event):
        self.scanner.core.setUseCompactAlgorithm(self.compactAlgRadioButton.GetValue())
        profile.putProfileSetting('use_compact', self.compactAlgRadioButton.GetValue())

    def onZChanged(self, event):
        self.scanner.core.setZOffset(self.zSlider.GetValue())
        profile.putProfileSetting('z_offset', self.zSlider.GetValue())
        
    def onRadiousChanged(self, event):
        minR = int(self.minRadiousSlider.GetValue())
        maxR = int(self.maxRadiousSlider.GetValue())

        if minR >= maxR:
            maxR = minR

        self.minRadiousSlider.SetValue(minR)
        self.maxRadiousSlider.SetValue(maxR)

        self.scanner.core.setRangeFilter(int(self.minRadiousSlider.GetValue()),
                                              int(self.maxRadiousSlider.GetValue()),
                                              int(self.minHeightSlider.GetValue()),
                                              int(self.maxHeightSlider.GetValue()))

        profile.putProfileSetting('min_rho', minR)
        profile.putProfileSetting('max_rho', maxR)

    def onHeightChanged(self, event):
        minH = int(self.minHeightSlider.GetValue())
        maxH = int(self.maxHeightSlider.GetValue())

        if minH >= maxH:
            maxH = minH

        self.minHeightSlider.SetValue(minH)
        self.maxHeightSlider.SetValue(maxH)

        self.scanner.core.setRangeFilter(int(self.minRadiousSlider.GetValue()),
                                              int(self.maxRadiousSlider.GetValue()),
                                              int(self.minHeightSlider.GetValue()),
                                              int(self.maxHeightSlider.GetValue()))

        profile.putProfileSetting('min_h', minH)
        profile.putProfileSetting('max_h', maxH)

    def updateProfileToAllControls(self):
        self.compactAlgRadioButton.SetValue(profile.getProfileSettingBool('use_compact'))
        self.completeAlgRadioButton.SetValue(not profile.getProfileSettingBool('use_compact'))
        self.minRadiousSlider.SetValue(profile.getProfileSettingInteger('min_rho'))
        self.maxRadiousSlider.SetValue(profile.getProfileSettingInteger('max_rho'))
        self.minHeightSlider.SetValue(profile.getProfileSettingInteger('min_h'))
        self.maxHeightSlider.SetValue(profile.getProfileSettingInteger('max_h'))
        self.zSlider.SetValue(profile.getProfileSettingInteger('z_offset'))