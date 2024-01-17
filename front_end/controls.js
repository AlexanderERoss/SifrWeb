// Controls to speed up using the front-end

// Enter triggers calculate button
document.getElementById("body")
    .addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("calculate-button").click();
        }
    });

// Number system data

let jsontext = {"Anglo Hindu-Arabic": {"Note": "",
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
                "Eastern Arabic - left to right": {"Note": "Left to right parsing; numerals are written the same as they traditionally write the lowest value digit first",
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
                          "Character Set":"𝋠𝋡𝋢𝋣𝋤𝋥𝋦𝋧𝋨𝋩𝋪𝋫𝋬𝋭𝋮𝋯𝋰𝋱𝋲𝋳"}
                "Braille": {"Radix Point": "٫",
                            "Negative Symbol": "-",
                            "Character Set": ""},
               }
