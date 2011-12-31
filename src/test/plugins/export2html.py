#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import os.path
import shutil

from outwiker.core.tree import WikiDocument
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class Export2HtmlTest (unittest.TestCase):
    def setUp(self):
        self.outputdir = "../test/temp"
        self.pluginname = u"Export to HTML"

        self.path = u"../test/samplewiki"
        self.root = WikiDocument.load (self.path)
        
        dirlist = [u"../plugins/export2html"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.__removeTempDir()
        os.mkdir (self.outputdir)


    def tearDown (self):
        self.__removeTempDir()


    def __removeTempDir (self):
        if os.path.exists (self.outputdir):
            shutil.rmtree (self.outputdir)


    def testLoading (self):
        self.assertEqual (len (self.loader), 1)
        self.loader[self.pluginname]


    def testExporterPage (self):
        pagename = u"Страница 1"
        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])

        self.assertEqual (exporter.page, self.root[pagename])


    def testExportSinglePage (self):
        """
        Тест на создание файлов и страниц
        """
        pagename = u"Страница 1"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.isfile (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename) ) )
        self.assertTrue (os.path.isdir (os.path.join (self.outputdir, pagename) ) )


    def testExportWithName (self):
        """
        Тест на то, что мы можем изменять имя файла и папки для экспорта
        """
        pagename = u"Страница 1"
        exportname = u"Бла-бла-бла"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])
        exporter.export (outdir = self.outputdir,
                exportname=exportname,
                imagesonly=False,
                alwaysOverwrite=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, exportname + ".html") ) )
        self.assertTrue (os.path.isfile (os.path.join (self.outputdir, exportname + ".html") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, exportname) ) )
        self.assertTrue (os.path.isdir (os.path.join (self.outputdir, exportname) ) )

    
    def testAttachesSinglePage (self):
        """
        Тест на то, что прикрепленные файлы копируются
        """
        pagename = u"Страница 1"
        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "add.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "memorial.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "wall.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "image.tif") ) )


    def testAttachesImagesSinglePage (self):
        """
        Тест на то, что копируются только прикрепленные картинки
        """
        pagename = u"Страница 1"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "add.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "memorial.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "wall.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "image.tif") ) )


    def testLinkChangeHtml (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на HTML-странице
        """
        pagename = u"Страница 1"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<img src="{pagename}/add.png" />'.format (pagename=pagename) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>.'.format (pagename=pagename) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)


    def testLinkChangeHtmlWithName (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на HTML-странице
        """
        pagename = u"Страница 1"
        exportname = u"Бла-бла-бла"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])
        exporter.export (outdir = self.outputdir,
                exportname=exportname,
                imagesonly=True,
                alwaysOverwrite=False)

        text = u""

        with open (os.path.join (self.outputdir, exportname + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<img src="{pagename}/add.png" />'.format (pagename=exportname) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>.'.format (pagename=exportname) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)


    def testLinkChangeWiki (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        fullpagename = u"Типы страниц/wiki-страница"
        pagename = u"wiki-страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<img src="{pagename}/add.png" />'.format (pagename=pagename) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>'.format (pagename=pagename) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)
        self.assertTrue (u'<a href="{pagename}/image.jpg"><img src="{pagename}/__thumb/th_maxsize_250_image.jpg" /></a>'.format (pagename=pagename) in text)


    def testLinkChangeWikiWithName (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        fullpagename = u"Типы страниц/wiki-страница"
        pagename = u"wiki-страница"
        exportname = u"Бла-бла-бла"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=exportname,
                imagesonly=True,
                alwaysOverwrite=False)

        text = u""

        with open (os.path.join (self.outputdir, exportname + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        # print text
        self.assertTrue (u'<img src="{pagename}/add.png" />'.format (pagename=exportname) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>'.format (pagename=exportname) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)
        self.assertTrue (u'<a href="{pagename}/image.jpg"><img src="{pagename}/__thumb/th_maxsize_250_image.jpg" /></a>'.format (pagename=exportname) in text)



    def testWikiPageThumb (self):
        """
        Проверка на то, что сохраняется папка __thumb
        """
        fullpagename = u"Типы страниц/wiki-страница"
        pagename = u"wiki-страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "image.jpg") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "__thumb") ) )


    def testFilesExportTextPage (self):
        """
        Экспорт текстовой страницы
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.isfile (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename) ) )
        self.assertTrue (os.path.isdir (os.path.join (self.outputdir, pagename) ) )


    def testAttachesExportTextPage (self):
        """
        Экспорт текстовой страницы
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "anchor.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "application.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "box.png") ) )


    def testHtmlFromTextPage (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'&lt;a href="http://jenyay.net"&gt;bla-bla-bla&lt;/a&gt;' in text)


    def testTextTemplate (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])

        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<head>' in text)
        self.assertTrue (u'</head>' in text)
        self.assertTrue (u'<body>' in text)
        self.assertTrue (u'</body>' in text)
        self.assertTrue (u'<pre>' in text)
        self.assertTrue (u'</pre>' in text)
        self.assertTrue (u'<title>Текстовая страница</title>' in text)


    def testAttachesImagesExportTextPage (self):
        """
        Экспорт текстовой страницы
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[fullpagename])
        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=True,
                alwaysOverwrite=False)

        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "anchor.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "application.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "box.png") ) )


    def testFileExists (self):
        """
        Тест на то, что создаваемый файл уже может существовать
        """
        pagename = u"Страница 1"
        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])

        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        self.assertRaises (BaseException, 
                exporter.export, 
                outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        exporter.export (outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=True)


    def testInvalidFormat (self):
        """
        Проверка на попытку экспортировать страницу, которая не может быть сохранена в HTML (страница поиска)
        """
        pagename = u"Типы страниц/Страница поиска"

        self.assertRaises (BaseException, 
                self.loader[self.pluginname].exporterFactory.getExporter, 
                page=self.root[pagename])


    def testHtmlNotFound (self):
        """
        Проверка на случай, если нет сформированного HTML-а
        """
        pagename = u"Страница 1"

        htmlname = u"__content.html"
        tmpname = u"__tmp.html"

        page = self.root[pagename]

        srcname = os.path.join (page.path, htmlname)
        newname = os.path.join (page.path, tmpname)

        os.rename (srcname, newname)

        exporter = self.loader[self.pluginname].exporterFactory.getExporter (self.root[pagename])

        self.assertRaises (BaseException, 
                exporter.export, 
                outdir = self.outputdir,
                exportname=pagename,
                imagesonly=False,
                alwaysOverwrite=False)

        os.rename (newname, srcname)


    def testExportBranchFiles (self):
        """
        Экспорт дерева
        """
        pagename = u"Страница 1"
        branchExporter = self.loader[self.pluginname].branchExporter (self.root[pagename])

        result = branchExporter.export (
                outdir=self.outputdir,
                imagesonly=False,
                alwaysOverwrite=False
                )

        self.assertEqual (len (result), 0)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename) ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + ".html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2_Страница 5") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2_Страница 5.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2_Страница 6") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2_Страница 6.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2_Страница 6_Страница 7") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            pagename + u"_Страница 2_Страница 6_Страница 7.html") ) )


    def testExportBranchRoot (self):
        """
        Экспорт, начиная с корня дерева
        """
        wikiname = u"samplewiki"
        branchExporter = self.loader[self.pluginname].branchExporter (self.root)

        result = branchExporter.export (
                outdir=self.outputdir,
                imagesonly=False,
                alwaysOverwrite=False
                )

        self.assertEqual (len (result), 1)
        self.assertTrue (u"Страница поиска" in result[0])

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2_Страница 5") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2_Страница 5.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2_Страница 6") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2_Страница 6.html") ) )

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2_Страница 6_Страница 7") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, 
            wikiname + u"_Страница 1_Страница 2_Страница 6_Страница 7.html") ) )