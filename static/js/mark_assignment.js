document.addEventListener("DOMContentLoaded", function () {
    // Get CSRF token from meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

    document.querySelectorAll(".mark-done-checkbox").forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            let assignmentId = this.dataset.assignmentId;

            fetch(`/ajax/assignments/${assignmentId}/complete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,  // Attach CSRF token
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    location.reload();  // Reload to move the assignment
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
