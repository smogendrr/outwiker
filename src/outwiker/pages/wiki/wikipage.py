#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.tree import WikiPage
from wikipanel import WikiPagePanel
from wikipreferences import WikiPrefGeneralPanel
from outwiker.core.factory import PageFactory
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.gui.hotkey import HotKey

from actions.bold import WikiBoldAction
from actions.italic import WikiItalicAction
from actions.bolditalic import WikiBoldItalicAction
from actions.underline import WikiUnderlineAction
from actions.strike import WikiStrikeAction
from actions.subscript import WikiSubscriptAction
from actions.superscript import WikiSuperscriptAction
from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.monospace import WikiMonospaceAction
from actions.alignleft import WikiAlignLeftAction
from actions.alignright import WikiAlignRightAction
from actions.aligncenter import WikiAlignCenterAction
from actions.alignjustify import WikiAlignJustifyAction
from actions.preformat import WikiPreformatAction
from actions.nonparsed import WikiNonParsedAction
from actions.listbullets import WikiListBulletsAction
from actions.listnumbers import WikiListNumbersAction
from actions.headings import *


_actions = [
        (WikiBoldAction, HotKey ("B", ctrl=True)),
        (WikiItalicAction, HotKey ("B", ctrl=True)),
        (WikiBoldItalicAction,  HotKey ("I", ctrl=True, shift=True)),
        (WikiUnderlineAction, HotKey ("U", ctrl=True)),
        (WikiStrikeAction, HotKey ("K", ctrl=True)),
        (WikiSubscriptAction, HotKey ("=", ctrl=True)),
        (WikiSuperscriptAction, HotKey ("+", ctrl=True)),
        (WikiFontSizeBigAction, HotKey (".", ctrl=True)),
        (WikiFontSizeSmallAction, HotKey (",", ctrl=True)),
        (WikiMonospaceAction, HotKey ("7", ctrl=True)),
        (WikiAlignLeftAction, HotKey ("L", ctrl=True, alt=True)),
        (WikiAlignRightAction, HotKey ("R", ctrl=True, alt=True)),
        (WikiAlignCenterAction, HotKey ("C", ctrl=True, alt=True)),
        (WikiAlignJustifyAction, HotKey ("J", ctrl=True, alt=True)),
        (WikiPreformatAction, HotKey ("F", ctrl=True, alt=True)),
        (WikiNonParsedAction, None),
        (WikiListBulletsAction, HotKey ("G", ctrl=True)),
        (WikiListNumbersAction, HotKey ("G", ctrl=True)),
        (WikiHeading1Action, HotKey ("1", ctrl=True)),
        (WikiHeading2Action, HotKey ("2", ctrl=True)),
        (WikiHeading3Action, HotKey ("3", ctrl=True)),
        (WikiHeading4Action, HotKey ("4", ctrl=True)),
        (WikiHeading5Action, HotKey ("5", ctrl=True)),
        (WikiHeading6Action, HotKey ("6", ctrl=True)),
        ]


class WikiWikiPage (WikiPage):
    """
    Класс wiki-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)
    

    @staticmethod
    def getTypeString ():
        return u"wiki"


class WikiPageFactory (PageFactory):
    @staticmethod
    def getPageType():
        return WikiWikiPage

    # Обрабатываемый этой фабрикой тип страниц (имеется в виду тип, описываемый строкой)
    @staticmethod
    def getTypeString ():
        return WikiPageFactory.getPageType().getTypeString()

    # Название страницы, показываемое пользователю
    title = _(u"Wiki Page")


    def __init__ (self):
        pass


    @staticmethod
    def create (parent, title, tags):
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        return PageFactory.createPage (WikiPageFactory.getPageType(), parent, title, tags)


    @staticmethod
    def getPageView (parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        panel = WikiPagePanel (parent)

        return panel


    @staticmethod
    def getPrefPanels (parent):
        """
        Получить список панелей для окна настроек
        Возвращает список кортежей ("название", Панель)
        """
        generalPanel = WikiPrefGeneralPanel (parent)

        return [ PreferencePanelInfo (generalPanel, _(u"General") ) ]


    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с HTML-страницей
        """
        map (lambda actionTuple: application.actionController.register (actionTuple[0](application), actionTuple[1] ), _actions)


    @staticmethod
    def removeActions (application):
        map (lambda actionTuple: application.actionController.removeAction (actionTuple[0].stringId), _actions)
