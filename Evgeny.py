from Nikita import take_log_from_file
import pprint

pprint.sorted = lambda x, key=None: x


trying_connect_video_none = {'Тип важности': 'info', 'message': 'Попытка установки соединения ',
                             'file': '/frontend/src/libs/kurento.js', 'token': '-', 'log': 'log text', 'date': '-'}
all_tried_connect_video = []

recording_in_db_none = {'Тип важности': 'info', 'message': 'База данных обновлена', 'file': '/backend/db/api.js',
                        'log': 'log text', 'date': '-'}
all_recording_in_db = []

opening_connect_video_none = {'Тип важности': 'info', 'message': 'Открытие соединения webrtc для ',
                              'file': '/frontend/src/libs/kurento.js', 'token': '-', 'log': 'log text', 'date': '-'}
all_opened_connect_video = []

changed_photo_none = {'Тип важности': 'info', 'message': 'Изменение фото пользователя',
                      'file': '/backend/routes/photo.js', 'token': '-', 'log': 'log text', 'date': '-'}
all_changed_photo = []

trying_delete_none = {'Тип важности':'info','message':'Удаление сессии','file':'/backend/routes/service/deleteSession.js','token':'-','log':'-','date':'-'}
deleting_error_none = {'Тип важности':'error','message':'Удаление сессии','file':'/backend/routes/service/deleteSession.js','token':'-','log':'-','date':'-'}
all_deleting_sessions = []

downloading_files_none = {'Тип важности':'info','message':'Скачивание файла','file':'/backend/utils/download.js','log':'log text','date':'-'}
all_downloaded_files = []

error_sending_video_none = {'Тип важности': 'error', 'message': 'Ошибка отправки видео',
                            'file': '/frontend/src/libs/kurento.js', 'token': '-', 'log': 'log text', 'date': '-'}
all_error_sending_video = []

posting_ml_none = {'Тип важности': 'info', 'message': 'Отправлен файл мл-сервису', 'file': '/backend/routes/files.js',
                   'log': 'log text', 'date': '-'}
all_posting_ml = []

registering_xqueue_none = {'Тип важности': 'info', 'message': 'Регистрация в xqueue',
                           'file': '/backend/routes/xqueue.js', 'token': '-', 'log': 'log text', 'date': '-'}
all_registered_xqueue = []

error_sending_token_toXqueue_none = {'Тип важности': 'error', 'message': 'Ошибка отправки токена в xqueue',
                                     'file': '/backend/routes/xqueue.js', 'token': '-', 'log': '-', 'date': '-'}
all_error_sent_token_toXqueue = []

error_sending_webcam_none = {'Тип важности': 'error', 'message': 'Ошибка отправки веб-камеры в xqueue',
                             'file': '/backend/utils/xqueue.js', 'token': '-', 'log': '-', 'date': '-'}
all_error_sent_webcam = []

sending_token_toXqueue_none = {'Тип важности': 'info', 'message': 'Отправка токена в xqueue',
                               'file': '/backend/routes/xqueue.js', 'token': '-', 'log': '-', 'date': '-'}
all_sent_token_toXqueue = []

error_sending_screencast_none = {'Тип важности': 'error', 'message': 'Ошибка отправки веб-камеры в xqueue',
                                 'file': '/backend/utils/xqueue.js', 'token': '-', 'log': '-', 'date': '-'}
all_error_send_screencast = []

ok_sending_webcam_none = {'Тип важности': 'info', 'message': 'Успешно отправлено видео с веб-камеры в xqueue',
                          'file': '/backend/utils/xqueue.js', 'token': '-', 'log': '-', 'date': '-'}
all_ok_sent_webcam = []

transcode_error_none = {'Тип важности': 'error', 'message': 'No db', 'file': '/backend/utils/kurento.js',
                        'token': 'token', 'log': 'log text', 'date': '-'}
all_transcode_error1 = []

