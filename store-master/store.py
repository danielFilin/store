
from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="l33tsup4h4x0r",
    database="store",
    cursorclass=pymysql.cursors.DictCursor
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE categories (name VARCHAR(255),  my_id int(10) AUTO_INCREMENT)")
# setsql = "INSERT INTO categories (name, my_id) VALUES (%s, %s)"
# categories = [("Food", 1),
#                 ("machinery", 2),
#                 ("toys", 3)]
# mycursor.executemany(setsql, categories)
# mydb.commit()


@get("/admin")
def admin_portal():
	return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post('/category')
def add_category():
    new_cat = request.POST.get('name')
    if new_cat:
        cat_list = get_my_categories()
        print(list(cat_list))
        # for category in cat_list():
        #     print(category)
        #     if category['name'] == new_cat:
        #         STATUS = "ERROR"
        #         MSG = "200 - Category already exists"
        insert_new_category(new_cat)
    else:
        STATUS = "ERROR"
        MSG = "Bad request! 400"
    result = {"STATUS":"gdd", "MSG":"fsa"}
    return json.dumps(result)


def insert_new_category(category):
    try:
        with mydb.cursor() as cursor:
            sql = "INSERT INTO categories(name)"
            cursor.execute(sql)
            mydb.commit()
            STATUS = "SUCCESS"
            MSG = "All went well"
    except Exception as e:
        STATUS = "error!"
        MSG = "Did not went well"
    result = {"STATUS":"good", "MSG":"good"}
    return result


@get('/categories')
def get_my_categories():
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT name FROM categories"
            cursor.execute(sql)
            CATEGORIES = cursor.fetchall()
            STATUS = "SUCCESS"
            MSG = "Item was added!"
    except Exception as e:
        STATUS = "ERROR"
        MSG = "500 - Internal Error"
    result = {"STATUS":STATUS, "CATEGORIES":CATEGORIES,"MSG":MSG}
    return json.dumps(result)


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=5000)
