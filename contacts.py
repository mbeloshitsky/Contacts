# -*- coding: utf-8 -*-
import bottle
from bottle import route, view
import sqlite3

db = sqlite3.connect('contacts.db')

def setupDb():
    db.executescript('''
    --- Поля контактного справочника
    create table fields (
       cid   int,                --- индекс контакта
       fkey  int,                --- имя поля
       value text,               --- значение поля
       ord   text,               --- Порядок сортировки (-1 - скрытое)
       foreign key(fkey) references i18n(fn)
    );
    
    --- Локализация полей контактного справочника
    create table i18n (
       fn integer primary key,   --- Индекс                
       fsysname text,            --- Системное имя (то, что берем из XML).
       caption text,             --- Заголовок
       tooltip,                  --- Подсказка-тултип
       deford                    --- Порядок сортировки по-умолчанию
    );

    --- Индексируем fSystemName т.к. по ней будет производиться
    --- выборка полей.
    create unique index idx_fsysname on i18n(fsysname);

    ''')

# Заглавная страничка контактного справочника. Вообще рендерить все
# сразу - не очень хороший подход. Со временем мы от него избавимся
# (TODO), при помощи реалтайм-подгрузки.
@route('/')
@view('design/contactList')
def index():
    return { 'title': 'ss',
        'entries': db.execute('''
            select 
               caption, tooltip, value, (ord || deford) as ord
            from 
               fields
            inner join 
               i18n
            on
               fkey = fn
            ''') }

# Форма добавления новых контактов и по совместительству их
# редактирования.
@route('/edit/:id')
@view('contactEditing')
def create(cid):
    # TODO: Выборка из БД данных контакта в случае, если мы его
    # редактируем.
    return page.fill({'id': cid})

# Универсальный фильтр. Фильтрует все, что только можно.
def filter():
    return 'Filter stub'

# Загрузка нашего скрипта. Проверяем окружение и пытаемся его
# настроить в случае если что не так. Если самостоятельно настроить
# невозможно - репортим ошибки.
def startup():
    # Получим что-нибудь из таблички i18n дабы убедиться в том, что мы
    # ее создали. Если мы словим ошибку вида "табличка не найдена" -
    # значит мы просто запускаем скрипт в первый раз и нам нужно
    # создать схему в БД.
    try:
        curr = db.execute('select count(fn) from i18n')
    except sqlite3.OperationalError as (wtf):
        if str(wtf).startswith("no such table: i18n"):
            # Okey. Мы словили исключение и оно нам говорит английским
            # языком, что нашей таблицы ещё не существует. Создаем
            # схему БД.
            setupDb()
            pass
    # Все готово. Запускаем бутылочный сервер.
    bottle.debug(True)
    bottle.run()


startup() # Do it
