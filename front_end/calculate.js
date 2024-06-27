var CONFIG={"api_network": {"host": "localhost", "port": 30003}}
console.log("API Host: " + CONFIG.api_network.host)
console.log("API Port: " + CONFIG.api_network.port)
var host = "http://" +  CONFIG.api_network.host + ":" + JSON.stringify(CONFIG.api_network.port);
console.log(host)
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
    let promise = await fetch(host + "/sifr/api/calculate_sifr",
                              {method: "POST",
                               body: calc_data,
                               headers: {"Accept": "application/json",
                                         "Content-Type": "application/json"}});
    let resultJSON = await promise.json();
    console.log("Result: ");
    await console.log(resultJSON);
    return resultJSON;
}

async function calculate() {
    var characterSet = await document.getElementById("character-set").value;
    var radixPoint = await document.getElementById("radix").value;
    var negativeSign = await document.getElementById("negative-sign").value;
    var formula = await document.getElementById("formula").value;

    sifrResponse = await getSifrCalc(characterSet, radixPoint, negativeSign, formula);

    document.getElementById("resultTitle").innerHTML = "Result:";
    // Layer which deals with back-end errors
    responseCode = await sifrResponse["Response"]
    if (responseCode == 200) {
        document.getElementById("result").innerHTML = sifrResponse["Result"];

    }
    else if (responseCode == 422) {
        document.getElementById("result").innerHTML = "ERROR: " + sifrResponse["Result"];
    }
}
