document.addEventListener("DOMContentLoaded", function() {
    const dateField = document.getElementById("id_start_date");
    const timeField = document.getElementById("id_start_time");
    const petField = document.getElementById("id_pet");
    const serviceField = document.getElementById("id_service");
    const dateFieldIcon = document.getElementById("start-date-icon")
    setDefaultOption(timeField, "Select a time");
    setDefaultOption(petField, "Select a pet");
    setDefaultOption(serviceField, "Select a service");

    dateFieldIcon.addEventListener("click", function(event) {
        event.preventDefault();
        const dateTimeFlatpickrContainer = document.getElementsByClassName("django-flatpickr")[0]._flatpickr;
        if (dateTimeFlatpickrContainer){
            dateTimeFlatpickrContainer.open();
        }
    });

    dateField.addEventListener("change", function() {
        const selectedDate = dateField.value;

        if (selectedDate) {
            fetch(`/api/available-times/${selectedDate}/`)
                .then((response) => response.json())
                .then((times) => {
                    timeField.innerHTML = "";

                    setDefaultOption(timeField, "Select a time");
                    times.forEach((time) => {
                        const option = document.createElement("option");
                        option.value = time;
                        option.text = time;
                        timeField.appendChild(option);
                    });
                })
                .catch((error) => console.error("Error fetching available times:", error));
        } else {
            timeField.innerHTML = "";
            setDefaultOption(timeField, "Select a time");
        }
    });
});

function setDefaultOption(selectElement, defaultValue) {

    var defaultOption = document.createElement("option");
    
    defaultOption.value = defaultValue;
    defaultOption.text = defaultValue;

    selectElement.add(defaultOption, 0);
    
    defaultOption.selected = true;
}
