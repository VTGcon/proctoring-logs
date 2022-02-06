import json
import re
from pprint import pprint

moc_data = [["критический", "все упало", "app.py", "113", "02.04/1997"],
            ["token 12345", "предупреждение", "стиль не тот", "style.css", "115", "03.03.1998"],
            ["внимание", "подходит конец дедлайна", "project.py", "118", "08.04.2001"]]

DEVICE_ERROR = "The user wants to continue without a microphone or webcam"
TIMEOUT_SETUP_1 = "Client showError: Долгое создание соединения"
TIMEOUT_SETUP_2 = "Установлен таймаут"
WEBCAM_ERROR = "webcam kurentoUtils.WebRtcPeer.WebRtcPeerSendonly error"
BEGIN_RECORD = "Пользовать нажал начать запись"
READY_TO_RECORD = "Пользовать уверен, что хочет начать запись"

json_kind = {
    "token": "",
    "Тип важности": "",
    "messege": "",
    "file": "",
    "log": "",
    "date": ""}


def take_log_from_file(file_name):
    file = open('examples/' + file_name + '.txt', 'r', encoding="utf-8").read()
    lines = file.split('\n')
    return lines


def make_json(data):
    result_json = []
    for record in data:
        record_to_json = json_kind.copy()
        index = 0
        for key, _ in record_to_json.items():
            if len(record) == 5:
                if index != 0:
                    record_to_json[key] = record[index - 1]
            else:
                record_to_json[key] = record[index]
            index += 1
        result_json.append(record_to_json)
    return result_json


def write_json_to_file(json_object, name):
    with open(name + ".json", 'w') as file:
        json.dump(json_object, file, indent=2, ensure_ascii=False)


def func(data, TIMEOUT_SETUP, file_name):
    tokens = {}
    token_len = 26
    for record in data:
        if re.match(r"\[[[0-9]|[a-z]]{24}]", record) is not None:
            token_name = record[0:token_len]
            message = record[token_len:]
            if not tokens.get(token_name, []):
                tokens[token_name] = [message]
            else:
                tokens[token_name].append(message)

    timeout_token_example = ["error", "Long connection", file_name, "", "", ""]
    timeout_tokens = []

    for token, messages in tokens.items():
        cur_token = timeout_token_example.copy()
        set_up_timeout = 0
        log = ""
        times_of_error1 = []
        times_of_error2 = []
        date = ""
        check = False
        storage = []
        begin_record_check = False
        ready_record_check = False
        full_token = ""
        for mes in messages:
            if TIMEOUT_SETUP in mes:
                check = True
                full_token = token + mes[mes.find(TIMEOUT_SETUP):]
                date = mes[mes.find(TIMEOUT_SETUP) + len(TIMEOUT_SETUP) + 1:]
                set_up_timeout += 1
                begin_record_check = any([(BEGIN_RECORD in _) for _ in storage])
                ready_record_check = any([(READY_TO_RECORD in _) for _ in storage])
                storage = []
            if DEVICE_ERROR in mes:
                times_of_error1.append(mes[mes.find(DEVICE_ERROR) + len(DEVICE_ERROR) + 1:])
            if WEBCAM_ERROR in mes:
                times_of_error2.append(mes[mes.find(WEBCAM_ERROR) + len(WEBCAM_ERROR) + 1:])
            storage.append(mes)
        if check:
            if set_up_timeout == 1:
                log += "Сюда надо записать какие-то данные "
            else:
                log += "Number of show error = " + str(set_up_timeout)
            log += "\n"

            if begin_record_check:
                log += BEGIN_RECORD
                log += "\n"

            if ready_record_check:
                log += READY_TO_RECORD
                log += "\n"

            if len(times_of_error1) > 0:
                log += DEVICE_ERROR + " happens at time:"
                log += "\n"
                for time in times_of_error1:
                    log += time + ";\n"

            if len(times_of_error2) > 0:
                log += WEBCAM_ERROR + " happens at time:"
                log += "\n"
                for time in times_of_error2:
                    log += time + ";\n"
            cur_token[3] = full_token
            cur_token[4] = log
            cur_token[5] = date
            timeout_tokens.append(cur_token)

    return timeout_tokens


