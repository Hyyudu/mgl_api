import json
from collections import defaultdict

from convert import roundTo
from src.sync.magellan import get_func_vector, getfunc, table_view, count_elements
from src.sync.nodes_data import node_names, node_params, param_names
from src.sync.desync_penalties import desync_penalties


class Sync:
    def __init__(self):
        self.help_text = [line.strip() for line in open("commands.txt", 'r')]
        self.freq_vectors = defaultdict(dict)
        self.systems = defaultdict(dict)
        self.corrections = {}
        self.slots = {}

    def xor(self, freq_vectors) -> str:
        zp = zip(*freq_vectors)
        arr = [str(x.count('1') % 2) for x in zp]
        return "".join(arr)

    def mask(self, vector, total):
        return "".join([vector[i] if c == '1' else '*' for i, c in enumerate(list(total))])

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

        elif args[0] == 'affected':
            self.cmd_system_affected(args)

        else:
            print("Аргумент {} для команды system не распознан".format(args[0]))
            self.cmd_help(["system"])

    def cmd_system_list(self):
        data = [["Код", "Система", "Марка"], "="] + [
            [node, name, self.systems[node].get("name")] for node, name in node_names.items()
        ]
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
        slots = self.count_system_slots()
        lst = [["Система"] + sorted(slots.keys())]
        for syst in sorted(self.systems.keys(), key=lambda x: x != 'hull'):
            lst += [[node_names[syst]] + [slots[detail].get(syst, 0) for detail in lst[0][1:]]]
        lst += ["="]
        lst += [["Итого"] + ["sum"] * (len(lst[0]) - 1)]
        table_view(lst, free_space_right=1)
        self.check_system_slots(slots)

    def cmd_system_vector(self, args):
        avail = list(self.freq_vectors.keys()) + ['all']
        if args[1] == 'hull':
            print("Корпус влияет на синхронизацию всех систем, но сам системой не является")
            print("Введите system vector all для вывода векторов рассихнрона по всем системам, или "
                  "system vector (название системы), чтобы увидеть подробную информацию о ее векторе рассинхрона.")
            return

        if len(args) == 1 or args[1] not in avail:
            print("Команде system vector надо указать код системы или all для вывода частотных векторов всех систем")
            return
        if args[1] == 'all':
            lst = [["Узел", "Вектор рассинхрона"], "-"] + [
                [node_names[syst], self.freq_vectors[syst].get('result', self.freq_vectors[syst]['total'])]
                for syst in self.freq_vectors.keys()
            ]
        else:
            syst = args[1]
            syst_vector = self.freq_vectors[syst]
            print(node_names[syst] + ": вектор частот ")
            lst = [["Система", "Вектор частот"], "-"] + [
                [node_names[sys] + ' ' + self.systems[sys].get('name'), self.mask(syst_vector[sys], syst_vector['total'])]
                for sys in syst_vector.keys()
                if sys not in ('total', 'correct', 'result')
            ] + ["=", ["Суммарно", syst_vector['total']]]
            if len(syst_vector.get('correct', '')) > 0:
                lst += [["Корректировка", syst_vector.get('correct')], ["Итого", syst_vector.get('result')]]

        table_view(lst)

    def cmd_system_affected(self, args):
        avail = list(self.freq_vectors.keys())
        if len(args) < 2:
            print("Для команды system affected надо указать код проверяемой системы. Например, system affected march_engine")
            return
        if args[1] not in avail:
            print("Указан код несуществующей системы: "+args[1])
            print("Для команды system affected надо указать код проверяемой системы. Например, system affected march_engine")
            return
        syst = self.systems[args[1]]
        sys_code = syst['type']
        print(node_names[syst['type']]+' '+syst['name'])
        lst = [["Параметр", "Штатное значение", "Текущее значение"], "-",]
        for param, val in syst['params'].items():
            arr = [param_names[param], val]
            func = desync_penalties[syst['type']].get(param, lambda s: 0)
            percent = 100 + func(self.freq_vectors[sys_code]['result'])
            arr.append("{}% ({})".format(percent, roundTo(val*percent/100)))
            lst.append(arr)
        table_view(lst)

    def cmd_system_params(self, args):
        try:
            syst = args[1]
            if syst not in list(self.systems) + ['all']:
                raise IndexError
        except IndexError:
            print("В команду system params необходимо передать код интересующей системы"
                  " или all для вывода ТТХ всего корабля")
            return
        if syst != 'all':
            systdata = self.systems[syst]
            print(node_names[syst] + " " + systdata.get("name"))
            for param, value in systdata['params'].items():
                print(" " * 10 + param_names[param] + ": " + str(value))
        else:
            print("Массогабаритные характеристики корабля:")
            sdata = [
                [node_names[sys],
                 self.systems[sys]['params']['weight'],
                 self.systems[sys]['params']['volume'] * (1 if sys == 'hull' else -1)
                 ] for sys in self.systems.keys()]
            zdata = list(zip(*sdata))
            lst = [["Система", "Масса", "Объем"], '='] + sdata + ["=", [
                "Итого", "sum", "sum"
            ]]
            table_view(lst)

    def cmd_help(self, args):
        if len(args) == 0:
            lines = self.help_text[:]
        else:
            lines = [l for l in self.help_text if l.startswith(args[0])]
        print(
            "\n".join(lines) + "\n" if lines else "Неизвестная команда или запрос. Введите help для вывода всех команд")

    def cmd_correct(self, args):
        if len(args) == 0 or args[0] not in ['test', 'list'] + list(self.freq_vectors.keys()):
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
            vector = get_func_vector(getfunc(functext))
        except:
            print(functext + " не является валидной логической функцией")
        else:
            print(vector)

    def cmd_correct_list(self):
        print("Список текущих корректировок")
        self.show_corrections()

    def set_system_correct(self, syst, functext):
        func = getfunc(functext)
        if not func:
            return
        vector = get_func_vector(func)
        if vector == "0" * 16:
            functext = ""
        self.corrections[syst] = functext
        fvs = self.freq_vectors[syst]
        fvs['correct'] = vector
        fvs['result'] = self.xor([fvs['total'], vector])
        if functext:
            print("{}: установлена корректирующая функция {} (частотный вектор {})".format(
                node_names[syst],
                functext,
                vector
            ))
        else:
            print(node_names[syst] + ": корректирующая функция сброшена")
        self.slots[syst] = count_elements(functext)

    def cmd_correct_system(self, args):
        syst = args[0]
        if len(args) == 1:
            self.show_corrections([syst])
            return
        functext = "".join(args[1:])
        self.set_system_correct(syst, functext)

    def load_data(self):
        sync_data = json.load(open("sync_data.json"))
        for system, sysdata in sync_data.items():
            self.systems[system] = node_params[sysdata.get('id')]
            for sys, fv in sysdata['freq_vectors'].items():
                self.freq_vectors[sys][system] = fv
        for sys, sysdata in self.freq_vectors.items():
            self.freq_vectors[sys]['total'] = self.xor(sysdata.values())
            self.freq_vectors[sys]['correct'] = '0'*16
            self.freq_vectors[sys]['result'] = self.freq_vectors[sys]['total']

    def show_corrections(self, systems=[]):
        if systems == []:
            systems = self.freq_vectors.keys()
        for syst in systems:
            if self.corrections.get(syst) is None:
                print(node_names[
                          syst] + ": корректирующая функция не установлена. Введите correct {} <текст функции>, чтобы ее установить".format(
                    syst))
            else:
                print("{}: корректирующая функция {} (частотный вектор {})".format(
                    node_names[syst],
                    self.corrections[syst],
                    self.freq_vectors[syst]['correct']
                ))

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
            elif command == 'save':
                self.cmd_save()
            else:
                print(
                    "Команда " + command + " не распознана. Введите help для вывода всех команд или help <имя команды> "
                                           "для получения справки о команде")


if __name__ == "__main__":
    s = Sync()
    s.load_data()
    s.terminal()
