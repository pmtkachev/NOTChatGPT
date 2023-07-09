import dis


class ServerMake(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []

        for f in clsdict:
            try:
                ret = dis.get_instructions(clsdict[f])
            except TypeError:
                pass
            else:
                for i in ret:
                    print(i)
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)

                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)

        print(methods)
        if 'connect' in methods:
            raise TypeError('Метод connect недопустим в серверном классе')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)


class ClientMake(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        for f in clsdict:
            try:
                ret = dis.get_instructions(clsdict[f])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for cmnd in ('accept', 'listen', 'socket'):
            if cmnd in methods:
                raise TypeError('В классе обнаружен запрещенный метод!')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)
