// Controls to speed up using the front-end

// Enter triggers calculate button
document.getElementById("body")
    .addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("calculate-button").click();
        }
    });


