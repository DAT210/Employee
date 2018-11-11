var employeesByGroup = [];

function groupList() {
    for (var i = 0; i<5; i++) {
        let groupNr = i
        let groupParent = $('#' + groupNr);
       
        console.log(groupParent.attr('id'));
        groupParent.on('click', function() {
            console.log('CLICKED ');
            $.ajax({
                url: "/group-employees/" + groupNr,
                dataType: "json",
                success: function (resp) {
                    console.log(groupNr);
                    groupParent.empty();
                    var listHead = $("<ul></ul>").attr('id', 'groupList'+groupNr);
                    $.each(resp, function(j, emp) {
                        element = $("<li class='list-group-item'></li>").html("Name: " + emp.name + " </br> Username: " + emp.username ).attr('id', emp.employee_id);
                        listHead.append(element);
                    });
                    groupParent.append(listHead);
                    
                }
            }

            );


        } );

    }
}