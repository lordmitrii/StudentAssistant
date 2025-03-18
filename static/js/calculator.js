document.addEventListener("DOMContentLoaded", function() {
    const addRowButton = document.getElementById("add-row");
    const tableBody = document.querySelector("#grades-table tbody");

    // Ensure existing event listeners are removed before adding a new one
    addRowButton.removeEventListener("click", addNewRow);
    addRowButton.addEventListener("click", addNewRow);

    function addNewRow(event) {
        event.stopImmediatePropagation(); // Prevent multiple triggers

        let newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td><input type="text" class="form-control" name="assignment[]" placeholder="Enter assignment name" required></td>
            <td><input type="number" class="form-control grade" name="grade[]" min="0" max="100" placeholder="Enter grade" required></td>
            <td><input type="number" class="form-control credit" name="credits[]" min="1" placeholder="Enter credits" required></td>
            <td><button type="button" class="btn btn-danger remove-row">&times;</button></td>
        `;
        tableBody.appendChild(newRow);
    }

    // Handle form submission
    document.getElementById("calculator-form").addEventListener("submit", function(event) {
        event.preventDefault();
        let grades = document.querySelectorAll(".grade");
        let credits = document.querySelectorAll(".credit");
        let totalWeighted = 0, totalCredits = 0;

        grades.forEach((grade, index) => {
            let gradeValue = parseFloat(grade.value);
            let creditValue = parseFloat(credits[index].value);
            totalWeighted += gradeValue * creditValue;
            totalCredits += creditValue;
        });

        let averageGrade = totalCredits > 0 ? (totalWeighted / totalCredits).toFixed(2) : "-";
        document.getElementById("average-grade").textContent = averageGrade;
    });

    // Handle row removal
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("remove-row")) {
            event.target.closest("tr").remove();
        }
    });
});