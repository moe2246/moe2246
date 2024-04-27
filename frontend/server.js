// load the things we need
var express = require('express');
var app = express();
var axios = require("axios")
const bodyParser = require('body-parser');
app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true }));

// set the view engine to ejs
app.set('view engine', 'ejs');

// use res.render to load up the login page
app.get('/', function(req,res){
    res.render("pages/index.ejs");
})

// Route for Login
app.post('/process_login', function(req, res){
    var username = req.body.username;
    var password = req.body.password;
    
    axios.post('http://127.0.0.1:5000/api/login',{
            username: username,
            password: password  
                    
    })
    if(username === 'Admin' && password === 'CIS3368SPRING2024')
    {
        res.render('pages/welcome', {
            user: username,
            auth: true
             
        });
    }
    else
    {
        res.render('pages/welcome' ,{
            user: "UNAUTHORIZED",
            auth: false
        });
    }

});



// FACILITY ROUTES -----------------------

app.get('/facility', function(req, res) {

    //Facility List API Call
    axios.get('http://127.0.0.1:5000/api/facility').then((response)=>{
        var facilities = response.data;
        console.log(facilities);
        res.render('pages/facility', {
            facilities: facilities
        });
    });
    
});

// Route for creating a facility
app.post('/create_facility', (req, res) => {
    const facilityName = req.body.facilityName;
    axios.post('http://127.0.0.1:5000/api/facility', {
        name: facilityName
    })
    .then(response => {
        // Render the form again with a success message
        res.render('pages/message', { message: 'Facility added successfully' });
    })
    .catch(error => {
        // Render the form again with an error message
        console.error('Error adding facility:', error);
        res.render('pages/message', { message: 'Failed to add facility' });
    });
});

// Route for updating a facility
app.post('/update_facility', (req, res) => {
    const facilityId = req.body.facilityId;
    const newFacilityName = req.body.newFacilityName;

    axios.put(`http://127.0.0.1:5000/api/facility`, {
        name: newFacilityName,
        id: facilityId
    })
    .then(response => {
        res.render('pages/message', { message: 'Facility updated successfully' });
    })
    .catch(error => {
        console.error('Error updating facility:', error);
        res.render('pages/message', { message: 'Failed to update facility' });
    });
});



// Route for deleting a facility
app.post('/delete_facility', (req, res) => {
    const facilityId = req.body.facilityId;

    axios.delete(`http://127.0.0.1:5000/api/facility`, {
        headers: {                                      // header parameters sourced from https://blog.logrocket.com/using-axios-set-request-headers/
            'Content-Type': 'application/json'   
        },
        data: {
            id: facilityId  
        }
    })
    .then(response => {
        res.render('pages/message', { message: 'Facility deleted successfully' });
    })
    .catch(error => {
        console.error('Error deleting facility:', error);
        res.render('pages/message', { message: 'Failed to delete facility' });
    });
});


// CLASSROOM ROUTES ---------------


// Route for listing all available classrooms    
app.get('/classroom', (req, res) => {
    axios.get('http://127.0.0.1:5000/api/facility').then((facilities)=>{
        var facilities = facilities.data; 
        console.log(facilities);
        axios.get('http://127.0.0.1:5000/api/classroom').then((classrooms)=>{
            var classrooms = classrooms.data;
            console.log(facilities);
            console.log(classrooms);
        res.render('pages/classroom', {
            classrooms: classrooms,
            facilities: facilities
        });
    });
});
});



// Route for creating a new classroom
app.post('/create_classroom', (req, res) => {
    const classroomName = req.body.classroomName;
    const classroomCapacity = req.body.classroomCapacity;
    const facilityId = req.body.facilityId;

    axios.post('http://127.0.0.1:5000/api/classroom', {
        name: classroomName,
        capacity: classroomCapacity,
        facility: facilityId
    })
    .then(response => {
        // Render the form again with a success message
        res.render('pages/message', { message: 'Classroom added successfully' });
    })
    .catch(error => {
        // Render the form again with an error message
        console.error('Error adding facility:', error);
        res.render('pages/message', { message: 'Failed to add classroom. Not enough teachers or class is full.' });
    });
});

// Route for updating a classroom
app.post('/update_classroom', (req, res) => {
    const facilityId = req.body.facilityId;
    const newClassroomName = req.body.newClassroomName;
    const newCapacity = req.body.newCapacity;
    const classroomId = req.body.classroomId;

    axios.put(`http://127.0.0.1:5000/api/classroom`, {
        name: newClassroomName,
        facility: facilityId,
        capacity: newCapacity,
        id: classroomId
    })
    .then(response => {
        res.render('pages/message', { message: 'Classroom updated successfully' });
    })
    .catch(error => {
        console.error('Error updating classroom:', error);
        res.render('pages/message', { message: 'Failed to update classroom' });
    });
});

// Route for deleting a classroom
app.post('/delete_classroom', (req, res) => {
    const classroomId = req.body.classroomId;

    axios.delete(`http://127.0.0.1:5000/api/classroom`, {
        headers: {                                     // header parameters sourced from https://blog.logrocket.com/using-axios-set-request-headers/           
            'Content-Type': 'application/json'
        },
        data: {
            id: classroomId  
        }
    })
    .then(response => {
        res.render('pages/message', { message: 'Classroom deleted successfully' });
    })
    .catch(error => {
        console.error('Error deleting classroom:', error);
        res.render('pages/message', { message: 'Failed to delete classroom' });
    });
});

