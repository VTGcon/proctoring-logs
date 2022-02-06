import pprint
import requests
import re
pprint.sorted = lambda x, key=None: x


# for no db error
output = {"Тип важности": 'error', "message": 'no db', "file": '', "token": '', "log": [], "date": ''}

# for browser info
info_of_browser = {"Тип важности": 'info', "message": 'Used browser', "file": "/frontend/src/pages/Client.js",
                   "token": '', 'log': '', "date": ''}
list_of_browser_info = []

# for host
info_of_host = {"Тип важности": "info", "message": "Host + port", "file": "/backend/bin/www", "log": "", "date": ""}
host_list = []

# two task. Not chromium and end by pressing cross
dict_cse_and_nce = {"Тип важности": "info", "message": "",  # cross session end and not chrome error
                    "file": "/frontend/src/pages/Client.js",
                    "token": '', "log": [], "date": ""}

# message and what to check
wtc_1 = 'Сессия завершена нажатием на крестик'
wtc_2 = 'Поменяйте браузер на Chrome или Chromium, в ином случае у вас не получится пройти экзамен'
mes_1 = 'Сессия завершена нажатием на крестик'
mes_2 = 'Пользователь зашел на сайт не через хромиум'

# markup
markup_error_dict = {"Тип важности": "warning", "file": "/frontend/src/pages/Watch.js", "token": "", "log": "",
                     "date": ""}
list_of_markup_error = []

# db message
db_mes_dict = {"Тип важности": "info", "message": "DB connection successful", "file": "/backend/db/db.js", "log": "",
               "date": ""}
list_of_db_mes = []

# list of containers to check
list_ch = ['xqueue', 'proctoring_kurento', 'portainer', 'proctoring_turn', 'proctoring_frontend',
           'proctoring_backend', 'proctoring_mongo', 'ml_screencast_service', 'ml_webcam_service']

# list for record check
record_dict = {"Тип важности": "info", "message": "",
               "file": "/frontend/src/pages/Client.js",
               "token": '', "log": [], "date": ""}
wts_1 = ['Пользовать остановил запись,', "Пользовать уверен, что хочет остановить запись,"]
wts_2 = ['Пользовать нажал начать запись,', "Пользовать уверен, что хочет начать запись,"]

# pars violations
list_to_pars_violations = ['run parse python script', 'res:', 'Exit with code:', 'err:', 'current_markup']


def take_logs_from_gh(token, file_name):
    url = 'https://raw.githubusercontent.com/OSLL/proctoring-logs/main/examples/' + file_name + '.txt?token=' + token
    r = requests.get(url)
    result = []
    bytes_ = b''
    for chunk in r:
        bytes_ += chunk
    alp = bytes_.split(b'\n')
    for x in alp:
        tech = x.decode('utf8')
        result.append(tech)
    return result


def take_log_from_file(file_name):
    file = open('examples/' + file_name + '.txt', 'r', encoding="utf-8").read()
    lines = file.split('\n')
    return lines


# don't work and don't necessary
'''
def create_df(res):
    start = 0
    for line in res:
        if len(line) < 4:
            start += 1
        else:
            first_word = line[0] + line[1] + line[2] + line[3]
            if first_word == "STAT":
                break
            else:
                start += 1
    test_list = res[start::]
    data_list = {'token': [], 'stat': [], 'time': []}
    trash = []
    stat = 0
    for line in test_list:
        if stat == 0:
            if line[0] + line[1] + line[2] + line[3] != "STAT":
                break
        l = line.replace('STAT, for token  ', '')
        l = l.split(' ,  ')
        for x in l:
            if x == '{':
                stat = 1
                continue
            if x == '}':
                stat = 0
                data_list['stat'].append(trash)
                trash = []
            if stat == 1:
                trash.append(x)
            if x == l[0] and stat == 0 and x != '}':
                data_list['token'].append(x)
            if len(l) == 2 and x == l[1]:
                data_list['stat'].append('no violations')
    df = pd.DataFrame(data=data_list)
    return df
'''


def find_containers(res):
    stat = 0
    exist = 0
    containers = []
    for line in res:
        if line == '+ docker ps -a':
            stat = 1
            exist = 1
        if line == '+ [ ! -z proctoring_backend ]':
            break
        if stat == 1:
            containers.append(line)
    if exist == 0:
        print('no containers exist')
    containers = containers[2::]
    return containers


