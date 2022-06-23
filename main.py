# coding=utf-8

from bottle import route, run, template, request, static_file, redirect
from controller.search_controller import server_static, index
import hanlp
if __name__ == '__main__':

    run(host='localhost', port=8080)
