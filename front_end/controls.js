// Controls to speed up using the front-end

// Enter triggers calculate button
document.getElementById("body")
    .addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("calculate-button").click();
        }
    });

// Function to populate controls (calls other functions)
function populateControls() {
    populateSystemSelector();
    document.getElementById("systemSelect").value = "Anglo Hindu-Arabic";
    systemSelect();
}

// Number system form data

let jsonText = {"Anglo Hindu-Arabic": {"Note": "",
                                       "Radix Point": ".",
                                       "Negative Symbol": "-",
                                       "Character Set": "0123456789"},
                "Continental Hindu-Arabic": {"Note": "",
                                             "Radix Point": ",",
                                             "Negative Symbol": "-",
                                             "Character Set": "0123456789"},
                "Binary": {"Note": "",
                           "Radix Point": ".",
                           "Negative Symbol": "-",
                           "Character Set": "01"},
                "Hexadecimal": {"Note": "",
                                "Radix Point": ".",
                                "Negative Symbol": "-",
                                "Character Set": "0123456789ABCDEF"},
                "Eastern Arabic - (left to right formula parsing)": {"Note": "Left to right parsing; numerals are written the same as they traditionally write the lowest value digit first",
                                                   "Radix Point": "٫",
                                                   "Negative Symbol": "-",
                                                   "Character Set": "٠١٢٣٤٥٦٧٨٩"},
                "Traditional Chinese Rod Numerals": {"Note": "Chosen horizontal direction; newer 〇 used instead of space for zero, negative slash through is ignored and a negative symbol is used, and radix uses traditional Chinese fraction symbol instead (unicode tally mark used)",
                                                     "Radix Point": "𝍷",
                                                     "Negative Symbol": "-",
                                                     "Character Set": "〇𝍠𝍡𝍢𝍣𝍤𝍥𝍦𝍧𝍨"},
                "Mayan": {"Note": "Assumed radix 〇, left-to-right",
                          "Radix Point": "〇",
                          "Negative Symbol": "-",
                          "Character Set":"𝋠𝋡𝋢𝋣𝋤𝋥𝋦𝋧𝋨𝋩𝋪𝋫𝋬𝋭𝋮𝋯𝋰𝋱𝋲𝋳"},
                "English Braille - EBAE": {"Note": "Ignores the number marker at the start (⠼)",
                                           "Radix Point": "⠨",
                                           "Negative Symbol": "⠤",
                                           "Character Set": "⠚⠁⠃⠉⠙⠑⠋⠛⠓⠊"},
               }

function populateSystemSelector() {
    systemSelectElement = document.getElementById('systemSelect')
        systemSelectElement.add(new Option("Custom"));
    for (var field in jsonText) {
        systemSelectElement.add(new Option(field));
    }
}

function systemSelect() {
    // Get value from dropdown
    system = document.getElementById('systemSelect').value;
    // Apply to fields
    document.getElementById('character-set').value = jsonText[system]["Character Set"]; 
    document.getElementById('radix').value = jsonText[system]["Radix Point"];
    document.getElementById('negative-sign').value = jsonText[system]["Negative Symbol"];
    if (jsonText[system]["Note"] !== "") {
        document.getElementById('system-note').innerHTML = "Number system note: " + jsonText[system]["Note"];
    }
}

function selectCustom() {
    document.getElementById("systemSelect").value = "Custom";
}