post_list_students_none = {'Тип важности': 'info', 'message': 'Ссылки сгенерированы из файла',
                           'file': '/backend/routes/studentsList.js', 'log': 'log text', 'date': '-'}
all_post_list_students = []

ok_sending_screencast_none = {'Тип важности': 'info', 'message': 'Успешно отправлено видео скринкаста в xqueue',
                              'file': '/backend/utils/xqueue.js', 'token': '-', 'log': '-', 'date': '-'}
all_ok_sent_screencast = []

xqueue_message_none = {'Тип важности': 'info', 'message': 'Обновление данных в xqueue',
                       'file': '/backend/routes/forceUpdate.js', 'log': '-', 'date': '-'}
xqueue_error_none = {'Тип важности': 'error', 'message': 'Обновление данных в xqueue',
                     'file': '/backend/routes/forceUpdate.js', 'log': '-', 'date': '-'}
all_xqueue = []

def trying_connect_video(strings):
    for x in strings:
        if x.find('joinRoom=') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = trying_connect_video_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            if x.find('type=window') != -1:
                new_dict['message'] += 'скринкаста'
            elif x.find('type=webcam') != -1:
                new_dict['message'] += 'веб-камеры'
            all_tried_connect_video.append(new_dict)
    return all_tried_connect_video

def opening_connect_video(strings):
    for x in strings:
        if x.find('start webrtc=') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = opening_connect_video_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            if x.find('type=window') != -1:
                new_dict['message'] += 'скринкаста'
            elif x.find('type=webcam') != -1:
                new_dict['message'] += 'веб-камеры'
            all_opened_connect_video.append(new_dict)
    return all_opened_connect_video

def take_changing_photo(strings):
    for x in strings:
        if x.find('edit photo of user by post request.') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.find('Token:')
            exit_token = x.find('Value:')
            new_dict = changed_photo_none.copy()
            new_dict['token'] = x[enter_token + 6:exit_token].strip()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_changed_photo.append(new_dict)
    return all_changed_photo

def take_deleting_sessions(strings):
	token = 'oghhjguiyyighgughguyuvhguvhiguhvb'
	for x in strings:
		if x.find('try to delete') != -1:
			enter_date = x.find('[')
			exit_date = x.find(']')
			enter_token = x.find('files/')
			new_dict = trying_delete_none.copy()
			new_dict['date'] = x[enter_date+1:exit_date]
			token = x[enter_token+6:]
			new_dict['token'] = token
			new_dict['log'] = x
			all_deleting_sessions.append(new_dict)
		if x.find('err:') != -1 and x.find(token) != -1:
			enter_date = x.find('[')
			exit_date = x.find(']')
			new_dict = deleting_error_none.copy()
			new_dict['date'] = x[enter_date+1:exit_date]
			new_dict['token'] = token
			new_dict['log'] = x
			all_deleting_sessions.append(new_dict)
	return all_deleting_sessions

def take_downloading_files(strings, cond, cond2):
    for x in strings:
        if x.find(cond) != -1 and x.find(
                cond2) != -1:  # поставил второй аргумент для строк: end + url + - + path, чтобы одновременно считывать и end и -
            enter_date = x.find('[')
            exit_date = x.find(']')
            new_dict = downloading_files_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_downloaded_files.append(new_dict)
    return all_downloaded_files

def error_sending_video(strings):
    for x in strings:
        if x.find('kurentoUtils.WebRtcPeer.WebRtcPeerSendonly after err') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = error_sending_video_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            all_error_sending_video.append(new_dict)
    return all_error_sending_video

def take_post_file_ml(strings):
    for x in strings:
        if x.find('post file to ML:') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            new_dict = posting_ml_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_posting_ml.append(new_dict)
    return all_posting_ml

def registered_xqueue(strings):
    for x in strings:
        if x.find('login to xqueue with token') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.find('token:')
            exit_token = x.find(',')
            new_dict = registering_xqueue_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 6:exit_token].strip()
            new_dict['log'] = x
            all_registered_xqueue.append(new_dict)
    return all_registered_xqueue

