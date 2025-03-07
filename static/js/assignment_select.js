document.addEventListener("DOMContentLoaded", function() {
    const courseSelect = document.getElementById("id_course");
    const assignmentSelect = document.getElementById("id_assignment");
    if (courseSelect) {
        courseSelect.addEventListener("change", function() {
            const courseId = this.value;
            fetch(`/ajax/get_assignments/?course_id=${courseId}`)
                .then(response => response.json())
                .then(data => {
                    assignmentSelect.innerHTML = "";
                    
                    if (data.assignments.length === 0) {
                        const emptyOption = document.createElement("option");
                        emptyOption.value = "";
                        emptyOption.text = "No Assignments Available";
                        assignmentSelect.appendChild(emptyOption);
                        return;
                    }
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
