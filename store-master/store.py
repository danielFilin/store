
from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql



mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="filin",
    database="store",
    cursorclass=pymysql.cursors.DictCursor
)

# first need to create a DB called store. Afterwards populate it with a few values. 

mycursor = mydb.cursor()

#create a store DB.
# mycursor.execute("CREATE TABLE categories (name VARCHAR(255),  my_id int(10) AUTO_INCREMENT)")

# setsql = "INSERT INTO categories (name, my_id) VALUES (%s, %s)"

# categoreies = [("Food", 1),
#                 ("machinery", 2),
#                 ("toys", 3)]

# mycursor.executemany(setsql, categoreies)

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
        print(len(cat_list))
        for category in cat_list:
             if category == new_cat:
                STATUS = "ERROR"
                MSG = "200 - Category already exists"
                add_category(new_cat)
    else:
        STATUS = "ERROR"
        MSG = "Bad request! 400"
    result = {"STATUS":"gdd", "MSG":"fsa"}
    return json.dumps(result)


def add_category(categ):
    try:
        with mydb.cursor() as cursor:
            sql = "INSERT INTO categories(name) VALUES ('{categ}')"
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
    myList = []
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT name FROM categories"
            cursor.execute(sql)
            mycategories = cursor.fetchall()
            for dic in mycategories:
                for key in dic:
                    print(dic[key] != "")
                    if dic[key] != "":
                        myList.append(dic[key])
    except Exception as e:    
        MSG = "500 - Internal Error"
    
    # result = {mycategories}
    # return json.dumps(result)
    return myList

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