def check_docker(res, list_to_check):
    containers = find_containers(res)
    new = []
    con_names = []
    for line in containers:
        trash = line.split()
        con_names.append(trash[-1])
        new.append(trash)
    con_names = sorted(con_names)
    list_to_check = sorted(list_to_check)
    if con_names != list_to_check:
        print('containers don\'t match\n')
    else:
        print('No problems with run containers\n')
    for line in new:
        if '(unhealthy)' in line:
            print('container ', line[-1], ' is unhealthy')


def stud_online(logs):
    logs = list(reversed(logs))
    stat = 0
    for line in logs:
        words = line.split()
        if len(words) > 0 and 'ONLINE:' in words:
            print('\nNow number of online sessions are {0}\n'.format(words[1]))
            stat = 1
            break
    if stat == 0:
        print('No online sessions exist')


def no_db_error(res):
    no_db_error = []
    log = {'I': [], 'II': [], 'III': [], 'IV': []}
    stat_of_read = 0
    for line in res:
        for_II = []
        for_IV = []
        line = line.split()
        # print(line)
        if len(line) > 4 and line[3] == 'No' and line[4] == 'db':
            if line[-1][0:-1] == output['token']:
                continue
            else:
                stat_of_read = 1
                token = line[-1][0:-1]
                output['token'] = token
                output['date'] = ' '.join(line[0:3])
        if stat_of_read == 1:
            no_db_error.append(line)
        if len(line) > 0 and stat_of_read == 1 and line[0] == '},':
            for string in no_db_error:
                if len(string) == 2 and string[0] == 'at':
                    output['file'] = string[-1]
            stat = 0
            stat_2 = 0
            for line_2 in res:
                if 'Success' and 'to' and 'post' and 'webcam' and 'markup' and output['token'] in line_2.replace(',',
                                                                                                                 '').split():
                    # if line_2[0:99] == str(output['date'] + ' Success to post webcam markup ' + output['token']+','):
                    log['I'] = output['date'] + ' Success to post webcam markup ' + output['token']
                if len(line_2) > 17 and line_2[
                                        (len(output['date']) + 1):(len(output['date']) + 17)] == 'db before update':
                    string = line_2.split()
                    if output['token'] in string:
                        stat = 1
                if stat == 1:
                    for_II.append(line_2)
                if len(line_2) > 0 and stat == 1 and line_2 == '},':
                    log['II'] = for_II[1::]
                    for_II = []
                    stat = 0
                if len(line_2) > 24 and line_2[(len(output['date']) + 1):(
                        len(output['date']) + 25)] == 'test that db is updated.':
                    string = line_2.split()
                    if output['token'] in string:
                        stat_2 = 1
                if stat_2 == 1:
                    for_IV.append(line_2)
                if len(line_2) > 0 and stat_2 == 1 and line_2 == '},':
                    # print(for_IV[1::])
                    log['IV'] = for_IV[1::]
                    for_IV = []
                    stat_2 = 0
            for_III = []
            for line in no_db_error[1::]:
                line = " ".join(line)
                for_III.append(line)
            log['III'] = for_III
            output['log'] = log
            pprint.pprint(output)
            print('\n')
            stat_of_read = 0
            no_db_error = []


def browser_info(res):
    for line in res:
        if 'Browser for token' in line:
            work_line = line.split()
            if info_of_browser['date'] == ' '.join(work_line[0:3]) and info_of_browser['token'] == work_line[3].replace(
                    '[', '').replace(']', ''):
                continue
            else:
                info_of_browser['date'] = ' '.join(work_line[0:3])
                info_of_browser['token'] = work_line[3].replace('[', '').replace(']', '')
                info_of_browser['log'] = ' '.join(work_line[10::])
                list_of_browser_info.append(info_of_browser.copy())
    return list_of_browser_info


def host_info(res):
    for line in res:
        if 'the HOST:' in line:
            work_line = line.split()
            if info_of_host['log'] == work_line[-1]:
                continue
            else:
                info_of_host['log'] = work_line[-1]
                host_list.append(info_of_host.copy())
    return host_list


