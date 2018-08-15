import json
import re
import sys
import urllib.request, urllib.response
from collections import defaultdict
from itertools import product

import requests
from sync_config import SERVICE_URL, API_URL

import os

def getfunc(functext):
    # очищаем вход
    st = re.sub("[^ABCDabcd \(\)\!\+]", "", functext, len(functext))
    # добавляем and между перемножающимися скобками или в конструкциях вида a(b+c)
    st = re.sub(r"([abcdABCD\)])\s*\(", r"\1 & (", st)
    st = re.sub(r"\)\s*([abcdABCD])", r") & \1", st)
    st = re.sub(r"\)\s*\(", r") & (", st)
    # заменяем отрицания
    st = st.replace("!", " not ")
    # заменяем дизъюнкции
    st = st.replace("+", " or ")
    # Находим все конъюнктивные группы и меняем их
    p = re.findall("[abcdx]+", st, re.I)
    p.sort(key=len, reverse=True)
    for group in p:
        st = st.replace(group, " and ".join(list(group)))
    # заменяем a на not A и т.д.
    for c in list("ABCD"):
        st = re.sub("(?<!\w)" + c.lower() + "(?!\w)", " not " + c + " ", st)
    # убираем дублирующиеся пробелы
    st = re.sub(" +", " ", st)
    # заменяем & на and, раньше нельзя, чтобы "a" в and не путалось с переменной
    st = st.replace("&", "and")
    # print(st)
    f = lambda A, B, C, D: bool(eval(st))
    try:
        get_func_vector(f)
    except SyntaxError:
        print("Введенный вами код " + functext + " не является правильной логической функцией")
    else:
        return f


def get_func_vector(func):
    if func == "":
        return "0" * 16
    if not callable(func):
        func = getfunc(func)
    return "".join([str(int(func(A, B, C, D))) for A, B, C, D in product([0, 1], [0, 1], [0, 1], [0, 1])][::-1])


def modernize_date(date):
    return date.replace("2018", "2349")


def roundTo(val, prec=3):
    return round(val, prec - len(str(int(val))))


def table_view(data, free_space_right=4, free_space_left=1, column_separator="|"):
    datas = [x for x in data if isinstance(x, (list, tuple))]
    zipdata = list(zip(*datas))
    column_widths = [max([len(str(x)) for x in col]) + free_space_right + free_space_left for col in zipdata]
    line_width = sum(column_widths) + len(column_separator) * (len(zipdata) - 1)
    for item in data:
        if isinstance(item, str):
            print(item * line_width)
        else:
            while "sum" in item:
                ind = item.index("sum")
                item[ind] = sum(
                    [x[ind] for x in data if isinstance(x, (tuple, list)) and isinstance(x[ind], (int, float))])
            print(column_separator.join(
                [" " * free_space_left + "{:<{x}}".format(item[i], x=x - free_space_left) for i, x in
                 enumerate(column_widths)]).format(*item))


