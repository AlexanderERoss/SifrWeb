// Script for interacting with back end

var host = "http://localhost:5000";
async function getSifrCalc(characterSet, radixPoint, negativeSign, formula) {
    console.log("Character Set: " + characterSet);
    console.log("Radix Point: " + radixPoint);
    console.log("Negative Sign: " + negativeSign);
    console.log("Formula: " + formula);
    calc_data = JSON.stringify({"CharacterSet": characterSet,
                                "RadixPoint": radixPoint,
                                "NegativeSign": negativeSign,
                                "Formula": formula});
    console.log("JSON submitted: ");
    console.log(calc_data);
    try {
        let promise = await fetch(host + "/sifr/api/calculate_sifr",
                                  {method: "POST",
                                   body: calc_data,
                                   headers: {"Accept": "application/json",
                                             "Content-Type": "application/json"}});

        let resultJSON = await promise.json();
        console.log(promise.status);
        console.log("Result: ");
        await console.log(resultJSON);
        return resultJSON;
    }
    catch(err) {
        // Make a result JSON describing the back-end being down instead
        await console.log("ERROR: " + err.message)
        if (err.message === "Failed to fetch") {
            resultJSON = {"Response": 503,
                          "Result": "Back-end server is not running or located at different address"};
            return resultJSON;
        }
        else {
            resultJSON = {"Response": 500,
                          "Result": err.message};
            return resultJSON;
        }
    }
}

// Takes the fields and calculates the formula using the back-end
async function calculate() {
    var characterSet = await document.getElementById("character-set").value;
    var radixPoint = await document.getElementById("radix").value;
    var negativeSign = await document.getElementById("negative-sign").value;
    var formula = await document.getElementById("formula").value;

    sifrResponse = await getSifrCalc(characterSet, radixPoint, negativeSign, formula);

    document.getElementById("resultTitle").innerHTML = "Result:";
    // Layer which deals with back-end errors
    responseCode = await sifrResponse["Response"]
    console.log(responseCode)
    if (responseCode == 200) {
        document.getElementById("result").innerHTML = await sifrResponse["Result"];
        document.getElementById("resultError").innerHTML = "";
        document.getElementById("scopedError").innerHTML = "";
    }
    else if (responseCode == 422) {
        document.getElementById("result").innerHTML = "";
        document.getElementById("resultError").innerHTML = "";
        document.getElementById("scopedError").innerHTML=  "SYNTACTIC ERROR (422): " + await sifrResponse["Result"];
    }
    else if (responseCode == 503) {
        document.getElementById("result").innerHTML = "";
        document.getElementById("resultError").innerHTML=  "BACK-END ERROR (503): " + await sifrResponse["Result"];
        document.getElementById("scopedError").innerHTML = "";
    }
    else {
        document.getElementById("result").innerHTML = "";
        document.getElementById("resultError").innerHTML=  "UNKNOWN ERROR (" +
            await sifrResponse["Response"] + "): " + await sifrResponse["Result"];
        document.getElementById("scopedError").innerHTML = "";
    }
}
