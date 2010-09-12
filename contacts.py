# -*- coding: utf-8 -*-
# Контактный справочник

import bottle
from bottle import route, view, request, static_file
from pymongo import Connection as dbConnect
from ConfigParser import ConfigParser as cfgParser

#------------------------------------------------------------------
# Контроллер - обработка запросов

@route('/favicon.ico')
@route('/static/:filename')
def server_static(filename='favicon.ico'):
    return static_file(filename, root='./static')

@route('/')
@view('design/contactList')
def index():
    return { 'entries' : entries.find(), 'settings' : settings.find() }

@route('/create')
@route('/edit/:cid')
@view('design/contactEdit')
def create(cid='new'):
    return {
        'entry' : entries.find({'cid': cid}),
        'settings' : settings
        }

@route('/edit', method='POST')
def post():
    targetObj = {
        '_id' : request.forms.get('cid'),
        }
    
    fields = zip(
        request.forms.getall('fkey'), 
        request.forms.getall('fvalue')
        )

    for f in fields:
        targetObj[f[0]] = f[1]
        
    entries.save(targetObj)
    return ''

@route('/settings')
@view('design/settings')
def settings():
    return { 'settings' : settings }

@route('/settings', method='POST')
def saveSettings():
    return 'Settings stub'

@route('/filter/:name/:value')
@view('design/filter')
def filter(name, value):
    return entries.find({name : value})

#------------------------------------------------------------------
# Загрузка

def startup(cfg):
    global entries, settings
    db = dbConnect(cfg.get('db', 'host'), cfg.getint('db', 'port')).contacts
    entries = db.entries
    if entries.count() == 0:
        entries.insert({'_id':'new', 'FullName':'Test'})
    settings = db.settings
    bottle.debug(cfg.getboolean('etc', 'debug'))
    bottle.run(host=cfg.get('http', 'host'), port=cfg.getint('http', 'port'))

cfg = cfgParser()
cfg.read('contacts.cfg')
startup(cfg) # Do it
