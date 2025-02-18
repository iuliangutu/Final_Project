document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-item-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Stop the link from redirecting

            const itemRow = event.target.closest("tr"); // Get the row of the item
            const deleteUrl = event.target.href; // Get delete URL

            console.log("Attempting to remove item:", deleteUrl);

            fetch(deleteUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(), // Get CSRF token dynamically
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server Response:", data); // Log server response

                if (data.success) {
                    itemRow.remove(); // Remove item row from table
                    document.getElementById("cart-total-cost").textContent = "Total cost: $" + data.total_cost.toFixed(2);
                } else {
                    console.error("Failed to remove item:", data);
                    alert("Failed to remove item. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error removing item:", error);
                alert("An error occurred. Please try again.");
            });
        });
    });

    // Function to fetch CSRF token from Django cookie
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
        return cookieValue || "";
    }
});