class Sync:
    def __init__(self):
        self.help_text = [line.strip() for line in open("commands.txt", 'r')]
        self.flight = {}
        self.nodes_data = {}
        self.node_names = {}
        self.param_names = {}
        self.param_short_names = {}
        self.sizes = {"small": "малый", 'medium': 'средний', 'large': 'большой'}
        self.companies = {'mst': "МарсСтройТрест", "mat": "Мицубиси Автоваз Технолоджи",
                          "kkg": "Красный Крест Генетикс",
                          "gd": "Гугл Дисней", "pre": "Пони РосКосмос Экспресс"}
        self.roles = {"pilot": "Пилот", "navigator": "Навигатор", "engineer": "Инженер", "supercargo": "Суперкарго",
                      "radist": "Радист"}
        self.engineer_id = 0

    def send_post(self, url, data=None):
        try:
            url = SERVICE_URL + url
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(data)
            jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))
            response = urllib.request.urlopen(req, jsondataasbytes)
            return response

            # r = requests.post(url, json=data or {})
            # return json.loads(r.text)
        except requests.exceptions.ConnectionError:
            print("Удаленный сервер не ответил по адресу " + url + ". Работа программы аварийно завершена")
            sys.exit()
        except json.decoder.JSONDecodeError:
            print(f"Не удалось расшифровать {r.text}")
            sys.exit()

    def mask(self, vector, total):
        return "".join([vector[i] if c == '1' else '*' for i, c in enumerate(list(total))])

    @staticmethod
    def check_account (login, password):
        try:
            url = API_URL + "/account"
            r = requests.get(url, auth=(login, password))
            return json.loads(r.text)
        except requests.exceptions.ConnectionError:
            print(f"Удаленный сервер {API_URL} не ответил. Работа программы аварийно завершена")
            sys.exit()

    def get_engineer_id(self):
        auto = False 
        if ('MAGELLAN_USER' in os.environ):
            login = os.environ['MAGELLAN_USER']
            auto = True
        else:
            login = input ("Введите логин / ID инженера> ")
        
        if ('MAGELLAN_PASS' in os.environ):
            password = os.environ['MAGELLAN_PASS']
            auto = True
        else:
            password = input ("Введите пароль> ")

        json = Sync.check_account(login, password)

        if (not ('account' in json)):
            print(f"Возможно пароль неверный")
            sys.exit()
        
        account = json['account']
            
        id = account['_id']
        isEngineer = account['professions']['isEngineer']

        if (not isEngineer):
            print(f"Терминал доступен только инженерам")
            sys.exit()

        if not auto:
            print("Вы можете установить переменные среды MAGELLAN_USER / MAGELLAN_PASS для автологина.")
            print("Не делайте это на общедоступных терминалах")
        
        if not account['jobs']['tradeUnion']['isEngineer']:
            print("ВНИМАНИЕ! Похоже, вы не член профсоюза")

        return id

    def node_show_name(self, node_data):
        if not node_data['node_name']:  # обычный узел
            return "{model_name} #{node_id}".format(**node_data)
        elif node_data['node_name'] == "{model_name}-{node_id}".format(**node_data):  # корпус с дефолтным именем
            return node_data['node_name']
        else:
            return "{node_name}, модель {model_name}".format(**node_data)

    def cmd_system(self, args):
        if not args:
            print("Команда system должна выполняться с дополнительными аргументами!")
            self.cmd_help(['system'])
            return

        if args[0] == 'list':
            self.cmd_system_list()

        elif args[0] == 'params':
            self.cmd_system_params(args)

        elif args[0] == 'slots':
            self.cmd_system_slots()

        elif args[0] == 'vector':
            self.cmd_system_vector(args)

        else:
            print("Аргумент {} для команды system не распознан".format(args[0]))
            self.cmd_help(["system"])

    def cmd_system_list(self):
        data = [["Код", "Система", "Узел"], "="]
        for node_type, name in self.node_names.items():
            data.append([node_type, name, self.node_show_name(self.nodes_data[node_type])])
        table_view(data)

    def count_system_slots(self):
        slots = defaultdict(dict)
        codes = {"*": "con", "+": "sum", "!": "inv"}
        datasource = {"hull": self.systems['hull']['slots'], **self.slots}

        for syst, data in datasource.items():
            for detail, dct in data.items():
                for slotcount, value in dct.items():
                    slots[codes[detail] + str(slotcount)][syst] = value if syst == 'hull' else -1 * value
        return slots

    def check_system_slots(self, slots={}):
        if slots == {}:
            slots = self.count_system_slots()
        if any([sum(x.values()) < 0 for x in slots.values()]):
            print("ВНИМАНИЕ! На корпусе не хватает слотов под детали для выбранных корректировочных функций!")
            return False
        return True

    def cmd_system_slots(self):
        all_details = set([])
        for row in self.nodes_data.values():
            all_details = all_details | set(row['slots'].keys())
        all_details = sorted(all_details)
        counter = defaultdict(int)
        lst = [["Узел"] + all_details, "="]
        mult = 1
        for row in sorted(self.nodes_data.values(), key=lambda x: x['node_type_code'] == 'hull', reverse=True):
            table_row = [self.node_names[row['node_type_code']]]
            for detail in all_details:
                detail_cnt = mult * row['slots'].get(detail, 0)
                table_row.append(detail_cnt)
                counter[detail] += detail_cnt
            lst.append(table_row)
            mult = -1 # Для всех, кроме корпуса, значения отрицательные
        lst.append("=")
        lst.append(["Итого"] + [counter[detail] for detail in all_details])
        table_view(lst)

    def cmd_system_vector(self, args):
        avail = list(self.nodes_data.keys()) + ['all']
        if len(args) == 1 or args[1] not in avail:
            print("Команде system vector надо указать код системы или all для вывода частотных векторов всех систем")
            return
        if args[1] == 'hull':
            print("Корпус влияет на синхронизацию всех систем, но сам системой не является")
            print("Введите system vector all для вывода векторов рассихнрона по всем системам, или "
                  "system vector (название системы), чтобы увидеть подробную информацию о ее векторе рассинхрона.")
            return

        if args[1] == 'all':
            lst = [["Узел", "Вектор рассинхрона"], "-"] + [
                [self.node_names[syst], self.nodes_data[syst].get('total')]
                for syst in self.nodes_data.keys()
                if syst != 'hull'
            ]
        else:
            syst = args[1]
            node_data = self.nodes_data[syst]
            hull_data = self.nodes_data['hull']
            print(self.node_names[syst] + ": вектор частот ")
            lst = [
                ["Система", "Вектор частот"],
                "=",
                [self.node_names[syst] + " " + self.node_show_name(node_data),
                 self.mask(node_data['node_vector'], node_data['vector'])],
                ["Корпус " + self.node_show_name(hull_data), self.mask(node_data['hull_vector'], node_data['vector'])],
                '-',
                ["Итого", node_data['vector']],
                ["Корректировка", node_data['correction']],
                ["Результат", node_data['total']]
            ]
        table_view(lst)

    def cmd_system_params(self, args):
        try:
            syst = args[1]
            if syst not in self.nodes_data.keys():
                raise IndexError
        except IndexError:
            print("В команду system params необходимо передать код интересующей системы"
                  " или all для вывода ТТХ всего корабля")
            return

        systdata = self.nodes_data[syst]

        print(f"""{self.node_names[syst]} {self.node_show_name(systdata)},""" +
              f""" уровень {systdata['level']}, размер {self.sizes[systdata['size']]}""")
        lst = [["Параметр", "Расчетное значение", "Синхронизация", "Текущее значение"], '=']
        for param_code, param_data in systdata['params'].items():
            lst.append([
                self.param_names[param_code],
                roundTo(param_data['value'] * 100 / param_data['percent']),
                f"{param_data['percent']}%",
                param_data['value']
            ])
        table_view(lst)

    def cmd_help(self, args):
        if len(args) == 0:
            lines = self.help_text[:]
        else:
            lines = [l for l in self.help_text if l.startswith(args[0])]
        print(
            "\n".join(lines) + "\n" if lines else "Неизвестная команда или запрос. Введите help для вывода всех команд")

    def cmd_correct(self, args):
        if len(args) == 0 or args[0] not in ['test', 'list'] + list(self.nodes_data.keys()):
            print("Команда correct используется одним из этих способов:")
            self.cmd_help(['correct'])
            return
        if args[0] == 'test':
            self.cmd_correct_test(args[1:])
        elif args[0] == 'list':
            self.cmd_correct_list()
        else:
            self.cmd_correct_system(args)

    def cmd_correct_test(self, args):
        functext = " ".join(args)
        try:
            vector = get_func_vector(functext)
        except:
            print(functext + " не является валидной логической функцией")
        else:
            print(vector)

    def cmd_correct_list(self):
        print("Список текущих корректировок")
        self.show_corrections()

    def set_system_correct(self, syst, functext):
        new_correction = self.send_post("sync/set_correction", {
            "flight_id": self.flight['id'],
            "node_type_code": syst,
            "correction": functext})
        if new_correction.get('status') == 'fail':
            print(new_correction.get('errors'))
            return
        self.nodes_data[syst] = new_correction['node_sync']
        print(f"Установлена корректирующая функция {functext}, вектор {new_correction['node_sync']['correction']}")

    def cmd_correct_system(self, args):
        syst = args[0]
        if len(args) == 1:
            self.show_corrections([syst])
            return
        functext = "".join(args[1:])
        self.set_system_correct(syst, functext)

    def get_flight_data(self):
        self.flight = self.send_post('mcc/get_nearest_flight_for_role',
                                     {"user_id": self.engineer_id, "role": "engineer"})
        if self.flight is None:
            print("Похоже, вы никуда не летите. Ждите вестей от ЦУП.")
            sys.exit()

        self.flight['departure'] = modernize_date(self.flight['departure'])
        print("""Данные по полету считаны:
        Номер полета: {id}
        Дата и время вылета: {departure}
        Номер дока: {dock}
Экипаж корабля: """.format(**self.flight))
        for role, user in self.flight['crew'].items():
            print(" " * 8 + self.roles[role] + ": " + user)

    def load_data(self):
        self.nodes_data = self.send_post("sync/get_build_data", {"flight_id": self.flight['id']})
        for val in self.nodes_data.values():
            val['params'] = json.loads(val['params_json'])
            val['slots'] = json.loads(val['slots_json'] or '{}')
            del (val['params_json'])
            del (val['slots_json'])
        params_and_nodes = self.send_post("get-params")
        self.param_names = {param['param_code']: param['param_name'] for param in params_and_nodes}
        self.param_short_names = {param['param_code']: param['param_short_name'] for param in params_and_nodes}
        self.node_names = {param['node_code']: param['node_name'] for param in params_and_nodes}

    def show_corrections(self, systems=None):
        if systems is None:
            systems = self.nodes_data.keys()
        for syst in systems:
            if not self.nodes_data[syst]['correction_func']:
                print(self.node_names[syst] +
                      f": корректирующая функция не установлена. Введите correct {syst} <текст функции>, чтобы ее установить")
            else:
                row = self.nodes_data[syst]
                print(self.node_names[syst] +
                      f": корректирующая функция {row['correction_func']} (частотный вектор {row['correction']})")

    def cmd_save(self):
        if self.check_system_slots():
            pass  # Отправить данные в БД
            print("Данные сохранены")

    def terminal(self):
        while True:
            args = [x for x in input("\n> ").split(" ") if x]
            if not args:
                continue
            command, *args = args
            command = command.lower()
            if command in ('exit', 'halt', 'stop', 'quit'):
                input("Получена команда отключения от терминала. Нажмите Enter для выхода.\n")
                break
            elif command == 'help':
                self.cmd_help(args)
            elif command == "system":
                self.cmd_system(args)
            elif command == "correct":
                self.cmd_correct(args)
            else:
                print(
                    "Команда " + command + " не распознана. Введите help для вывода всех команд или help <имя команды> "
                                           "для получения справки о команде")


if __name__ == "__main__":
    s = Sync()
    s.engineer_id = s.get_engineer_id()
    s.get_flight_data()
    s.load_data()
    s.terminal()
