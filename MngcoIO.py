from cryptography.fernet import Fernet


def read():
    dicts = {}
    lists = {}
    section = ''

    with open('C:\\Users\\nekta\\PycharmProjects\\Mango\\Project\\mango-constants.mngco', 'r') as file:
        data = file.read()

        key = data.split('\n')[0]
        keyObj = Fernet(key)

        encrypted = data.split('=\n')[1]
        decrypted = keyObj.decrypt(encrypted).decode()

    for line in decrypted.split('\n'):
        if line == '' or line[0:2] == '//':
            continue
        elif line[0] == '@':
            section = line
            dicts[line] = ''
            continue

        if ':' in line:
            dicts[line.split(':')[0]] = line.split(':')[1]
        elif line[0] == '@':
            pass
        elif section in lists:
            lists[section].append(line)
        else:
            lists[section] = [line]

    return dicts, lists


def read2():
    pairs = {}
    lists = {}
    section = ''

    with open('C:\\Users\\nekta\\PycharmProjects\\Mango\\Project\\mango-constants.mngco', 'r') as file:
        data = file.read()

        key = data.split('\n')[0]
        keyObj = Fernet(key)

        encrypted = data.split('=\n')[1]
        decrypted = keyObj.decrypt(encrypted).decode()

    for line in decrypted.split('\n'):
        if line == '' or line[0:2] == '//':
            continue
        elif line[0] == '@':
            section = line
            pairs[line] = ''
            continue
        if line == 'SYNTAX:FULL-ERROR':
            pass

        if ':' in line:
            if section not in pairs:
                pairs[section] = {}
            try:
                pairs[section][line.split(':')[0]] = line.split(':')[1]
            except TypeError:
                pairs[section] = {}
                pairs[section][line.split(':')[0]] = line.split(':')[1]

        elif section in lists:
            lists[section].append(line)
        else:
            lists[section] = [line]

    return pairs, lists
