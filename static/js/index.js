function displayResult(result) {
    var resultElement = document.getElementById('result');
    resultElement.textContent = "Your Dry bean is " + result;
    resultElement.classList.remove('hidden');
}

setTimeout(function() {
    displayResult("Example Bean");
}, 2000000);


const populateDropdown = (input, dropDown) => {numberValues.forEach(value => {
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

const numberValues = [1, 2, 3, 4, 5, 6];

const areaInput = document.getElementById("area-input");
const areaDropDown = document.getElementById("area-dropdown");

populateDropdown(areaInput, areaDropDown)

const perimeterInput = document.getElementById("perimeter-input");
const perimeterDropDown = document.getElementById("perimeter-dropdown");

populateDropdown(perimeterInput, perimeterDropDown)





