import socket

while True:

    while True:

        target_host = "192.168.100.11"
        target_port = 9100
        serial_number = 'VNF4R27155'

        print("""
Компания "Мастер Сервис" (https://masservice.ru/) представляет:
Утилиту для смены серийного номера на устройствах Hewlett-Packard
Обновляемый список поддерживаемых устройств https://disk.yandex.ru/d/SB8KCzflBCmlUA
Для обновления списка пишите на p13p@yandex.ru
        
        """)
        new_host = input('Введите ip принтера, по умолчанию (ENTER) ip = 192.168.100.11\n')
        if new_host:
            target_host = new_host
        new_sn = input('Введите серийный номер принтера, по умолчанию (ENTER) VNF4R27155\n')

        if new_sn:
            serial_number = new_sn.upper()
        print(f"""
Отправка {serial_number} на хост {target_host} - 
подтвердить (Enter) или ввести заново (любой символ и Enter)
        """)
        if not input():
            break

    job = [
        bytes('%-12345X@PJL\r\n', 'UTF-8'),
        # bytes('%-12345X@PJL RDYMSG DISPLAY="HACKED"\r\n', 'UTF-8'),
        bytes('@PJL SET SERVICEMODE=HPBOISEID\r\n', 'UTF-8'),
        bytes('@PJL SET SERIALNUMBER=', 'ASCII') + bytes(serial_number, 'ASCII') + bytes('\r\n', 'UTF-8'),
        bytes('@PJL SET SERVICEMODE=EXIT\r\n', 'UTF-8'),
        # bytes('@PJL RESET\r\n', 'UTF-8'),
        bytes('%-12345X', 'UTF-8')
    ]

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((target_host, target_port))
    except socket.error:
        print(f"""
Неудачная попытка соединения с хостом {target_host}
        """)
    except TimeoutError:
        print(f"""
Неудачная попытка соединения с хостом {target_host}
Проверьте ip адрес устройства и его доступность
        """)
    else:
        for b in job:
            soc.sendall(b)
        print(f"""
Новый серийный номер {serial_number} отправлен на хост {target_host}
Если устройство поддерживает PGL команду SET SERIALNUMBER, серийный номер изменён
            """)
    finally:
        soc.close()

    print(f"""
Закончить работу (Enter) или продолжить (любой символ и Enter)
    """)
    if not input():
        break
