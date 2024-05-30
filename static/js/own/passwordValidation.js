(() => {
    'use strict'
    if (window.location.pathname === '/users/register/') {
        const forms = document.querySelectorAll('.needs-validation')

        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                const password1 = form.querySelector('input[name="password1"]').value;
                const password2 = form.querySelector('input[name="password2"]').value;
                displayEmptyPasswordError(form);
                if (password1 !== password2) {
                    event.preventDefault();
                    event.stopPropagation();
                    displayDivergentPasswordError(form, 'Passwords do not match');
                } else if (password1.length < 8) {
                    event.preventDefault();
                    event.stopPropagation();
                    displayEmptyPasswordError(form);
                    displayInvalidPasswordError(form, 'Password must be at least 8 characters');
                } else if (passwordSimilarToPersonalInfo(password1)) {
                    event.preventDefault();
                    event.stopPropagation();
                    displayEmptyPasswordError(form);
                    displayInvalidPasswordError(form, 'Password is too similar to personal information');
                } else if (isCommonPassword(password1)) {
                    event.preventDefault();
                    event.stopPropagation();
                    displayEmptyPasswordError(form);
                    displayInvalidPasswordError(form, 'Password is commonly used');
                } else if (isEntirelyNumeric(password1)) {
                    event.preventDefault();
                    event.stopPropagation();
                    displayEmptyPasswordError(form);
                    displayInvalidPasswordError(form, 'Password can’t be entirely numeric');
                }


                form.classList.add('was-validated');
            }, false)
        })


    } else {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        const forms = document.querySelectorAll('.needs-validation')

        // Loop over them and prevent submission
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
    }

    function displayEmptyPasswordError(form) {
        const passwordInput1 = form.querySelector('input[name="password1"]');
        const feedback1 = passwordInput1.nextElementSibling.nextElementSibling;
        feedback1.innerText = '';
        passwordInput1.classList.remove('is-invalid');
        const passwordInput2 = form.querySelector('input[name="password2"]');
        const feedback2 = passwordInput2.nextElementSibling.nextElementSibling;
        feedback2.innerText = '';
        passwordInput2.classList.remove('is-invalid');
        form.classList.remove('was-validated');
    }

    function displayInvalidPasswordError(form, message) {
        const passwordInput = form.querySelector('input[name="password1"]');
        const feedback = passwordInput.nextElementSibling.nextElementSibling;
        feedback.innerText = message;
        passwordInput.classList.add('is-invalid');
    }

    function displayDivergentPasswordError(form, message) {
        const passwordInput = form.querySelector('input[name="password2"]');
        const feedback = passwordInput.nextElementSibling.nextElementSibling;
        feedback.innerText = message;
        passwordInput.classList.add('is-invalid');
    }

    function passwordSimilarToPersonalInfo(password) {
        // Implement your logic to check similarity with personal info
        // For example, check if the password contains parts of personal information
        // Return true if it's too similar, false otherwise
        // Example logic: You can check for similarities with email, username, etc.
        return false; // Placeholder - replace with your validation logic
    }

    function isCommonPassword(password) {
        // Implement your logic to check if the password is commonly used
        // Check against a list of commonly used passwords
        // Return true if it's a common password, false otherwise
        return false; // Placeholder - replace with your validation logic
    }

    function isEntirelyNumeric(password) {
        // Implement your logic to check if the password is entirely numeric
        // Return true if it's entirely numeric, false otherwise
        return /^\d+$/.test(password);
    }
})()