document.addEventListener("DOMContentLoaded", function() {
    const petField = document.getElementById("id_pet");
    const serviceField = document.getElementById("id_service");
    const dateFieldIcon = document.getElementById("start-date-icon")


    dateFieldIcon.addEventListener("click", function(event) {
        event.preventDefault();
        const dateTimeFlatpickrContainer = document.getElementsByClassName("django-flatpickr")[0]._flatpickr;
        if (dateTimeFlatpickrContainer){
            dateTimeFlatpickrContainer.open();
        }
    });

});

