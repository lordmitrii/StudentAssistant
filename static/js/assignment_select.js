document.addEventListener("DOMContentLoaded", function() {
    const courseSelect = document.getElementById("id_course");
    const assignmentSelect = document.getElementById("id_assignment");
    // if courseSelect is not null, add event listener
    if (courseSelect) {
        courseSelect.addEventListener("change", function() {
            const courseId = this.value;
            
            // if courseId is empty, clear the assignmentSelect and return
            // this is to avoid sending an empty request to the server
            if (!courseId) {
                assignmentSelect.innerHTML = "";
                const emptyOption = document.createElement("option");
                emptyOption.value = "";
                emptyOption.text = "No Assignments Available";
                assignmentSelect.appendChild(emptyOption);
                return;
            }
            
            // Fetch assignments for the selected course
            fetch(`/ajax/get_assignments/?course_id=${courseId}`)
                .then(response => response.json())
                .then(data => {
                    assignmentSelect.innerHTML = "";
                    
                    // Check if the response contains assignments
                    if (data.assignments.length === 0) {
                        const emptyOption = document.createElement("option");
                        emptyOption.value = "";
                        emptyOption.text = "No Assignments Available";
                        assignmentSelect.appendChild(emptyOption);
                        return;
                    }

                    // Populate the assignment select element with the fetched assignments
                    const emptyOption = document.createElement("option");
                    emptyOption.value = "";
                    emptyOption.text = "Select Assignment (Optional)";
                    assignmentSelect.appendChild(emptyOption);

                    data.assignments.forEach(function(assignment) {
                        const option = document.createElement("option");
                        option.value = assignment.id;
                        option.text = assignment.name;
                        assignmentSelect.appendChild(option);
                    });
                })
                .catch(error => console.error("Error fetching assignments:", error));
        });
    }
});
