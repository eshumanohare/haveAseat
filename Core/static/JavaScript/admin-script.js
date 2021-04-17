function deleteStudent(username, row) {
    fetch(`/admin-panel/delete-student/${username}/`, {
        method: "POST",
        body: JSON.stringify({}),
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        }
    })
    .then(response => response.json())
    .then(response => {
        const panelMessage = document.getElementById("Panel-Message");
        console.log(response);
        const messageHTML = `<div id="Deleted-Student-Card"><img id="Deleted-Student-Card-Cross" onclick="this.parentElement.remove();" src="/static/Images/Cross.png"><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Username</p><p class="Deleted-Student-Details-Text">${response["username"]}</p></div><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Name</p><p class="Deleted-Student-Details-Text">${response["firstName"] + ' ' + response["lastName"]}</p></div><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Email</p><p class="Deleted-Student-Details-Text">${response["email"]}</p></div><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Roll Number</p><p class="Deleted-Student-Details-Text">${response["rollNumber"]}</p></div><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Program</p><p class="Deleted-Student-Details-Text">${response["program"]}</p></div><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Batch</p><p class="Deleted-Student-Details-Text">${response["batch"]}</p></div><div class="Deleted-Student-Details"><p class="Deleted-Student-Details-Heading">Branch</p><p class="Deleted-Student-Details-Text">${response["branch"]}</p></div></div>`;
        panelMessage.innerHTML = messageHTML;
        row.remove();
    });
}

function disableAllForms(forms) {
    forms.forEach(function(item, index) {
        item.classList.add("Hide");
    });
}

function disableAllFormsExcept(forms, number) {
    forms.forEach(function(item, index) {
        if (index != number) {
            item.classList.add("Hide");
        } else {
            item.classList.toggle("Hide");
        }
    });
}

function displayStudents(outputs) {
    let newHTML = `<tr class="Panel-Table-Row">
        <th class="Panel-Table-Heading">S. No</th>
        <th class="Panel-Table-Heading">Name</th>
        <th class="Panel-Table-Heading">Username</th>
        <th class="Panel-Table-Heading">Email</th>
        <th class="Panel-Table-Heading">Roll Number</th>
        <th class="Panel-Table-Heading">Batch</th>
        <th class="Panel-Table-Heading">Program</th>
        <th class="Panel-Table-Heading">Branch</th>
        <th class="Panel-Table-Heading">Date of Joining</th>
        <th class="Panel-Table-Heading">Graduation Year</th>
        <th class="Panel-Table-Heading">Remove</th>
    </tr>`;

    for (let i = 0 ; i < outputs.length ; i++) {
        newHTML += `<tr class="Panel-Table-Row">
            <td class="Panel-Table-Heading">${i}</td>  
            <td class="Panel-Table-Heading">${outputs[i]["firstName"] + " " + outputs[i]["lastName"]}</td>
            <td class="Panel-Table-Heading">${outputs[i]["username"]}</td>
            <td class="Panel-Table-Heading">${outputs[i]["email"]}</td>    
            <td class="Panel-Table-Heading">${outputs[i]["rollNumber"]}</td>    
            <td class="Panel-Table-Heading">${outputs[i]["batch"]}</td>    
            <td class="Panel-Table-Heading">${outputs[i]["program"]}</td>    
            <td class="Panel-Table-Heading">${outputs[i]["branch"]}</td>    
            <td class="Panel-Table-Heading">${outputs[i]["dateOfJoining"]}</td>    
            <td class="Panel-Table-Heading">${outputs[i]["graduationYear"]}</td>    
            <td class="Panel-Table-Heading">
                <button class="Panel-Row-Button Red" onclick="deleteStudent('${outputs[i]["username"]}', this.parentElement.parentElement);">Remove</button> 
            </td>
        </tr>`;
    }    

    panelTable.innerHTML = newHTML;
}

function displayCourses(outputs) {
    let newHTML = `<tr class="Panel-Table-Row">
    <th class="Panel-Table-Heading">S. No</th>
    <th class="Panel-Table-Heading">Course Name</th>
    <th class="Panel-Table-Heading">Section</th>
    <th class="Panel-Table-Heading">Credits</th>
    <th class="Panel-Table-Heading">Student Cap</th>
    <th class="Panel-Table-Heading">Program</th>
    <th class="Panel-Table-Heading">Department</th>
    <th class="Panel-Table-Heading">View Details</th>
</tr>`;

    for (let i = 0 ; i < outputs.length ; i++) {
        newHTML += `<tr class="Panel-Table-Row">
        <td class="Panel-Table-Heading">${i}</td>  
        <td class="Panel-Table-Heading">${outputs[i]["courseName"]}</td>
        <td class="Panel-Table-Heading">${outputs[i]["section"]}</td>
        <td class="Panel-Table-Heading">${outputs[i]["credits"]}</td>    
        <td class="Panel-Table-Heading">${outputs[i]["studentCap"]}</td>    
        <td class="Panel-Table-Heading">${outputs[i]["program"]}</td>    
        <td class="Panel-Table-Heading">${outputs[i]["department"]}</td>      
        <td class="Panel-Table-Heading">
            <button class="Panel-Row-Button Red">View Details</button>
        </td>
    </tr>`;
    }    

    panelTable.innerHTML = newHTML;
}