// Teacher Routes ------------------------------

// Route for getting all available classrooms
app.get('/teacher', (req, res) => {
    axios.get('http://127.0.0.1:5000/api/teacher').then((teachers)=>{
        var teachers = teachers.data;
        console.log(teachers);
        axios.get('http://127.0.0.1:5000/api/classroom').then((classrooms)=>{
            var classrooms = classrooms.data;
            console.log(teachers);
            console.log(classrooms);
        res.render('pages/teacher', {
            classrooms: classrooms,
            teachers: teachers
        });
    });
});
});

// Route for creating a new Teacher
app.post('/create_teacher', (req, res) => {
    const teacherFirst = req.body.teacherFirst;
    const teacherLast = req.body.teacherLast;
    const classroomId = req.body.classroomId;

    axios.post('http://127.0.0.1:5000/api/teacher', {
        firstname: teacherFirst,
        lastname: teacherLast,
        room: classroomId
    })
    .then(response => {
        // Render the form again with a success message
        res.render('pages/message', { message: 'Teacher created successfully' });
    })
    .catch(error => {
        // Render the form again with an error message
        console.error('Error creating teacher:', error);
        res.render('pages/message', { message: 'Failed to create teacher. Reached max capacity of teachers or not enough students in classroom.' });
    });
});

// Route for updating a teacher
app.post('/update_teacher', (req, res) => {
    const newTeacherFirst = req.body.newTeacherFirst;
    const newTeacherLast = req.body.newTeacherLast;
    const classroomId = req.body.classroomId;
    const teacherId = req.body.teacherId;

    axios.put(`http://127.0.0.1:5000/api/teacher`, {
        firstname: newTeacherFirst,
        lastname: newTeacherLast,
        room: classroomId,
        id: teacherId
    })
    .then(response => {
        res.render('pages/message', { message: 'Teacher updated successfully' });
    })
    .catch(error => {
        console.error('Error updating teacher:', error);
        res.render('pages/message', { message: 'Failed to update teacher. Reached max capacity of teachers or not enough students in classroom.' });
    });
});

// Route for deleting a teacher
app.post('/delete_teacher', (req, res) => {
    const teacherId = req.body.teacherId;

    axios.delete(`http://127.0.0.1:5000/api/teacher`, {
        headers: {                                       // header parameters sourced from https://blog.logrocket.com/using-axios-set-request-headers/
            'Content-Type': 'application/json'
        },
        data: {
            id: teacherId  
        }
    })
    .then(response => {
        res.render('pages/message', { message: 'Teacher deleted successfully' });
    })
    .catch(error => {
        console.error('Error deleting deleting:', error);
        res.render('pages/message', { message: 'Failed to delete teacher' });
    });
});

// Child Routes ------------------------------------

// Route for lising out all available children
app.get('/child', (req, res) => {
    axios.get('http://127.0.0.1:5000/api/child').then((children)=>{
        var children = children.data;
        console.log(children);
        axios.get('http://127.0.0.1:5000/api/classroom').then((classrooms)=>{
            var classrooms = classrooms.data;
            console.log(children);
            console.log(classrooms);
        res.render('pages/child', {
            classrooms: classrooms,
            children: children
        });
    });
});
});

// Route for creating a new child
app.post('/create_child', (req, res) => {
    const childFirst = req.body.childFirst;
    const childLast = req.body.childLast;
    const childAge = req.body.childAge;
    const classroomId = req.body.classroomId;

    axios.post('http://127.0.0.1:5000/api/child', {
        
        firstname: childFirst,
        lastname: childLast,
        age: childAge,
        room: classroomId
    })
    .then(response => {
        // Render the form again with a success message
        res.render('pages/message', { message: 'Child created successfully' });
    })
    .catch(error => {
        // Render the form again with an error message
        console.error('Error creating child:', error);
        res.render('pages/message', { message: 'Failed to create child. Reached max capacity of classroom or not enough teachers.' });
    });
});

// Route for updating a child
app.post('/update_child', (req, res) => {
    const newChildFirst = req.body.newChildFirst;
    const newChildLast = req.body.newChildLast;
    const newChildAge = req.body.newChildAge;
    const classroomId = req.body.classroomId;
    const childId = req.body.childId;

    axios.put('http://127.0.0.1:5000/api/child', {
        
        firstname: newChildFirst,
        lastname: newChildLast,
        age: newChildAge,
        room: classroomId,
        id: childId
    })
    .then(response => {
        // Render the form again with a success message
        res.render('pages/message', { message: 'Child updated successfully' });
    })
    .catch(error => {
        // Render the form again with an error message
        console.error('Error updating child:', error);
        res.render('pages/message', { message: 'Failed to update child. Reached max capacity of classroom or not enough teachers.' });
    });
});

// Route for deleting a child
app.post('/delete_child', (req, res) => {
    const childId = req.body.childId;

    axios.delete(`http://127.0.0.1:5000/api/child`, {
        headers: {                                         // header parameters sourced from https://blog.logrocket.com/using-axios-set-request-headers/
            'Content-Type': 'application/json'
        },
        data: {
            id: childId  
        }
    })
    .then(response => {
        res.render('pages/message', { message: 'Child deleted successfully' });
    })
    .catch(error => {
        console.error('Error deleting child:', error);
        res.render('pages/message', { message: 'Failed to delete child' });
    });
});


const port = 8080;

app.listen(port, () => console.log('Application started on port 8080'));