def markup_error(res):
    for line in res:
        if 'Ошибки вывода markup' in line:
            work_line = line.split()
            if markup_error_dict['date'] == ' '.join(work_line[0:3]) and markup_error_dict['token'] == work_line[
                3].replace('[', '').replace(']', ''):
                continue
            else:
                info_of_browser['token'] = work_line[3].replace('[', '').replace(']', '')
                markup_error_dict['date'] = ' '.join(work_line[0:3])
                markup_error_dict['log'] = work_line[8::]
                list_of_markup_error.append(markup_error_dict.copy())
    return list_of_markup_error


def db_message(res):
    for line in res:
        if 'DB connection successful' in line:
            work_line = line.split()
            if db_mes_dict['date'] == ' '.join(work_line[0:3]):
                continue
            else:
                db_mes_dict['date'] = ' '.join(work_line[0:3])
                list_of_db_mes.append(db_mes_dict.copy())
    return list_of_db_mes


def violation(res):
    list_of_viol = []
    tokens = []
    stat = 0
    byf = []
    viol_dict = {"Тип важности": "info", "message": "Statistics from ML",
                 "file": '/backend/routes/studentData.js', 'token': '', 'log': '', 'date': ''}
    for line in res:
        if 'STAT, for token' in line:
            work_line = line.replace('STAT, for token', '').replace(",", '').split()
            if len(work_line) > 3 and work_line[3] in tokens:
                continue
            if len(work_line) > 3:
                viol_dict['token'] = work_line[3]
                tokens.append(work_line[3])
                viol_dict['date'] = ' '.join(work_line[0:3])
                if work_line[-1] == '{':
                    stat = 1
                else:
                    viol_dict['log'] = work_line[-1]
                    list_of_viol.append(viol_dict.copy())

        if stat == 1:
            if line == '},' or line == '}':
                stat = 0
                viol_dict['log'] = byf[1::]
                byf = []
                list_of_viol.append(viol_dict.copy())
            else:
                byf.append(line)
    return list_of_viol


def ml_service(res):
    tokens = []
    ml_dict = {"Тип важности": "info", "message": "Post authorization token to ML",
               "file": "/backend/routes/ml/authToken.js", "log": "", "date": ""}
    ml_list = []
    for line in res:
        if 'post authorization token to ML:' in line:
            work_line = line.replace('post authorization token to ML:', '').replace(',', '').split()
            if work_line[-2] in tokens:
                continue
            else:
                tokens.append(work_line[-2])
                ml_dict['date'] = ' '.join(work_line[0:3])
                ml_dict['log'] = ' '.join(work_line[3::])
                ml_list.append(ml_dict.copy())
    return ml_list


def record(res, what_to_search):
    record_list = []
    stat = 0
    tokens = []
    for line in res:
        if re.findall(what_to_search[0], line):
            if stat == 1:
                if len(record_dict['log']) == 1:
                    record_dict['message'] = what_to_search[0] + " но не подтвердил действие"
                record_list.append(record_dict.copy())
                stat = 0
            work_line = line.replace(what_to_search[0], '').replace(']', '').replace('[', '').split()
            if work_line[3] in tokens:
                continue
            else:
                tokens.append(work_line[3])
                record_dict['message'] = what_to_search[0][0:-1]
                record_dict['log'].append(line)
                record_dict['token'] = work_line[3]
                record_dict['date'] = ' '.join(work_line[0:3])
                stat = 1

        if re.findall(what_to_search[1], line):
            record_dict['log'].append(line)
    if len(record_dict['log']) == 1:
        record_dict['message'] = what_to_search[0] + " но не подтвердил действие"
        record_list.append(record_dict.copy())
    if len(record_dict['log']) == 2:
        record_list.append(record_dict.copy())
    return record_list


def check_some(res, what_to_check, mes):
    ultimate_list = []
    tokens = []
    for line in res:
        if re.findall(what_to_check, line) != []:
            work_line = line.replace(what_to_check, '') \
                .replace(']', '').replace('[', '').split()
            if len(work_line) > 3 and work_line[3] in tokens:
                continue
            if len(work_line) > 3:
                tokens.append(work_line[3])
                dict_cse_and_nce['message'] = mes
                dict_cse_and_nce['log'] = line
                dict_cse_and_nce['token'] = work_line[3]
                dict_cse_and_nce['date'] = ' '.join(work_line[0:3])
                ultimate_list.append(dict_cse_and_nce.copy())
    return ultimate_list


