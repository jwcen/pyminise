from bottle import route, request, static_file, redirect, template
from service.search_service import search_fun


@route('/static/<filename>')
def server_static(filename):
    if filename == "jquery.min.js":
        return static_file("jquery.min.js", root='./data/front/js/')
    elif filename == "bootstrap.min.js":
        return static_file("bootstrap.js", root='./data/front/js/')
    elif filename == "bootstrap.min.css":
        return static_file("bootstrap.css", root='./data/front/css/')


@route('/')
def index():
    return redirect("/search")


@route('/search')
def index():
    form = request.GET.decode("utf-8")
    keyword = form.get("keyword", "")
    p = form.get("p", "")
    mask = form.get("mask", "")
    # related_flag = form.get("related", "")
    context = search_fun(keyword, mask,p)
    return template("./web/search-result.html", context)
