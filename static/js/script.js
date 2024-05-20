document.addEventListener("DOMContentLoaded", function() {
    const dateFieldIcon = document.getElementById("start-date-icon")


    dateFieldIcon.addEventListener("click", function(event) {
        event.preventDefault();
        const dateTimeFlatpickrContainer = document.getElementsByClassName("django-flatpickr")[0]._flatpickr;
        if (dateTimeFlatpickrContainer){
            dateTimeFlatpickrContainer.open();
        }
    });

});