def violation_pars_list(res, list_of_violations_to_pars):
    full_list = []
    byf = []
    stat = 0
    dict_to_pull = {"Тип важности": "info", "message": "Парсинг нарушений",
                    "file": "/backend/utils/parseVideoWithMarkup.js", "log": "", "date": ""}
    for line in res:
        if re.findall(list_of_violations_to_pars[0], line) != [] or re.findall(list_of_violations_to_pars[1],
                                                                               line) != [] or re.findall(
                list_of_violations_to_pars[2], line):
            work_line = line.split()
            if len(work_line) > 3 and work_line[0][0] == '[':
                dict_to_pull['date'] = ' '.join(work_line[0:3])
            dict_to_pull['Тип важности'] = 'info'
            dict_to_pull['log'] = line
            if dict_to_pull not in full_list:
                full_list.append(dict_to_pull.copy())

        if re.findall(list_of_violations_to_pars[3], line) != []:
            work_line = line.split()
            if len(work_line) > 3 and work_line[0][0] == '[':
                dict_to_pull['date'] = ' '.join(work_line[0:3])
            dict_to_pull['Тип важности'] = 'error'
            dict_to_pull['log'] = line
            if dict_to_pull not in full_list:
                full_list.append(dict_to_pull.copy())

        if re.findall(list_of_violations_to_pars[4], line) != []:
            work_line = line.split()
            if len(work_line) > 3 and work_line[0][0] == '[':
                dict_to_pull['date'] = ' '.join(work_line[0:3])
            dict_to_pull['Тип важности'] = 'info'
            if work_line[-1] == '{,' or work_line[-1] == '{':
                stat = 1
            else:
                dict_to_pull['log'] = line
        if stat == 1:
            if line == '},' or line == '},\x01,':
                byf.append(line)
                dict_to_pull['log'] = byf
                if dict_to_pull not in full_list:
                    full_list.append(dict_to_pull.copy())
                stat = 0
                byf = []
            else:
                byf.append(line)
    return full_list


#############
#for task 75, can find any line
list_of_lines_info = [
    'run parse python script',                          #62
    'current_markup',                                   #62
    'res:',                                             #62
    'Exit with code:',                                  #62
    'post authorization token to ML:',                  #42
    'DB connection successful',                         #40
    'Browser for token',                                #37
    'Поменяйте браузер на Chrome или Chromium, '
    'в ином случае у вас не получится пройти экзамен',  #50
    'Сессия завершена нажатием на крестик'             #49
]
list_of_lines_errors = [
    'err:',                         #62
    'Ошибки вывода markup',         #39
]




def ultimate_to_find(log, words, token_ex, multi_line, end):
    #tune the dict
    dict_form = {
        "Тип важности": "none",
        "message": "",
        'token': "",
        "log": "",
        "date": ""
    }
    if token_ex == 0:
        del dict_form['token']
    if words in list_of_lines_info:
        dict_form['Тип важности'] = 'info'
    if words in list_of_lines_errors:
        dict_form['Тип важности'] = 'error'

    dict_form['message'] = words

    #func elements
    byf = []           # for multi line finding
    global_list = []   # for a lot of dicts
    stat = 0

    #start
    for line in log:
        if re.findall(words, line) != []:
            work_line = line.split()
            if len(work_line) > 3 and work_line[0][0] == '[':
                dict_form['date'] = ' '.join(work_line[0:3])
            if token_ex == 1:
                dict_form['token'] = re.findall(r'\w{24}', line)[0]
            if multi_line == 1:
                stat = 1
            if multi_line == 0:
                dict_form['log'] = line
        if multi_line == 0 and dict_form not in global_list and len(dict_form['log']) > 6:
            global_list.append(dict_form.copy())


        if stat == 1:
            byf.append(line)
        if line in end:
            stat = 0
            byf.append(line)
            dict_form['log'] = byf
            byf = []
            if dict_form not in global_list and len(dict_form['log']) > 6:
               global_list.append(dict_form.copy())
               byf = []
    if dict_form not in global_list and len(dict_form['log']) > 6:
        global_list.append(dict_form.copy())
        byf = []

    return global_list[0::]  

  
