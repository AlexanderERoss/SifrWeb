// Script for interacting with back end

var host = "http://localhost:5000";
async function getSifrCalc(characterSet, xcimalSeparator, negativeSign, formula) {
    console.log("Character Set: " + characterSet);
    console.log("Xcimal Separator: " + xcimalSeparator);
    console.log("Negative Sign: " + negativeSign);
    console.log("Formula: " + formula);
    calc_data = JSON.stringify({"CharacterSet": characterSet,
                                "XcimalSeparator": xcimalSeparator,
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
    var xcimalSeparator = await document.getElementById("xcimal-separator").value;
    var negativeSign = await document.getElementById("negative-sign").value;
    var formula = await document.getElementById("formula").value;

    sifrResponse = await getSifrCalc(characterSet, xcimalSeparator, negativeSign, formula);

    document.getElementById("resultTitle").innerHTML = "Result:";
    document.getElementById("result").innerHTML = sifrResponse["Result"];
}
