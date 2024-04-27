import flask
from flask import jsonify
from flask import request
import creds
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
from sql import execute_read_row_query


# Setting up application name
app = flask.Flask(__name__) # Sets up the application
app.config["DEBUG"] = True # Allow to show errors in browser

# Created a connection to my mySQL Database
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

# LOGIN API ------------------------------------------------------
username = 'Admin'
password = 'CIS3368SPRING2024'


@app.route('/api/login', methods=['POST']) # Route to Login API http://127.0.0.1:5000/api/login
def login():
    request_data = request.get_json()
    user_name = request_data.get('username')
    pass_word = request_data.get('password')
    if username == user_name and password == pass_word:
        return jsonify({"message": "Login successful!"})
    else: 
        return jsonify({"Error": "Wrong login info!"})
    
# FACILITY TABLE OPERATIONS ------------------------------------------------------

# API to ADD new facility to database
@app.route('/api/facility', methods=["POST"]) # Route to add new facility to database http://127.0.0.1:5000/api/facility
def create_facility():
    request_data = request.get_json()
    new_facility_name = request_data['name']
    add_facility = 'INSERT INTO facility (name) VALUES ("%s")' % (new_facility_name)
    execute_query(conn, add_facility)
    return jsonify({"message": "Facility Added!"})

# API to SELECT and display all facilities from database
@app.route("/api/facility", methods=["GET"]) # Route to select facilities from database http://127.0.0.1:5000/api/facility
def get_facilities():
    display_facility = 'SELECT id, `name` FROM facility'
    facility = execute_read_query(conn, display_facility)
    return jsonify(facility)

# API to UPDATE the facility names from database
@app.route("/api/facility", methods=["PUT"]) # Route to add update facility in database http://127.0.0.1:5000/api/facility
def update_facility():
    request_data = request.get_json()
    facility_to_update = request_data["id"]
    updated_name = request_data["name"]
    update_query = """
UPDATE facility 
SET name = "%s"
WHERE id = %s """ % (updated_name, facility_to_update)
    execute_query(conn, update_query)
    return jsonify({"message": "Facility Updated!"})

# API to DELETE facility from database
@app.route("/api/facility", methods=["DELETE"]) # Route to delete facility from database http://127.0.0.1:5000/api/facility
def delete_facility():
    request_data = request.get_json()
    facility_to_remove = request_data["id"]
    delete_statement = 'DELETE FROM facility WHERE id = %s' % (facility_to_remove)
    execute_query(conn, delete_statement)
    return jsonify({"message": "Facility Deleted!"})
    
# CLASSROOM TABLE OPERATIONS ------------------------------------------------------

# API to SELECT and display all available classrooms from database
@app.route('/api/classroom', methods=["GET"]) # Route to select classrooms from database http://127.0.0.1:5000/api/classroom
def select_classrooms():
    select_classroom = 'SELECT id, capacity, name, facility FROM classroom'
    classroom = execute_read_query(conn, select_classroom)
    return jsonify(classroom) 


# API to ADD new classroom to database
@app.route('/api/classroom', methods=["POST"]) # Route to add new classroom to database http://127.0.0.1:5000/api/classroom
def create_classroom():
    request_data = request.get_json()
    classroom_capacity = request_data["capacity"]
    classroom_name = request_data["name"]
    facility_id = request_data["facility"]

    check_facility = 'SELECT name FROM facility WHERE id = %s' 
    facility_result = execute_read_row_query(conn, check_facility, (facility_id,))

    if not facility_result:
        return jsonify({"Error": "Facility does not Exist!"})

    create_query = 'INSERT INTO classroom (capacity, name, facility) VALUES (%s , "%s", %s)' % (classroom_capacity, classroom_name, facility_id)
    execute_query(conn, create_query)
    return jsonify({"message": "Classroom created!"})

# API to UPDATE Classroom
@app.route('/api/classroom', methods=['PUT']) # Route to update classroom in database http://127.0.0.1:5000/api/classroom
def update_classroom():
    request_data = request.get_json()
    update_capacity = request_data["capacity"]
    update_name = request_data["name"]
    update_facility = request_data["facility"]
    classroom_to_change = request_data["id"]
    update_query = """
UPDATE classroom
SET capacity = %s, name = "%s", facility = %s
WHERE id = %s """ % (update_capacity, update_name, update_facility, classroom_to_change)
    execute_query(conn, update_query)
    return jsonify({"message": "Classroom updated!"})