def stud_tab(res):
    form_dict = {"Тип важности": "", "message": "Страница с таблицей", "token": "",
               "file": "/frontend/src/pages/SessionTable.js", "log": "", "date": ""}
    check_1 = 'session_processing_end'
    check_2 = 'err in student data'
    table_list = []
    for line in res:
        if re.findall(check_1, line) != []:
            form_dict['Тип важности'] = "info"
            work_line = line.replace(check_1, '') \
                .replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['token'] = work_line[3]
                form_dict['date'] = ' '.join(work_line[0:3])
                table_list.append(dict_cse_and_nce.copy())
            if form_dict not in table_list:
                table_list.append(form_dict.copy())
        if re.findall(check_2, line) != []:
            form_dict['Тип важности'] = "error"
            work_line = line.replace(check_1, '') \
                .replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['token'] = work_line[3]
                form_dict['date'] = ' '.join(work_line[0:3])
                table_list.append(dict_cse_and_nce.copy())
            if form_dict not in table_list:
                table_list.append(form_dict.copy())
    return  table_list  
  
def video_record(res):
    form_dict = {"Тип важности": "", "message": "", "token": "",
                 "file": "/frontend/src/pages/Client.js", "log": "", "date": ""}
    check_1 = 'in progress,'
    check_2 = 'not started,'
    check_3 = 'finished,'
    video_list = []
    for line in res:
        if re.findall(check_1, line) != []:
            form_dict['Тип важности'] = "info"
            form_dict['message'] = "Запись видео началась"
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['token'] = work_line[3]
                form_dict['date'] = ' '.join(work_line[0:3])
            if form_dict not in video_list:
                video_list.append(form_dict.copy())

        if re.findall(check_2, line) != []:
            form_dict['Тип важности'] = "error"
            form_dict['message'] = "Запись видео не началась"
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['token'] = work_line[3]
                form_dict['date'] = ' '.join(work_line[0:3])
            if form_dict not in video_list:
                video_list.append(form_dict.copy())

        if re.findall(check_3, line) != []:
            form_dict['Тип важности'] = "info"
            form_dict['message'] = "Запись видео завершилась"
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['token'] = work_line[3]
                form_dict['date'] = ' '.join(work_line[0:3])
            if form_dict not in video_list:
                video_list.append(form_dict.copy())

    return video_list