def sending_token_to_xqueue(strings):
    for x in strings:
        if x.find('send token:') != -1 and x.find('to xqueue') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.find('token:')
            exit_token = x.find('to xqueue')
            new_dict = sending_token_toXqueue_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 6:exit_token].strip()
            new_dict['log'] = x
            all_sent_token_toXqueue.append(new_dict)
    return all_sent_token_toXqueue

def error_sending_token_to_xqueue(strings):
    for x in strings:
        if x.find('xqueue error') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.find('token:')
            exit_token = x.find('to xqueue')
            new_dict = error_sending_token_toXqueue_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[
                                enter_token + 6:exit_token].strip()  # получаю токен так, посколкьку  в задаче сказано, что token выше, но что значит это выше? поэтому сделал по аналогии
            new_dict['log'] = x
            all_error_sent_token_toXqueue.append(new_dict)
    return all_error_sent_token_toXqueue

def take_error_sending_webcam(strings):
    for x in strings:
        if x.find('sendDateWebToXqueue error') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = error_sending_webcam_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            all_error_sent_webcam.append(new_dict)
    return all_error_sent_webcam

def take_error_sending_screencast(strings):
    for x in strings:
        if x.find('sendDateScreenToXqueue error') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = error_sending_screencast_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            all_error_send_screencast.append(new_dict)
    return all_error_send_screencast

def take_ok_sending_webcam(strings):
    for x in strings:
        if x.find('Send to xqueue webcam - ok') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = ok_sending_webcam_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            all_ok_sent_webcam.append(new_dict)
    return all_ok_sent_webcam

def take_ok_sending_screencast(strings):
    for x in strings:
        if x.find('Send to xqueue screencast - ok') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            enter_token = x.rfind('[')
            exit_token = x.rfind(']')
            new_dict = ok_sending_screencast_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['token'] = x[enter_token + 1:exit_token]
            new_dict['log'] = x
            all_ok_sent_screencast.append(new_dict)
    return all_ok_sent_screencast

def take_ffmpeg_transcode_error(res):
    q = len(res)
    log_text = []
    for x in range(q):
        if res[x].find('ffmpeg transcode Error') != -1:
            enter_date = res[x].find('[')
            exit_date = res[x].find(']')
            date = res[x][enter_date + 1:exit_date]
            enter = res[x].find('files/')
            enter = enter + 6
            exit = res[x].find('/window.webm')
            token = res[x][enter:exit]
            i = x
            while i != q:
                if (res[i].find('ffmpeg') != -1 and res[i].find(token) != -1) or (
                        res[i].find('mediainfo') != -1 and res[i].find('token') != -1):
                    log_text.append(res[i])
                i += 1
            transcode_error = transcode_error_none.copy()
            transcode_error['date'] = date
            transcode_error['token'] = token
            transcode_error['log'] = log_text
            all_transcode_error1.append(transcode_error)
            log_text = []
    return all_transcode_error1

def take_post_list_stud(strings):
    for x in strings:
        if x.find('post students list:') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            new_dict = post_list_students_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_post_list_students.append(new_dict)
    return all_post_list_students

def take_update_xqueue(strings):
    for x in strings:
        if x.find('FORCE SEND TOKEN TO XQUEUE') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            new_dict = xqueue_message_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_xqueue.append(new_dict)
        if x.find('Failed update all token for xqueue') != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            new_dict = xqueue_error_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_xqueue.append(new_dict)

    return all_xqueue

def recording_in_db(strings, cond):
    for x in strings:
        if x.find(cond) != -1:
            enter_date = x.find('[')
            exit_date = x.find(']')
            new_dict = recording_in_db_none.copy()
            new_dict['date'] = x[enter_date + 1:exit_date]
            new_dict['log'] = x
            all_recording_in_db.append(new_dict)
    return all_recording_in_db

