#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_
from .pagestat import PageStat
from .treestat import TreeStat
from .pagestatdialog import PageStatDialog


if getCurrentVersion() < Version (1, 7, 0, 684, status=StatusSet.DEV):
    print ("Spoiler plugin. OutWiker version requirement: 1.7.0.684")
else:
    class PluginStatistics (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)

            self.ID_PAGE_STAT = wx.NewId()
            self.ID_TREE_STAT = wx.NewId()

            self._separatorMenuItem = None
            self._pageStatMenuItem = None
            self._treeStatMenuItem = None


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Statistics"

        
        @property
        def description (self):
            return _(u"Plugin to display statistics")


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net")
        
        
        def initialize(self):
            self._initlocale(u"statistics")

            if self._application.mainWindow != None:
                self._addMenuItems ()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            if self._application.mainWindow != None:
                self._removeMenu ()


        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e

            set_(_)


        @property
        def toolsMenu (self):
            return self._application.mainWindow.mainMenu.toolsMenu


        def _addMenuItems (self):
            """
            Добавить пункты, связанные со статистикой в меню 'Инструменты'
            """
            assert self._separatorMenuItem == None
            assert self._pageStatMenuItem == None
            assert self._treeStatMenuItem == None

            self._separatorMenuItem = self.toolsMenu.AppendSeparator()

            self._pageStatMenuItem = self.toolsMenu.Append (self.ID_PAGE_STAT, _(u"Page statistic"))
            self._application.mainWindow.Bind (wx.EVT_MENU, self._onPageStat, id=self.ID_PAGE_STAT)

            self._treeStatMenuItem = self.toolsMenu.Append (self.ID_TREE_STAT, _(u"Tree statistic"))
            self._application.mainWindow.Bind (wx.EVT_MENU, self._onTreeStat, id=self.ID_TREE_STAT)


        def _removeMenu (self):
            """
            Удалить добавленные пункты меню
            """
            assert self._separatorMenuItem != None
            assert self._pageStatMenuItem != None
            assert self._treeStatMenuItem != None

            self._application.mainWindow.Unbind (wx.EVT_MENU, handler=self._onPageStat)
            self._application.mainWindow.Unbind (wx.EVT_MENU, handler=self._onTreeStat)

            self.toolsMenu.RemoveItem (self._separatorMenuItem)
            self.toolsMenu.RemoveItem (self._pageStatMenuItem)
            self.toolsMenu.RemoveItem (self._treeStatMenuItem)

            self._separatorMenuItem = None
            self._pageStatMenuItem = None
            self._treeStatMenuItem = None


        def _onPageStat (self, event):
            if self._application.selectedPage != None:
                pageStat = PageStat (self._application.selectedPage)

                with PageStatDialog (self._application.mainWindow, pageStat) as dlg:
                    dlg.ShowModal()


        def _onTreeStat (self, event):
            if self._application.wikiroot != None:
                treeStat = TreeStat (self._application.wikiroot)

                # Сколько элементов списков выводить
                listcount = 10

                # Количество страниц
                print u"Page count: {0}".format (treeStat.pageCount)

                # Страницы с максимальной глубиной вложенности
                maxDepthList = treeStat.maxDepth
                print u"Max depth: {0}".format (maxDepthList[0][0])
                for _, page in maxDepthList:
                    print u"    {0}".format (page.title)

                # Количество тегов
                print u"Tags count: {0}".format (treeStat.tagsCount)

                # Самые часто используемые теги
                tagsList = treeStat.frequentTags[0: min (listcount, treeStat.tagsCount)]
                print u"Frequent tags:"
                for tagName, count in tagsList:
                    print u"    {0}: {1}".format (tagName, count)

                # Самые редкто используемые теги
                tagsList = treeStat.frequentTags
                tagsList.reverse()

                print u"Infrequent tags:"
                for tagName, count in tagsList[0: min (listcount, treeStat.tagsCount)]:
                    print u"    {0}: {1}".format (tagName, count)

                # Последние измененные записи
                pageDate = treeStat.pageDate
                print "Recent edited pages:"
                for page in pageDate[0: min (listcount, treeStat.pageCount)]:
                    print u"    {0}: {1}".format (page.title, page.datetime)

                # Самые старые записи
                pageDate.reverse()
                print "Old pages:"
                for page in pageDate[0: min (listcount, treeStat.pageCount)]:
                    print u"    {0}: {1}".format (page.title, page.datetime)



        def getPageStat (self, page):
            """
            Получить экземпляр класса для сбора статистики по странице. Используется в тестах
            """
            return PageStat (page)


        def getTreeStat (self, root):
            """
            Получить экземпляр класса для сбора статистики по дереву. Используется в тестах
            """
            return TreeStat (root)