def user_add(res):
    form_dict = {"Тип важности": "info", "message": "Добавление нового пользователя в админы",
                 "file": "/backend/routes/usersdb.js", "log": "", "date": ""}
    check = 'Успешно добавлен'
    users_list = []
    for line in res:
        if re.findall(check, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
            if form_dict not in users_list:
                users_list.append(form_dict.copy())
    return users_list  
  
 def user_del(res):
    form_dict = {"Тип важности": "info", "message": "Удаление нового пользователя из админов",
                 "file": "/backend/routes/usersdb.js", "log": "", "date": ""}
    check = 'Успешно удалён'
    users_list = []
    for line in res:
        if re.findall(check, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
            if form_dict not in users_list:
                users_list.append(form_dict.copy())
    return users_list  

#stat
def admins(res):
    admin_list = []
    stat = 0
    byf = []
    check = 'admins array'
    admins_dict = {"Тип важности": "info", "message": "Список админов",
                 "file": '/backend/routes/studentData.js', 'log': '', 'date': ''}
    for line in res:
        if re.findall(check, line) != []:
            work_line = line.split()
            if len(work_line) > 3:
                admins_dict['date'] = ' '.join(work_line[0:3])
                stat = 1

        if stat == 1:
            if line == ']' or line == '],':
                stat = 0
                admins_dict['log'] = byf[1::]
                byf = []
                if admins_dict not in admin_list:
                    admin_list.append(admins_dict.copy())
            else:
                byf.append(line)
    return admin_list  

#error
def video_upload_error(res):
    vid_list = []
    stat = 0
    byf = []
    check = 'fileSize: 0,'
    vid_dict = {"Тип важности": "error", "message": "Ошибка загрузки видео",
                 "file": '/backend/routes/links/file.js', 'log': '', 'date': ''}
    for line in res:
        if re.findall(check, line) != []:
            work_line = line.split()
            if len(work_line) > 3:
                vid_dict['date'] = ' '.join(work_line[0:3])
                stat = 1

        if stat == 1:
            if line == '}' or line == '},':
                stat = 0
                vid_dict['log'] = byf
                byf = []
                if vid_dict not in vid_list:
                    vid_list.append(vid_dict.copy())
            else:
                byf.append(line)
    return vid_list  
 
#error/info
def webcam_error_status(res):
    webcam_er = []
    stat = 0
    byf = []
    check_1 = 'update_post markup webсam'
    check_2 = 'THIS FILE FOR WEBCAM MARKUP'
    check_3 = 'Processing student webcam failed'
    webcam_er_dict = {"Тип важности": "info", "message": "Ошибка загрузки видео", "token": "",
                 "file": '/backend/routes/ml/markup.js', 'log': '', 'date': ''}
    for line in res:
        if re.findall(check_2, line) != [] and webcam_er_dict['token'] != '':
            work_line = line.split()
            if len(work_line) > 3:
                webcam_er_dict['date'] = ' '.join(work_line[0:3])
                stat = 1

        if re.findall(check_1, line) != []:
            work_line = line.split()
            webcam_er_dict['token'] = work_line[-1]

        if stat == 1:
            if line == '}' or line == '},' or line == '},\x01,':
                stat = 0
                webcam_er_dict['log'] = byf
                byf = []
                if webcam_er_dict not in webcam_er:
                    webcam_er.append(webcam_er_dict.copy())
                    webcam_er_dict = {"Тип важности": "info", "message": "Ошибка загрузки видео", "token": "",
                                "file": '/backend/routes/links/file.js', 'log': '', 'date': ''}
            else:
                if re.findall(check_3, line) != []:
                    webcam_er_dict['Тип важности'] = 'error'
                byf.append(line)
    return webcam_er

#error/info
def webcam_error_part_2(res):
    byf = []
    webcam_er_p2 = []
    stat = 0
    check_1 = 'Success to post webcam markup'
    check_2 = 'webcamMarkup error for token'
    webcam_er_dict_p2 = {"Тип важности": "info", "message": "В бд внесены нарушений с вебкамеры", "token": "",
                         "file": '/backend/routes/ml/markup.js', 'log': '', 'date': ''}
    for line in res:
        if re.findall(check_1, line) != []:
            webcam_er_dict_p2['Тип важности'] = "info"
            webcam_er_dict_p2['message'] = "В бд внесены нарушений с вебкамеры"
            work_line = line.split()
            if len(work_line) > 3:
                webcam_er_dict_p2['date'] = ' '.join(work_line[0:3])
                webcam_er_dict_p2['token'] = work_line[-1]
                stat = 1

        if re.findall(check_2, line) != []:
            webcam_er_dict_p2['Тип важности'] = "error"
            webcam_er_dict_p2['message'] = "В бд не внесены нарушений с вебкамеры"
            work_line = line.split()
            if len(work_line) > 3:
                webcam_er_dict_p2['date'] = ' '.join(work_line[0:3])
                webcam_er_dict_p2['token'] = work_line[-1]
                stat = 1

        if stat == 1:
            if line == '}' or line == '},' or line == '},\x01,':
                stat = 0
                webcam_er_dict_p2['log'] = byf
                byf = []
                if webcam_er_dict_p2 not in webcam_er_p2:
                    webcam_er_p2.append(webcam_er_dict_p2.copy())
            else:
                byf.append(line)

    return webcam_er_p2
  

#error/info
def screencast_error_status(res):
    screen_er = []
    stat = 0
    byf = []
    check_1 = 'update_post markup screen'
    check_2 = 'THIS FILE FOR WEBCAM MARKUP'
    check_3 = 'Processing student webcam failed'
    screen_er_dict = {"Тип важности": "info", "message": "Нарушения скринкаста", "token": "",
                 "file": '/backend/routes/ml/screencastMark.js', 'log': '', 'date': ''}
    for line in res:
        if re.findall(check_2, line) != [] and screen_er_dict['token'] != '':
            work_line = line.split()
            if len(work_line) > 3:
                screen_er_dict['date'] = ' '.join(work_line[0:3])
                stat = 1

        if re.findall(check_1, line) != []:
            work_line = line.split()
            screen_er_dict['token'] = work_line[-1]

        if stat == 1:
            if line == '}' or line == '},' or line == '},\x01,':
                stat = 0
                screen_er_dict['log'] = byf
                byf = []
                if screen_er_dict not in screen_er:
                    screen_er.append(screen_er_dict.copy())
                    screen_er_dict = {"Тип важности": "info", "message": "Нарушения скринкаста", "token": "",
                                "file": '/backend/routes/ml/screencastMark.js', 'log': '', 'date': ''}
            else:
                if re.findall(check_3, line) != []:
                    screen_er_dict['Тип важности'] = 'error'
                byf.append(line)
    return screen_er


#error/info
def screencast_error_part_2(res):
    byf = []
    screen_er_p2 = []
    stat = 0
    check_1 = 'Success to post screencast markup'
    check_2 = 'screenCastMarkup error for:'
    screen_er_dict_p2 = {"Тип важности": "info", "message": "В бд внесены нарушения скринкаста", "token": "",
                         "file": '/backend/routes/ml/screencastMark.js', 'log': '', 'date': ''}
    for line in res:
        if re.findall(check_1, line) != []:
            screen_er_dict_p2['Тип важности'] = "info"
            screen_er_dict_p2['message'] = "В бд внесены нарушения скринкаста"
            work_line = line.split()
            if len(work_line) > 3:
                screen_er_dict_p2['date'] = ' '.join(work_line[0:3])
                screen_er_dict_p2['token'] = work_line[-1]
                stat = 1

        if re.findall(check_2, line) != []:
            screen_er_dict_p2['Тип важности'] = "error"
            screen_er_dict_p2['message'] = "В бд не внесены нарушения скринкаста"
            work_line = line.split()
            if len(work_line) > 3:
                screen_er_dict_p2['date'] = ' '.join(work_line[0:3])
                screen_er_dict_p2['token'] = work_line[-1]
                stat = 1

        if stat == 1:
            if line == '}' or line == '},' or line == '},\x01,':
                stat = 0
                screen_er_dict_p2['log'] = byf
                byf = []
                if screen_er_dict_p2 not in screen_er_p2:
                    screen_er_p2.append(screen_er_dict_p2.copy())
            else:
                byf.append(line)

    return screen_er_p2  

def connection(res):
    form_dict = {"Тип важности": "info", "message": "Соединение установлено",
                 "file": "/backend/utils/kurento.js", "token": "", "log": "", "date": ""}
    check = 'connection was created'
    con_list = []
    for line in res:
        if re.findall(check, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = re.findall(r'\w{24}', line)[0]
            if form_dict not in con_list:
                con_list.append(form_dict.copy())
    return con_list

def video_sending_try(res):
    form_dict = {"Тип важности": "", "message": "",
                 "file": "/backend/utils/xqueue.js", "token": "", "log": "", "date": ""}
    check_1 = 'backend/utils/xqueue try to send token'
    check_2 = 'backend/utils/xqueue error while trying to send data to xqueue'
    check_3 = 'Success to post sendDateWebToXqueue in db'
    check_4 = 'backend/utils/xqueue can\'t find value by token'
    video_try = []
    for line in res:
        if re.findall(check_1, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = re.findall(r'\w{24}', line)[0]
                form_dict['Тип важности'] = "info"
                form_dict['message'] = 'Попытка отправки видео в xqueue'
            if form_dict not in video_try:
                video_try.append(form_dict.copy())

        if re.findall(check_2, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = re.findall(r'\w{24}', line)[0]
                form_dict['Тип важности'] = "error"
                form_dict['message'] = 'Ошибка отправки видео в xqueue'
            if form_dict not in video_try:
                video_try.append(form_dict.copy())

        if re.findall(check_3, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = "none"
                form_dict['Тип важности'] = "info"
                form_dict['message'] = 'Успешно отправлено видео в xqueue'
            if form_dict not in video_try:
                video_try.append(form_dict.copy())

        if re.findall(check_4, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = re.findall(r'\w{24}', line)[0]
                form_dict['Тип важности'] = "error"
                form_dict['message'] = 'Ошибка поиска видео по токену перед отправкой в xqueue'
            if form_dict not in video_try:
                video_try.append(form_dict.copy())

    return video_try  

def backend_conection(res):
    form_dict = {"Тип важности": "info", "message": "Установка соединения на бекенде",
                 "file": "/backend/utils/kurento.js", "token": "", "log": "", "date": ""}
    check_1 = 'Backend utils/kurento: RECEIVE_VIDEO_FROM'
    check_2 = 'Backend utils/kurento: CANDIDATE'
    con_list = []
    for line in res:
        if re.findall(check_1, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = re.findall(r'\w{24}', line)[0]
            if form_dict not in con_list:
                con_list.append(form_dict.copy())

        if re.findall(check_2, line) != []:
            work_line = line.replace(']', '').replace('[', '').split()
            if len(work_line) > 3:
                form_dict['log'] = line
                form_dict['date'] = ' '.join(work_line[0:3])
                form_dict['token'] = re.findall(r'\w{24}', line)[0]
            if form_dict not in con_list:
                con_list.append(form_dict.copy())
    return con_list  
  
if __name__ == '__main__':
    
    # Nikita
    res = take_log_from_file(file_name)
    '''
    resultus = backend_conection(res)
    pprint.pprint(resultus)
    
    
    resultus = video_sending_try(res)
    pprint.pprint(resultus)
    
    resultus = connection(res)
    pprint.pprint(resultus)
  
    
    resultus = screencast_error_status(res)
    pprint.pprint(resultus)
    resultus = screencast_error_part_2(res)
    pprint.pprint(resultus)
    
    resultus = webcam_error_status(res)
    pprint.pprint(resultus)
    
    resultus = webcam_error_part_2(res)
    pprint.pprint(resultus)
    
    resultus = video_upload_error(res)
    pprint.pprint(resultus)
    
    resultus = admins(res)
    pprint.pprint(resultus)
    
    resultus = user_del(res)
    pprint.pprint(resultus)
    
    resultus = user_add(res)
    pprint.pprint(resultus)
    
    resultus = video_record(res)
    pprint.pprint(resultus)
    
    resultus = stud_tab(res)
    pprint.pprint(resultus)
    
    check_docker(res, list_ch)
    stud_online(res)
    no_db_error(res)
    print('\n')
    br_info = browser_info(res)
    if br_info != []:
        pprint.pprint(br_info)
    else:
        print('no br info')
    print('\n')
    host = host_info(res)
    if host != []:
        pprint.pprint(host)
    else:
        print('no mes about host')
    print('\n')
    m_er = markup_error(res)
    if m_er != []:
        pprint.pprint(m_er)
    else:
        print('no markup error')
    print('\n')
    db_connection = db_message(res)
    if db_connection != []:
        pprint.pprint(db_connection)
    else:
        print('no db connection error')
    print('\n')
    rec = record(res, wts_1)
    if rec != []:
        pprint.pprint(rec)
    else:
        print('no info about start recording')
    print('\n')
    rec = record(res, wts_2)
    if rec != []:
        pprint.pprint(rec)
    else:
        print('no info about end recording')
    print('\n')
    check_1 = check_some(res, wtc_1, mes_1)  # end by cross
    if check_1 != []:
        pprint.pprint(check_1)
    else:
        print('no cross')
    print('\n')
    check_2 = check_some(res, wtc_2, mes_2)  # not chrome error
    if check_2 != []:
        pprint.pprint(check_2)
    else:
        print('no not chrome browser error')
    print('\n')
    vil = violation(res)
    if vil != []:
        pprint.pprint(vil)
    else:
        print('no violation at this session')
    print('\n')
    vl_list = violation_pars_list(res, list_to_pars_violations)
    if vl_list != []:
        pprint.pprint(vl_list)
    else:
        print('no violations to pars')
    print('\n')
    '''
    
    #ultimate func
    '''
    #run ultimate func
    log = take_log_from_file(file_name)
    # test of info with one string
    print('test 1')
    line = list_of_lines_info[0]
    resus = ultimate_to_find(log, line, 0, 0, ['},', '},\x01,'])
    pprint.pprint(resus)
    # test of info with some strings
    print('\n\ntest 2')
    line = list_of_lines_info[1]
    resus = ultimate_to_find(log, line, 0, 1, ['},', '},\x01,'])
    pprint.pprint(resus)
    # error test
    print('\n\ntest 3')
    line = list_of_lines_errors[1]
    resus = ultimate_to_find(log, line, 0, 0, ['},', '},\x01,'])
    pprint.pprint(resus)
    '''