function displayFaculties(outputs) {
    let newHTML = `<tr class="Panel-Table-Row">
    <th class="Panel-Table-Heading">S. No</th>
    <th class="Panel-Table-Heading">Username</th>
    <th class="Panel-Table-Heading">Name</th>
    <th class="Panel-Table-Heading">Email</th>
    <th class="Panel-Table-Heading">Profile Links</th>
</tr>`;

    for (let i = 0 ; i < outputs.length ; i++) {
        newHTML += `<tr class="Panel-Table-Row">
        <td class="Panel-Table-Heading">${i}</td>  
        <td class="Panel-Table-Heading">${outputs[i]["username"]}</td>
        <td class="Panel-Table-Heading">${outputs[i]["firstName"] + " " + outputs[i]["lastName"]}</td>
        <td class="Panel-Table-Heading">${outputs[i]["email"]}</td>    
        <td class="Panel-Table-Heading">
        <a href="${outputs[i]["profileLink"]}" target="_blank" class="Panel-Row-Button Red">Visit Profile</a>
        </td>
    </tr>`;
    }    

    panelTable.innerHTML = newHTML;
}

const filterForm1 = document.getElementById("Filter-Form-1");
const filterForm2 = document.getElementById("Filter-Form-2");
const filterForm3 = document.getElementById("Filter-Form-3");
const panelTable = document.getElementById("Panel-Table");
const formHeadings = document.querySelectorAll(".Form-Heading");
const forms = [filterForm1, filterForm2, filterForm3];

disableAllForms(forms);

formHeadings.forEach(function (item, index) {
    item.addEventListener("click", () => {
        disableAllFormsExcept(forms, index);
    });
});


filterForm1.onsubmit = () => {        
    // Filtering selected sections
    let sections = document.querySelectorAll("#Filter-Form-1 .Course-Section");
    let selectedSections = []

    sections.forEach(function(item, index) {
        if (item.checked) {
            selectedSections.push(item.value);
        }
    });

    // Filtering selected credits
    let credits = document.querySelectorAll("#Filter-Form-1 .Credits");
    let selectedCredits = []

    credits.forEach(function(item, index) {
        if (item.checked) {
            selectedCredits.push(item.value);
        }
    });

    // Filtering selected programs
    let programs = document.querySelectorAll("#Filter-Form-1 .Program");
    let selectedPrograms = []

    programs.forEach(function(item, index) {
        if (item.checked) {
            selectedPrograms.push(item.value);
        }
    });

    // Filtering selected departments
    let departments = document.querySelectorAll("#Filter-Form-1 .Department");
    let selectedDepartments = []

    departments.forEach(function(item, index) {
        if (item.checked) {
            selectedDepartments.push(item.value);
        }
    });

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const data = {
        "sections": selectedSections,
        "credits": selectedCredits,
        "programs": selectedPrograms,
        "departments": selectedDepartments,
    };

    fetch("/fetch-courses/", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "X-CSRFToken": csrfToken,
        }
    })
    .then(response => response.json())
    .then(response => {
        if (response["success"]) {
            console.log(response["outputs"]);
            displayCourses(response["outputs"]);
        } else {
            alert("Some error occured while fetching the data");
        }
    });

    return false;
};

filterForm2.onsubmit = (event) => {
    // Filtering selected branches
    let branches = document.querySelectorAll("#Filter-Form-2 .Branch");
    let selectedBranches = []

    branches.forEach(function(item, index) {
        if (item.checked) {
            selectedBranches.push(item.value);
        }
    });

    // Filtering selected departments
    let years = document.querySelectorAll("#Filter-Form-2 .Year");
    let selectedYears = []

    years.forEach(function(item, index) {            
        selectedYears.push(item.value);
    });

    // Filtering selected programs
    let programs = document.querySelectorAll("#Filter-Form-2 .Program");
    let selectedPrograms = []

    programs.forEach(function(item, index) {
        if (item.checked) {
            selectedPrograms.push(item.value);
        }
    });

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const data = {
        "branches": selectedBranches,
        "years": selectedYears,
        "programs": selectedPrograms,
    };

    fetch("/fetch-students/", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "X-CSRFToken": csrfToken,
        }
    })
    .then(response => response.json())
    .then(response => {
        if (response["success"]) {
            console.log(response["outputs"]);
            displayStudents(response["outputs"]);
        } else {
            alert("Some error occured while fetching the data");
        }
    });
    
    return false;
};

filterForm3.onsubmit = (event) => {
    // Filtering selected departments
    let departments = document.querySelectorAll("#Filter-Form-3 .Department");
    let selectedDepartments = []

    departments.forEach(function(item, index) {
        if (item.checked) {
            selectedDepartments.push(item.value);
        }
    });

    // Filtering selected programs
    let programs = document.querySelectorAll("#Filter-Form-3 .Program");
    let selectedPrograms = []

    programs.forEach(function(item, index) {
        if (item.checked) {
            selectedPrograms.push(item.value);
        }
    });

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const data = {        
        "programs": selectedPrograms,
        "departments": selectedDepartments,
    };

    fetch("/fetch-faculties/", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "X-CSRFToken": csrfToken,
        }
    })
    .then(response => response.json())
    .then(response => {
        if (response["success"]) {
            console.log(response["outputs"]);
            displayFaculties(response["outputs"]);
        } else {
            alert("Some error occured while fetching the data");
        }
    });
    
    return false;
};