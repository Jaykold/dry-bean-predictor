function displayResult(result) {
    var resultElement = document.getElementById('result');
    resultElement.textContent = "Your Dry bean is " + result;
    resultElement.classList.remove('hidden');
}

setTimeout(function() {
    displayResult("Example Bean");
}, 2000000);


const populateDropdown = (input, dropDown, values) => {values.forEach(value => {
// Optional: Show/hide dropdown when input is focused
input.addEventListener('focus', () => {
    dropDown.style.display = 'block';
});

input.addEventListener('blur', () => {
    // Optionally, add a delay to allow clicking on dropdown items
    setTimeout(() => {
        dropDown.style.display = 'none';
    }, 200);
});

const dropDownChild = document.createElement('div');
    dropDownChild.textContent = value;
    dropDownChild.classList.add('dropdown-item');
    dropDownChild.addEventListener('click', () => {
        console.log(value)
        input.value = value;
        console.log("input value",input.value)
        areaDropDown.style.display = 'none'; // Hide dropdown after selection
    });

    dropDown.appendChild(dropDownChild);
});}

const areaValues = [71236, 39318, 34045];

const areaInput = document.getElementById("area-input");
const areaDropDown = document.getElementById("area-dropdown");

populateDropdown(areaInput, areaDropDown, areaValues)


const perimeterValues = [1055.392, 746.921, 681.927];
const perimeterInput = document.getElementById("perimeter-input");
const perimeterDropDown = document.getElementById("perimeter-dropdown");

populateDropdown(perimeterInput, perimeterDropDown, perimeterValues)

const majoraxislengthValues = [345.968599, 279.815434, 252.167650];
const majoraxislengthInput = document.getElementById("majoraxislength-input");
const majoraxislengthDropDown = document.getElementById("majoraxislength-dropdown");

populateDropdown(majoraxislengthInput, majoraxislengthDropDown, majoraxislengthValues)

const minoraxislengthValues = [264.740746, 179.451019, 172.362100];
const minoraxislengthInput = document.getElementById("minoraxislength-input");
const minoraxislengthDropDown = document.getElementById("minoraxislength-dropdown");

populateDropdown(minoraxislengthInput, minoraxislengthDropDown, minoraxislengthValues)

const aspectratioValues = [1.487857, 2.092897, 1.606084];
const aspectratioInput = document.getElementById("aspectratio-input");
const aspectratioDropDown = document.getElementById("aspectratio-dropdown");

populateDropdown(aspectratioInput, aspectratioDropDown, aspectratioValues)

const eccentricityValues = [0.740453, 0.878465, 0.782514];
const eccentricityInput = document.getElementById("eccentricity-input");
const eccentricityDropDown = document.getElementById("eccentricity-dropdown");

populateDropdown(eccentricityInput, eccentricityDropDown, eccentricityValues)
