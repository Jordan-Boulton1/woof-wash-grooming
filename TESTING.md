# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

## Code Validation

### HTML

I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

| Directory | File | Screenshot                                                                       | Notes                                                                                                    |
| --- | --- |----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| grooming_service | 404.html | ![screenshot](documentation/testing/validation/html/404-error-validation.png)         | Pass: No Errors                                                                                          |
| grooming_service | about.html | ![screenshot](documentation/testing/validation/html/about-html-validation.png)        | Pass: No Errors                                                                                          |
| grooming_service | appointment.html | ![screenshot](documentation/testing/validation/html/appointment-html-validation.png)  | Pass: No Errors                                                                                          |
| grooming_service | edit_profile.html | ![screenshot](documentation/testing/validation/html/profile-edit-html-validation.png) | Pass: No Errors                                                                                          |
| grooming_service | home.html | ![screenshot](documentation/testing/validation/html/home-html-validation.png)         | I am aware of the errors on this page, the errors are due to summernote rendering the short description. |
| grooming_service | login.html | ![screenshot](documentation/testing/validation/html/login-html-validation.png)        | Pass: No Errors                                                                                          |
| grooming_service | profile.html | ![screenshot](documentation/testing/validation/html/profile-html-validation.png) | Pass: No Errors |                                                                                         |
| grooming_service | register.html | ![screenshot](documentation/testing/validation/html/register-html-validation.png)     | Pass: No Errors                                                                                          |
| grooming_service | services.html | ![screenshot](documentation/testing/validation/html/services-html-validation.png)     | I am aware of the errors on this page, the errors are caused when rendering the summernote descriptions. |

### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

| Directory | File | Screenshot | Notes                                                                                                                                                                                          |
| --- | --- | --- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| static | style.css | ![screenshot](documentation/testing/validation/css/css-validation.png) | I am aware of the error that occurs when running through the validator however, due to the error coming from the external flatpickr.css and not my own, I am unable to do anything about this. |

### JavaScript

I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.

| Directory | File | Screenshot                                                                  | Notes                                |
| --- | --- |-----------------------------------------------------------------------------|--------------------------------------|
| static | edit_profile.js | ![screenshot](documentation/testing/validation/js/edit-profile-js-validation.png) | Pass: No Errors                      |
| static | login.js | ![screenshot](documentation/testing/validation/js/login-js-validation.png)  | Pass: No Errors                      |
| static | profile.js | ![screenshot](documentation/testing/validation/js/profile-js-validation.png) | Unused variables from external files |
| static | register.js | ![screenshot](documentation/testing/validation/js/register-js-validation.png) | Pass: No Errors                      |
| static | script.js | ![screenshot](documentation/testing/validation/js/script-js-validation.png) | Pass: No Errors                      |

### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| Directory | File | CI URL | Screenshot                                                                                | Notes |
| --- | --- | --- |-------------------------------------------------------------------------------------------| --- |
| grooming_service | admin.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/admin.py) | ![screenshot](documentation/testing/validation/python/admin-validation.png)               | Pass: No Errors |
| grooming_service | custom_user_manager.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/custom_user_manager.py) | ![screenshot](documentation/testing/validation/python/custom-user-manager-validation.png) | Pass: No Errors |
| grooming_service | forms.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/forms.py) | ![screenshot](documentation/testing/validation/python/forms-validation.png)               | Pass: No Errors |
| grooming_service | models.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/models.py) | ![screenshot](documentation/testing/validation/python/models-validation.png)              | Pass: No Errors |
| grooming_service | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/urls.py) | ![screenshot](documentation/testing/validation/python/urls-validation.png)                | Pass: No Errors |
| grooming_service | validators.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/validators.py) | ![screenshot](documentation/testing/validation/python/validators.png)                     | Pass: No Errors|
| grooming_service | views.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/grooming_service/views.py) | ![screenshot](documentation/validation/path-to-screenshot.png)                            | |
|  | manage.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/manage.py) | ![screenshot](documentation/testing/validation/python/manage-validation.png)              | Pass: No Errors |
| woof_wash_grooming | settings.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/woof_wash_grooming/settings.py) | ![screenshot](documentation/testing/validation/python/settings-validation.png)            | Pass: No Errors |
| woof_wash_grooming | urls.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woof-wash-grooming/main/woof_wash_grooming/urls.py) | ![screenshot](documentation/testing/validation/python/urls-validation2.png)               | Pass: No Errors |

## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.

| Browser | Home                                                                          | About                                                                       | Services                                                                  | Appointment                                                                  | Profile                                                                  | Edit Profile                                                                  | Register                                                                  | Login                                                                  | 404 Error Page                                                       | Notes |
| --- |-------------------------------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------------|------------------------------------------------------------------------|----------------------------------------------------------------------| --- |
| Chrome | ![screenshot](documentation/testing/browsers/browser-chrome-home.png)         | ![screenshot](documentation/testing/browsers/browser-chrome-about.png) | ![screenshot](documentation/testing/browsers/browser-chrome-services.png) | ![screenshot](documentation/testing/browsers/browser-chrome-appointment.png) | ![screenshot](documentation/testing/browsers/browser-chrome-profile.png) | ![screenshot](documentation/testing/browsers/browser-chrome-edit-profile.png) | ![screenshot](documentation/testing/browsers/browser-chrome-register.png) | ![screenshot](documentation/testing/browsers/browser-chrome-login.png) | ![screenshot](documentation/testing/browsers/browser-chrome-404.png) | Works as expected |
| Firefox| ![screenshot](documentation/testing/browsers/browser-firefox-home.png) | ![screenshot](documentation/testing/browsers/browser-firefox-about.png) | ![screenshot](documentation/testing/browsers/browser-firefox-services.png) | ![screenshot](documentation/testing/browsers/browser-firefox-appointment.png) | ![screenshot](documentation/testing/browsers/browser-firefox-profile.png) | ![screenshot](documentation/testing/browsers/browser-firefox-edit-profile.png) | ![screenshot](documentation/testing/browsers/browser-firefox-register.png) | ![screenshot](documentation/testing/browsers/browser-firefox-login.png) | ![screenshot](documentation/testing/browsers/browser-firefox-404.png) | Works as expected |