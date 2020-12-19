#!/usr/bin/env python3

from pathlib import Path

import cherrypy

import furigana.mecab

class FuriganaServer() :
	def __init__(self) :
		self.mecab = furigana.mecab.Mecab("--dicdir=/var/lib/mecab/dic/juman-utf8")

	@cherrypy.expose
	def index(self):
		return Path("data/furigana.html").read_text()

	@cherrypy.expose
	@cherrypy.tools.allow(methods='POST')
	@cherrypy.tools.accept(media='text/plain')
	def _mecab_process(self) :
		txt = cherrypy.request.body.read().decode('utf8').strip()
		txt = self.mecab.process(txt)
		return txt

conf = {
	"/data": {
		"tools.staticdir.on" : True,
		"tools.staticdir.dir" : str(Path("./data").absolute()),
		"tools.gzip.on" : True,
	},
	"/javascript": {
		"tools.staticdir.on" : True,
		"tools.staticdir.dir" : str(Path("./javascript").absolute()),
		"tools.gzip.on" : True,
	}
}

if __name__ == '__main__' :
	cherrypy.quickstart(FuriganaServer(), config=conf)
