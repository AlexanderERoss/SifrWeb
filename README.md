# SifrWeb
A web page for the Sifr universal xcimal calculator.

Sifr is a universal calculator than can define positional x-base number system using the character list (e.g. '0123456789' for the Hindu-Arabic number system) and then can do arithmetic based by extended dunder methods.

## Architecture
Front end webpage runs Javascript to a loopback port which parses text (explicitly with BOMDAS, sorry SQL injecters) and runs it through a back-end which then serves the response.

## Repo Structure
Divided into front-end (raw HTML, CSS, and JS) and back-end (Python) at the highest level.

## Dependencies
- Sifr pip package for the back-end
- Flask for the API

## To Implement
Currently relies upon BODMSA ordering and requires that O (or exponentiation) is the first thing implemented. Can adjust this to generalize to all functions that precede the multiplication operator (to account for the effect of the unary negation operator)