# API to DELETE Classroom
@app.route('/api/classroom', methods=['DELETE']) # Route to delete classroom in database http://127.0.0.1:5000/api/classroom
def delete_classroom():
    request_data = request.get_json()
    classroom_to_delete = request_data["id"]
    delete_statement = 'DELETE FROM classroom WHERE id = %s' % (classroom_to_delete)
    execute_query(conn, delete_statement)
    return jsonify({"message": "Classroom deleted!"})

# TEACHER TABLE OPERATIONS ------------------------------------------------------

# API to ADD teacher to table
@app.route('/api/teacher', methods=['POST']) # Route to add new teacher to database http://127.0.0.1:5000/api/teacher
def create_teacher():
    request_data = request.get_json()
    teacher_firstname = request_data['firstname']
    teacher_lastname = request_data['lastname']
    teacher_room = request_data['room']

    # Checks to see if the classroom exist in the database
    check_room = 'SELECT capacity FROM classroom WHERE id = %s' 
    room_result = execute_read_row_query(conn, check_room, (teacher_room,))

    if not room_result:
        return jsonify({"Error": "Room does not Exist!"})
    
    create_query = 'INSERT INTO teacher (firstname, lastname, room) VALUES ("%s", "%s", %s)' % (teacher_firstname, teacher_lastname, teacher_room)
    execute_query(conn, create_query)
    return jsonify({"message": "Teacher created!"})


# API to SELECT and display all teachers from database 
@app.route('/api/teacher', methods=['GET']) # Route to select teahcers from database http://127.0.0.1:5000/api/teacher
def get_teachers():
    select_teachers = 'SELECT id, firstname, lastname, room FROM teacher'
    teacher = execute_read_query(conn, select_teachers)
    return jsonify(teacher)

# API to UPDATE teacher in database
@app.route('/api/teacher', methods=['PUT']) # Route to update teacher in database http://127.0.0.1:5000/api/teacher
def change_teacher():
    request_data = request.get_json()
    update_teacher_first = request_data['firstname']
    update_teacher_last = request_data['lastname']
    update_teacher_room = request_data['room']
    update_teacher_id = request_data['id']

    # Checks to see if classroom exists in the database
    check_room = 'SELECT name FROM classroom WHERE id = %s' 
    room_result = execute_read_row_query(conn, check_room, (update_teacher_room,))
    if not room_result:
        return jsonify({"Error": "Room does not Exist!"})

    update_query = """
        UPDATE teacher
        SET firstname = "%s", lastname = "%s", room = %s
        WHERE id = %s """ % (update_teacher_first, update_teacher_last, update_teacher_room, update_teacher_id)
    execute_query(conn, update_query)
    return jsonify({"message": "Teacher updated!"})

# API to DELETE teacher from database
@app.route('/api/teacher', methods=['DELETE']) # Route to delete teahcer in database http://127.0.0.1:5000/api/teacher
def remove_teacher():
    request_data = request.get_json()
    teacher_to_delete = request_data["id"]
    delete_statement = 'DELETE FROM teacher WHERE id = %s' % (teacher_to_delete)
    execute_query(conn, delete_statement)
    return jsonify({"message": "Teacher deleted!"})


# CHILD TABLE OPERATIONS ------------------------------------------------------

