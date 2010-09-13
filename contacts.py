# -*- coding: utf-8 -*-
# Контактный справочник

from bottle import route, view, request, \
    static_file, debug, run, redirect
from pymongo import Connection as dbConnect
from pymongo.objectid import ObjectId as objId
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

@route('/edit/:cid')
@view('design/contactEdit')
def edit_contact(cid='new'):
    if cid != 'new':
        cid = objId(cid)
    return {
        'entry' : entries.find_one({'_id': cid}),
        'settings' : settings
        }

@route('/edit', method='POST')
def save_contact():
    contact = {}
    for k,v in request.forms.iterallitems():
        if (k,v) != ('_id', 'new'):
            contact[k] = v
        if '_id' in contact:
            contact['_id'] = objId(contact['_id'])
    entries.save(contact)
    redirect('/')

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
# Загрузка сервера

def startup(cfg):
    global entries, settings
    db = dbConnect(cfg.get('db', 'host'), cfg.getint('db', 'port')).contacts
    entries = db.entries
    if entries.count() == 0:
        entries.insert({
                '_id': 'new',
                'FullName':'',
                'Email':'',
                'Phone':''})
    settings = db.settings
    debug(cfg.getboolean('etc', 'debug'))
    run(host=cfg.get('http', 'host'), port=cfg.getint('http', 'port'))

cfg = cfgParser()
cfg.read('contacts.cfg')
startup(cfg) # Do it