def check_ref_on_photo(records: list[str]):
    tokens = []
    template_token = ["info", "Проверка ссылки на фото", " /backend/routes/photoLinkChecker.js", "", ""]
    res = None
    result_str = None
    err = None
    log_message = ""
    was_space_sym = False
    image_urls = []
    for record in records:
        if record.startswith("image url:"):
            image_urls.append(record[len("image url "):])

        if record.startswith("res: "):
            res = True

        if res and record.startswith("result_str "):
            result_str = True

        if result_str and res and record.startswith("err: "):
            err = True

        if record.strip() == "":
            was_space_sym = True

        if err:
            log_message += record

        if err and was_space_sym:
            if record.startswith("err: "):
                was_space_sym = False
            else:
                res = None
                result_str = None
                err = None
                record_token = template_token.copy()
                record_token[2] = log_message
                tokens.append(record_token)
                log_message = ""
                was_space_sym = False

    return tokens


def parse_error_on_video(records: list[str]):
    tokens = []
    template_token = ["", "info", "Вызов метода для парсинга нарушений на видео", "/backend/routes"
                                                                                  "/videoMarkupPictures.js", "", ""]
    date = None
    parseVideoWithMarkup = False
    for record in records:
        if parseVideoWithMarkup:
            token_pos = record.find("token:")
            markup_pos = record.find("markup:")
            token = record
            parseVideoWithMarkup = False

        if "parseVideoWithMarkup info" in record:
            data_end = record.find("]")
            date = record[1:data_end]
            las_part = record[data_end + 1 + len("parseVideoWithMarkup info") + 1:]
            parseVideoWithMarkup = True


def no_media_server_at_address(records: list[str]):
    # нет примера, не понятно какие сообщения брать в виде логов + где искать сам токен
    tokens = []
    template_token = ["", "error", "Нет медиасервера", " /backend/utils/kurento.js", "", ""]

    for record in records:
        if "Could not find media server at address" in record:
            cur_token = template_token.copy()
            template_token[5] = record[1:record.find("]")]
            tokens.append(cur_token)
    return tokens


def connection_start_and_end(records: list[str]):
    tokens = []
    template_token = ["", "info", "Начало и конец соединения", " /backend/utils/kurento.js", "", ""]
    cur_token = None
    cur_date = None
    cur_log = ""
    write_in_log = False
    is_first_line = False
    for record in records:
        if "start mediapipeline" in record:
            cur_token = record[1:record.find("]")]
            cur_date = record[record.find("=") + 1:]
            write_in_log = True
            is_first_line = True

        if "finish mediapipeline" in record:
            upd_token = template_token.copy()
            upd_token[0] = cur_token
            upd_token[4] = cur_log
            upd_token[5] = cur_date
            cur_token = None
            cur_date = None
            cur_log = ""
            write_in_log = False
            tokens.append(upd_token)

        if write_in_log and not is_first_line:
            cur_log += record[record.find("[") + 1:]
        is_first_line = False
    return tokens


def backend_stop_session(records: list[str]):
    tokens = []
    template_token = ["", "info", "Остановка соединения", " /backend/utils/kurento.js", "", ""]
    cur_date = None

    prev_record = None
    for record in records:
        if re.match(r"\[[a-zA-Z0-9]+] \(frontend\) type=webcam start webrtc.*", record):
            cur_date = record[record.find("webrtc") + 7:]
        if "Backend stopSession" in record:
            upd_token = template_token.copy()
            cur_token = prev_record[1:prev_record.find("]")]
            cur_log = record[len("Backend stopSession") + 1:]
            upd_token[0] = cur_token
            upd_token[4] = cur_log
            upd_token[5] = cur_date
            tokens.append(upd_token)

        prev_record = record
    return tokens


def student_name_error(records: list[str]):
    tokens = []
    template_token = ["", "error", "Ошибка в имени студента", " /backend/utils/kurento.js", "", ""]
    session_start = False
    log = ""
    date = None
    session_end = True
    log_start = False
    previous_bracket_closed = False
    for record in records:
        if "session {" in record:
            session_start = True
            session_end = False

        if session_start:
            if "startTime" in record:
                date = record[record.find("startTime:") + 10:-1]
            if record.startswith("}"):
                session_end = True
                session_start = False

        if log_start:
            if previous_bracket_closed:
                if not record.startswith("["):
                    tpd_token = template_token.copy()
                    tpd_token[5] = date
                    tpd_token[4] = log
                    tokens.append(tpd_token)
                    session_start = False
                    log = ""
                    date = None
                    session_end = True
                    log_start = False
                    previous_bracket_closed = False
                else:
                    previous_bracket_closed = False

            if record.startswith("]"):
                previous_bracket_closed = True
            log += record

        if "Student name can't consist of empty spaces" in record:
            log_start = True
    return tokens

