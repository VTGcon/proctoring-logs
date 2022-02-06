from Nikita import  *
from Evgeny import *
from VS import *
from Victor import *

import string
import pandas as pd
import pprint
import requests
import json
from github import Github
import base64
import re


#func options, need for work
pprint.sorted = lambda x, key=None: x
token = 'AK4ZZFW3CNMEEED45ZR3IJDBMRUCI'
token_to_find = '609ccc0239a8b82be11b5229'

#file name
file_name = 'consoleText 2021 11 03'

if __name__ == '__main__':
    '''
    Here u need to do same as in instruction
    '''
    #func options
    log = take_log_from_file(file_name)

    #find some and print
    host = host_info(log)
    pprint.pprint(host)
    print('\n')

    resultus = webcam_error_status(log)
    pprint.pprint(resultus)
    print('\n')

    resultus = webcam_error_part_2(log)
    pprint.pprint(resultus)
    print('\n')

    resultus = user_doesnt_want_to_continue(log)
    pprint.pprint(resultus)
    print('\n')

    resultus = take_ok_sending_screencast(log)
    pprint.pprint(resultus)
    print('\n')

    resultus = backend_stop_session(log)
    pprint.pprint(resultus)
    print('\n')
