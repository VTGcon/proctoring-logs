import nltk
import string


def token_matches_init(logs):
    auth_token_dict_ = {}
    for i in logs:
        if i.find('STAT') != -1:
            auth_token = i[17:41]
            if auth_token in auth_token_dict_:
                auth_token_dict_[auth_token].append(i)
            else:
                auth_token_dict_[auth_token] = [i]
    return auth_token_dict_


def auth_token_matches(auth_token_dict_, auth_token):
    return "".join(i + "\n" for i in auth_token_dict_[auth_token]) if auth_token in auth_token_dict_ else 'No matches'


def tokenize_logs(log):
    tokens = []
    punctuation_list = [i for i in string.punctuation]
    punctuation_list.append('..')
    punctuation_list.append('``')
    punctuation_list.append("''")
    for i in log:
        tokens.append([j for j in nltk.tokenize.word_tokenize(i) if j not in punctuation_list])
    return tokens


#info
def user_wants_to_continue(log):
    info = []
    for line in log:
        if re.match(r"The user wants to continue without a microphone or webcam", line):
            tmp1 = re.match(r'\[.*]', line).group(0)
            tmp2 = re.match(r'\.=.*', line).group(0)
            info.append({'Тип важности': "info",
                         "message": "У пользователя отсутствует веб-камера или микрофон",
                         'file': "/frontend/src/libs/kurento-dev.js", 'token': tmp1[1:len(tmp1)], 'log': line,
                         'date': tmp2[1:len(tmp2)]})
    return info

#info
def user_doesnt_want_to_continue(log):
    info = []
    for line in log:
        if re.match(r"User doesn't want to continue without microphone or webcam", line):
            tmp1 = re.match(r'\[.*]', line).group(0)
            tmp2 = re.match(r'\.=.*', line).group(0)
            info.append({'Тип важности': "info",
                         'message': "У пользователя была проблема с отсутствием веб-камеры или микрофона",
                         'file': "/frontend/src/libs/kurento-dev.js", 'token': tmp1[1:len(tmp1)], 'log': line,
                         'date': tmp2[1:len(tmp2)]})
    return info

#error
def failed_webcam(log):
    fail_list = []
    for line in log:
        if re.match(r"\[.*] FAILED WEBCAM", line):
            tmp = re.match(r"\[.*]", line).group(0)
            fail_list.append(
                {"Тип важности": "error", "message": "Ошибка веб-камеры", "file": "/frontend/src/libs/kurento-dev.js",
                 "token": tmp[1: len(tmp) - 1], "log": line, "date": "todo"
                 })
    return fail_list

#info
def creating_session(log):
    result = []
    for line in log:
        if re.findall(".*] Creating Session:.*", line):
            tmp1 = re.search(r'n:.*,$', line).group(0)
            tmp2 = re.search(r'\[.*@', line).group(0)
            result.append({"Тип важности:": "info", "message": "Creating Session",
                           "file": "/backend/routes/service/createSession.js", "token": "TODO",
                           "log": tmp1[2:len(tmp1) - 1],
                           "date": tmp2[1:len(tmp2) - 1]
                           })
    return result
