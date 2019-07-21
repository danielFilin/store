
from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
import ast


mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="filin",
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


@get("/test")
def test():
    return json.dumps({"name" : "yoav"})


@post("/test")
def post_test():
    return json.dumps({"name" : request.forms.get("name")})


@post('/category')
def add_category():
    new_cat = request.POST.get('name')
    if new_cat:
        cat_list = get_my_categories()
        new_category = list(cat_list)
        my_cat = "".join(new_category)
        json_acceptable_string = my_cat.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        myobj = d['CATEGORIES']
        counter = 0
        for category in myobj:
            #print(new_cat in category['name'])
            if new_cat in category['name']:
                STATUS = "ERROR"
                MSG = "200 - Category already exists"
                counter = -1
                #print(new_cat, category['name'])
        if counter == 0:
            print(counter)
            insert_new_category(new_cat)
        else:
            return None
    else:
        STATUS = "ERROR"
        MSG = "Bad request! 400"
    result = {"STATUS":"Error", "MSG":"fsa"}
    return json.dumps(result)


def insert_new_category(category):
    print(category)
    try:
        with mydb.cursor() as cursor:
            sql = "INSERT INTO categories (name, id) VALUES('{}',null)".format(category)
            cursor.execute(sql)
            STATUS = "SUCCESS"
            mydb.commit()
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


@delete("/category/<id>")
def remove_category(id):
    print('entering delete')
    try:
        with mydb.cursor() as cursor:
            sql = "DELETE FROM CATEGORIES WHERE id={}".format(id)
            cursor.execute(sql)
            status = "The category was deleted successfully"
            mydb.commit()
            msg = ""
    except Exception as e:
        status = "The category was not deleted due to an error"
        msg = "500 - Internal Error"
    return json.dumps({"STATUS": status, "MSG": msg})


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
