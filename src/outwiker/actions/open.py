#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import openWikiWithDialog


class OpenAction (BaseAction):
    """
    Открытие дерева заметок
    """
    stringId = u"OpenTree"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Open…")


    @property
    def description (self):
        return _(u"Open tree notes")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        openWikiWithDialog (self._application.mainWindow, False)
