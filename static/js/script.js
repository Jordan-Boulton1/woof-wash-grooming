document.addEventListener("DOMContentLoaded", function() {
    const dateField = document.getElementById("id_start_date");
    const timeField = document.getElementById("id_start_time");

    if (timeField) {
        timeField.innerHTML = "";
    }

    dateField.addEventListener("change", function() {
        const selectedDate = dateField.value;

        if (selectedDate) {
            fetch(`/api/available-times/${selectedDate}/`)
                .then((response) => response.json())
                .then((times) => {
                    timeField.innerHTML = "";

                    times.forEach((time) => {
                        const option = document.createElement("option");
                        option.value = time;
                        option.text = time;
                        timeField.appendChild(option);
                    });
                })
                .catch((error) => console.error("Error fetching available times:", error));
        }
    });
});
