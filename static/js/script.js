if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
document.addEventListener("DOMContentLoaded", function() {
    const dateFieldIcon = document.getElementById("start-date-icon");
    const serviceSelect = document.getElementById("id_service");


    dateFieldIcon.addEventListener("click", function(event) {
        event.preventDefault();
        const dateTimeFlatpickrContainer = document.getElementsByClassName("django-flatpickr")[0]._flatpickr;
        if (dateTimeFlatpickrContainer){
            dateTimeFlatpickrContainer.open();
        }
    });

    serviceSelect.addEventListener('change', function (event) {
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        const selectedValue = selectedOption.value;
        const priceRangeContainer = document.getElementById('servicePrice');
        priceRangeContainer.innerHTML = "";
        if (selectedValue) {
              fetch(`/api/service/price/${selectedValue}/`)
                  .then((response) => response.json())
                  .then((data) => {
                      priceRangeContainer.hidden = false;
                      priceRangeContainer.innerHTML = `<p> Price: £${data.price_range.vary_price1} - £${data.price_range.vary_price2} </p>`
                  });
        }
    });

});

