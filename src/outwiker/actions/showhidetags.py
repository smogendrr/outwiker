#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.actions.showhidebase import ShowHideBaseAction


class ShowHideTagsAction (ShowHideBaseAction):
    """
    Показать / скрыть панель с тегами
    """
    stringId = u"ShowHideTags"

    def __init__ (self, application):
        super (ShowHideTagsAction, self).__init__ (application)


    @property
    def title (self):
        return _(u"Tags")


    @property
    def description (self):
        return _(u"Show / hide a tags panel")
    

    @property
    def strid (self):
        return self.stringId


    def getPanel (self):
        return self._application.mainWindow.tagsCloudPanel
