# -*- coding: utf-8 -*-
import bottle
from bottle import route, view
import sqlite3

db = sqlite3.connect('contacts.db')

# По умолчанию на выходе из sqlite возвращается массив. Это не очень
# удобно, и мы немного переделаем это поведение, чтобы на выходе
# возвращался хэш.
def row2dict(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db.row_factory = row2dict

# Настройка БД
def setupDb():
    db.executescript('''
    --- Поля контактного справочника
    create table fields (
       cid   int,                      --- индекс контакта
       fkey  int,                      --- имя поля
       value text,                     --- значение поля
       ord   text,                     --- Порядок сортировки 
                                       --- (-1 - не показывать)
       foreign key(fkey) references i18n(fn)
    );
    
    --- Локализация полей контактного справочника
    create table i18n (
       fn       integer primary key,   --- Индекс                
       fsysname text,                  --- Системное имя (то, 
                                       --- что берем из XML).
       caption  text,                  --- Заголовок
       tooltip  text,                  --- Подсказка-тултип
       deford   int                    --- Порядок сортировки 
                                       --- по-умолчанию
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
    return { 'entries' : db.execute('''
        select 
           caption, tooltip, value, (ord || deford) as ord
        from 
           fields
        inner join 
           i18n
        on
           fkey = fn
        order by 
           cid, ord
        ''') }

# Форма добавления новых контактов и по совместительству их
# редактирования.
@route('/create')
@route('/edit/:cid')
@view('design/contactEdit')
def create(cid=''):
    # Опять же, если нам передали id в качестве параметра, пытаемся
    # получить данные о контакте из БД и загрузить их в форму. Если же
    # мы потерпим неудачу, то просто возвращаем новую форму для
    # создания контакта.
    return { 'entries' : db.execute('''
        select 
           fkey, caption, tooltip, value, (ord || deford) as ord
        from 
           fields
        inner join 
           i18n
        on
           fkey = fn
        where 
           cid = ?
        order by
           ord
        ''', (cid or 0)) }


# Сюда к нам приходят данные, запощенные пользователем
@route('/edit', method='POST')
def post():
    return ''

# Настройки скрипта. Выводим обрабатываем табличку i18n
@route('/settings')
@view('design/settings')
def settings():
    return { 'entries' : db.execute('''
       select
          fn, fsysname, caption, tooltip, deford
       from
          i18n
       order by
          deford
    ''') }


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
