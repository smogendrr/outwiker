#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PluginsConfig
from outwiker.gui.htmlrenderfactory import getHtmlRender
from outwiker.core.system import getCurrentDir


class PluginsPanel (wx.Panel):
    """
    Панель со списком установленных плагинов
    """
    def __init__ (self, parent):
        wx.Panel.__init__ (self, parent, style=wx.TAB_TRAVERSAL)
        self.__htmlMinWidth = 150

        self.__createGui ()

        self.__controller = PluginsController (self)


    def __createGui (self):
        self.pluginsList = wx.CheckListBox (self, -1, style=wx.LB_SORT)
        self.pluginsList.SetMinSize ((50, -1))

        # Панель, которая потом заменится на HTML-рендер
        self.__blankPanel = wx.Panel (self)
        self.__blankPanel.SetMinSize ((self.__htmlMinWidth, -1))

        self.__pluginsInfo = None

        self.__layout()


    @property
    def pluginsInfo (self):
        if self.__pluginsInfo == None:
            # Удалим пустую панель, а вместо нее добавим HTML-рендер
            self.mainSizer.Remove (self.__blankPanel)
            self.__blankPanel.Destroy()

            self.__pluginsInfo = getHtmlRender (self)
            self.__pluginsInfo.SetMinSize ((self.__htmlMinWidth, -1))

            self.mainSizer.Add (self.__pluginsInfo, flag=wx.EXPAND)
            self.Layout()

        return self.__pluginsInfo


    def __layout (self):
        self.mainSizer = wx.FlexGridSizer (1, 2)
        self.mainSizer.AddGrowableRow (0)
        self.mainSizer.AddGrowableCol (0)
        self.mainSizer.AddGrowableCol (1)
        self.mainSizer.Add (self.pluginsList, flag=wx.EXPAND)
        self.mainSizer.Add (self.__blankPanel, flag=wx.EXPAND)

        self.SetSizer (self.mainSizer)


    def LoadState(self):
        self.__controller.loadState ()


    def Save (self):
        self.__controller.save()



class PluginsController (object):
    """
    Контроллер, отвечающий за работу панели со списком плагинов
    """
    def __init__ (self, pluginspanel):
        self.__owner = pluginspanel

        # Т.к. под виндой к элементам CheckListBox нельзя прикреплять пользовательские данные,
        # придется их хранить отдельно.
        # Ключ - имя плагина, оно же текст строки
        # Значение - экземпляр плагина
        self.__pluginsItems = {}

        self.__owner.Bind (wx.EVT_LISTBOX, self.__onSelectItem, self.__owner.pluginsList)


    def __onSelectItem (self, event):
        htmlContent = u""
        if event.IsSelection():
            plugin = self.__pluginsItems[event.GetString()]
            assert plugin != None

            htmlContent = self.__createPluginInfo (plugin)

        self.__owner.pluginsInfo.SetPage (htmlContent, getCurrentDir())


    def __createPluginInfo (self, plugin):
        assert plugin != None

        infoTemplate = u"""<HTML>
<HEAD>
    <META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>
</HEAD>

<BODY>
{name}<BR>
{version}<BR>
{url}<BR>
{description}<BR>
</BODY>
</HTML>"""

        plugin_name = u"""<H3>{name}</H3>""".format (name=plugin.name)

        plugin_version = u"""<B>{version_header}:</B> {version}""".format (
                version_header = _(u"Version"),
                version=plugin.version)

        plugin_description = u"""<B>{description_head}:</B> {description}""".format (
                description_head = _(u"Description"),
                description = plugin.description.replace ("\n", "<BR>"))

        if "url" in dir (plugin):
            plugin_url = u"""<BR><B>{site_head}</B>: <A HREF="{url}">{url}</a><BR>""".format (
                    site_head = _("Site"),
                    url = plugin.url)
        else:
            plugin_url = u""


        result = infoTemplate.format (
                name = plugin_name,
                version = plugin_version,
                description = plugin_description,
                url = plugin_url)

        return result


    def loadState (self):
        self.__pluginsItems = {}
        self.__owner.pluginsList.Clear()
        self.__appendEnabledPlugins()
        self.__appendDisabledPlugins()


    def __appendEnabledPlugins (self):
        """
        Добавить загруженные плагины в список
        """
        for plugin in Application.plugins:
            index = self.__owner.pluginsList.Append (plugin.name)

            assert plugin.name not in self.__pluginsItems.keys()
            self.__pluginsItems[plugin.name] = plugin

            self.__owner.pluginsList.Check (index, True)


    def __appendDisabledPlugins (self):
        """
        Добавить отключенные плагины в список
        """
        for plugin in Application.plugins.disabledPlugins.values():
            index = self.__owner.pluginsList.Append (plugin.name)

            assert plugin.name not in self.__pluginsItems.keys()
            self.__pluginsItems[plugin.name] = plugin

            self.__owner.pluginsList.Check (index, False)


    def save (self):
        config = PluginsConfig (Application.config)
        config.disabledPlugins.value = self.__getDisabledPlugins()
        Application.plugins.updateDisableList()


    def __getDisabledPlugins (self):
        disabledList = []

        for itemindex in range (self.__owner.pluginsList.GetCount()):
            if not self.__owner.pluginsList.IsChecked (itemindex):
                disabledList.append (self.__pluginsItems[self.__owner.pluginsList.GetString (itemindex)].name)

        return disabledList

