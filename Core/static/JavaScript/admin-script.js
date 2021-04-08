window.onload = () => {
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

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value
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
        
        return false;
    };

    filterForm3.onsubmit = (event) => {
        
        return false;
    };
};