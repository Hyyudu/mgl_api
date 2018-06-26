from src.services.db import DB

db = DB()
dummy = {"id": 100, "name": "Dummy", 'code': 'dum'}
new_dummy = {"id": 101, "name": "New dummy", 'code': 'ndm'}

def test_delete():
    db.query('delete from companies where id in ({}, {})'.format(dummy['id'], new_dummy['id']), need_commit=True)
    assert db.fetchAll('select * from companies where id=:id', dummy) == []

def test_fetchAll():
    # act
    companies = db.fetchAll("select * from companies")

    # assert
    assert companies == [
        {'id': 1, 'name': 'Гугл Дисней', 'code': 'gd'},
        {'id': 2, 'name': 'Пони Роскосмос Экспресс', 'code': 'pre'},
        {'id': 3, 'name': 'Красный Крест Генетикс', 'code': 'kkg'},
        {'id': 4, 'name': 'Мицубиси АвтоВАЗ Технолоджи', 'code': 'mat'},
        {'id': 5, 'name': 'МарсСтройТрест', 'code': 'mst'}
    ]


def test_fetchRow():
    google = db.fetchRow("select id, name from companies where id=:id", {"id": 1})
    assert google == {"id": 1, "name": "Гугл Дисней"}
    assert db.fetchRow('select * from companies where id=7') is None


def test_fetchColumn():
    assert db.fetchColumn('select id from companies order by id') == [1, 2, 3, 4, 5]
    assert db.fetchColumn('select id from companies where id=7') == []

def test_fetchOne():
    assert db.fetchOne('select name from companies where id=:id', {'id': 1}) == 'Гугл Дисней'
    assert db.fetchOne('select name from companies where id=999') is None

def test_insert():
    # act
    company_id = db.insert('companies', dummy)
    found = db.fetchRow('select * from companies where id=:id', dummy)

    # assert
    assert found == dummy
    assert company_id == 100

def test_update():
    db.update('companies', new_dummy, "id="+str(dummy['id']))
    found = db.fetchRow('select * from companies where id=:id', new_dummy)

    # assert
    assert found == new_dummy

def test_cleanup():
    test_delete()

def test_insert_many():
    db.insert('companies', [dummy, new_dummy])
    found = db.fetchAll('select * from companies where id>=100 order by id')

    assert found == [dummy, new_dummy]

def test_cleanup2():
    test_delete()