# API to create child in child table
@app.route('/api/child', methods=['POST']) # Route to add new child to database http://127.0.0.1:5000/api/child 
def add_child():
    request_data = request.get_json()
    child_firstname = request_data['firstname']
    child_lastname = request_data['lastname']
    child_age = request_data['age']
    child_room = request_data['room']

    # Checks to see if the room exist in the database 
    check_room = 'SELECT capacity FROM classroom WHERE id = %s' 
    room_result = execute_read_row_query(conn, check_room, (child_room,))
    
    if not room_result:
        return jsonify({"Error": "Room does not Exist!"})
    
    # Collects the total number of teachers in a specific classroom
    check_teacher = 'SELECT COUNT(*) as TeacherTotal FROM teacher where room = %s' # Referenced used when creating the select count(*) statement https://www.geeksforgeeks.org/count-sql-table-column-using-python/
    teacher_result = execute_read_row_query(conn, check_teacher, (child_room,)) 
    teacher_count = teacher_result['TeacherTotal'] if teacher_result else 0
    
    # Collects the total number of children in a specific classroom
    check_child = 'SELECT COUNT(*) as ChildTotal FROM child WHERE room = %s' # Referenced used when creating the select count(*) statement https://www.geeksforgeeks.org/count-sql-table-column-using-python/
    child_result = execute_read_row_query(conn, check_child, (child_room,))
    child_count = child_result['ChildTotal'] if child_result else 0

    # Collects the total capacity of a specific classroom
    check_capacity = 'SELECT capacity FROM classroom WHERE id = %s'
    capacity_result = execute_read_row_query(conn, check_capacity, (child_room,))
    capacity_count = capacity_result['capacity'] if capacity_result else 0

    # This is the check that makes sure that more than 10 children cannot be assigned to a classroom if only one teacher is available as well as maximum capacity
    if child_count >= 10 * teacher_count:
       return jsonify({"Error": "Not enough teachers in classroom!"})
    elif child_count == capacity_count:
        return jsonify({"Error": "Classroom capacity exceeded!"})
    else:
        create_query = 'INSERT INTO child (firstname, lastname, age, room) VALUES ("%s", "%s", %s, %s)' % (child_firstname, child_lastname, child_age, child_room)
        execute_query(conn, create_query)
        return jsonify({"message": "Child Added!"})

# API to SELECT and display all children in the database
@app.route('/api/child', methods=['GET'])  # Route to select children from database http://127.0.0.1:5000/api/child
def get_child():
    select_child = 'SELECT id, firstname, lastname, age, room FROM child'
    child = execute_read_query(conn, select_child)
    return jsonify(child)

# API to UPDATE child in database
@app.route('/api/child', methods=['PUT']) # Route to update child in database http://127.0.0.1:5000/api/child
def update_child():
    request_data = request.get_json()
    update_child_first = request_data['firstname']
    update_child_last = request_data['lastname']
    update_child_age = request_data['age']
    update_child_room = request_data['room']
    update_child_id = request_data['id']

    # Checks to see if the room exist in the database 
    check_room = 'SELECT capacity FROM classroom WHERE id = %s' 
    room_result = execute_read_row_query(conn, check_room, (update_child_room,))
    if not room_result:
        return jsonify({"Error": "Room does not exist!"})
    
    # Collects the total number of teachers in a specific classroom
    check_teacher = 'SELECT COUNT(*) as TeacherTotal FROM teacher where room = %s' # Referenced used when creating the select count(*) statement https://www.geeksforgeeks.org/count-sql-table-column-using-python/
    teacher_result = execute_read_row_query(conn, check_teacher, (update_child_room,))
    teacher_count = teacher_result['TeacherTotal'] if teacher_result else 0
    
    # Collects the total number of children in a specific classroom
    check_child = 'SELECT COUNT(*) as ChildTotal FROM child WHERE room = %s' # Referenced used when creating the select count(*) statement https://www.geeksforgeeks.org/count-sql-table-column-using-python/
    child_result = execute_read_row_query(conn, check_child, (update_child_room,))
    child_count = child_result['ChildTotal'] if child_result else 0

    # Collects the total capacity of a specific classroom
    check_capacity = 'SELECT capacity FROM classroom WHERE id = %s'
    capacity_result = execute_read_row_query(conn, check_capacity, (update_child_room,))
    capacity_count = capacity_result['capacity'] if capacity_result else 0

    # This is the check that makes sure that more than 10 children cannot be assigned to a classroom if only one teacher is available
    if child_count >= 10 * teacher_count:
       return jsonify({"Error": "Not enough teachers in classroom! Please add another teacher."})
    elif child_count > capacity_count:
        return jsonify({"Error": "Classroom capacity exceeded!"})
    else:
        update_query = """
        UPDATE child
        SET firstname = "%s", lastname = "%s", age = %s, room = %s
        WHERE id = %s """ % (update_child_first, update_child_last, update_child_age, update_child_room, update_child_id)
        execute_query(conn, update_query)
        return jsonify({"message": "Child Updated!"})

# API to DELETE child from database
@app.route('/api/child', methods=['DELETE']) # Route to delete child in database http://127.0.0.1:5000/api/child
def delete_child():
    request_data = request.get_json()
    child_to_delete = request_data["id"]
    delete_statement = 'DELETE FROM child WHERE id = %s' % (child_to_delete)
    execute_query(conn, delete_statement)
    return jsonify({"message": "Child Deleted!"})

app.run()







    



    
    
    
    
   

     