var employeeIDList = [];


function init() {
    $('#add_employee').on('click', function() {
        var newEmployee = {
            name: $('#name').val(),
            group: $('#group').val()
        };
    
        $.ajax({
            type: 'POST',
            dataType: "json",
            url: '/employees',
            data: newEmployee,
            success: function(resp) {
                groupList();
            }
        });    
    });

    $('#add_user').on('click', function(){
        var newUser = {
            emp_id: $('#emp_id').val(),
            username: $('#username').val(),
            password: $('#password').val(),
            auth: $('#auth').val()
        };
        $.ajax({
            type: 'POST',
            dataType: "json",
            url: '/users',
            data: newUser,
            success: function(resp) {
                groupList();
            }
        }); 
     });
    

     for (var i = 0; i<5; i++) {
        let groupNr = i
        let groupParent = $('ul #group' + groupNr);
        $.ajax({
            url: "/group-employees/" + groupNr,
            dataType: "json",
            success: function (resp) {
                groupParent.empty();
                $.each(resp, function(j, emp) {
                    employeeIDList.push(emp.employee_id);
                    element = $("<li class='list-group-item py-3'></li>").html("<b>Name:</b> " + emp.name + "      <b>ID:</b> " + emp.employee_id);
                    editBtn = $("<button type='button' class='btn btn-dark btn-sm' id='edit" + emp.employee_id + "' style='float: right; height :50%;'>Edit</span></button>");
                    editBtn.on('click', function() {
                        var parent = $(this).parent();
                        parent.empty();
                        var textfield = $("<form class='form-inline'><div class='form-group'><label for='edit_name'>Employee name:</label></div></form>");
                        var theField = $("<input type='text' class='form-control' id='edit_name' placeholder='Enter new name' name='edit_name'>");
                        textfield.append(theField);
                        parent.append(textfield);
                        var editEmployee = $("<button type='button' class='btn btn-dark btn-sm' id='edit_btn'>Edit</button>");
                        editEmployee.on('click', function() {
                            var req = {
                                emp_id: emp.employee_id,
                                name: theField.val()
                                
                            }
                            $.ajax({
                                type: 'PUT',
                                dataType: "json",
                                url: '/employees/'+ emp.employee_id,
                                data: req,
                                success: function(resp) {
                                    groupList();
                                }
                            });
                        });
                        
                        parent.append(editEmployee);
                        groupList();
                    });
                          
                    
                    
                    element.append(" </br> <b>Username:</b> " + emp.username + "<b>Authority:</b>" + emp.access_level);
                    element.append(editBtn);
                    
                    deleteBtn = $("<button type='button' class='btn btn-danger btn-sm' style='float: right; height :50%;'>Delete</span></button>").attr('id', 'remove'+emp.employee_id);
                    deleteBtn.on('click', function(){
                        
                        var req = {
                            emp_id: emp.employee_id
                        }
                        $.ajax({
                            type: 'DELETE',
                            dataType: "json",
                            url: '/employees/'+emp.employee_id,
                            data: req,
                            success: function(resp) {
                                groupList();
                            }
                        });
                    });
                    element.append(deleteBtn);
                    groupParent.append(element);
                });           
            }
        });
    }    
}

// refreshing the page on every event
function groupList() {
    for (var i = 0; i<5; i++) {
        let groupNr = i
        let groupParent = $('ul #group' + groupNr);        

        $.ajax({
            url: "/group-employees/" + groupNr,
            dataType: "json",
            success: function (resp) {
                groupParent.empty();
                $.each(resp, function(j, emp) {
                    element = $("<li class='list-group-item py-3'></li>").html("<b>Name:</b> " + emp.name + "      <b>ID:</b> " + emp.employee_id);
                    editBtn = $("<button type='button' class='btn btn-dark btn-sm' id='edit" + emp.employee_id + "' style='float: right; height :50%;'>Edit</span></button>");
                    editBtn.on('click', function() {
                        
                        var parent = $(this).parent();
                        parent.empty();
                        var textfield = $("<form class='form-inline'><div class='form-group'><label for='edit_name'>Employee name:</label></div></form>");
                        var theField = $("<input type='text' class='form-control' id='edit_name' placeholder='Enter new name' name='edit_name'>");
                        textfield.append(theField);
                        parent.append(textfield);
                        var editEmployee = $("<button type='button' class='btn btn-dark btn-sm' id='edit_btn'>Edit</button>");
                        editEmployee.on('click', function() {
                            var req = {
                                emp_id: emp.employee_id,
                                name: theField.val()
                            }
                            $.ajax({
                                type: 'PUT',
                                dataType: "json",
                                url: '/employees/'+ emp.employee_id,
                                data: req,
                                success: function(resp) {
                                    groupList();
                                }
                            });
                        });

                        parent.append(editEmployee);
                        
                    });
                    
                    element.append(" </br> <b>Username:</b> " + emp.username + "<b>Authority:</b>" + emp.access_level);
                    element.append(editBtn);
                    
                    deleteBtn = $("<button type='button' class='btn btn-danger btn-sm' style='float: right; height :50%;'>Delete</span></button>").attr('id', 'remove'+emp.employee_id);
                    deleteBtn.on('click', function(){
                        var req = {
                            emp_id: emp.employee_id
                        }
                        $.ajax({
                            type: 'DELETE',
                            dataType: "json",
                            url: '/employees/'+emp.employee_id,
                            data: req,
                            success: function(resp) {
                                groupList();
                            }
                        });
                    });
                    element.append(deleteBtn);
                    groupParent.append(element);
                });           
            }
        });  

    }

    var currentIDs = $('#emp_id');
    currentIDs.empty();
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/employees',
        success: function(resp) {
            $.each(resp, function(j, employees) {
                $.each(employees, function(i, emp) {
                    element = $("<option value='" + emp.employee_id + "'>" + emp.employee_id + "</option>");
                    currentIDs.append(element);
                });                
            });
        }
    });    
}
