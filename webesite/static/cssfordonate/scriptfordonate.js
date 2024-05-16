document.addEventListener("DOMContentLoaded", function() {
    // Define trash varieties with their prices per kilo
    const trashPrices = {
        plastic: {
            bottles: 1.5,
            bags: 0.8,
            containers: 1.2
        },
        metal: {
            cans: 2,
            wire: 3,
            utensils: 1.8
        },
        paper: {
            newspaper: 0.5,
            magazines: 0.7,
            cardboard: 0.9
        }
        // Add more varieties if needed
    };

    const trashTypeSelect = document.getElementById("trashType");
    const trashVarietySelect = document.getElementById("trashVariety");
    const trashWeightInput = document.getElementById("trashWeight");
    const addButton = document.getElementById("addButton");
    const donationList = document.getElementById("donationItems");
    const totalPriceSpan = document.getElementById("totalPrice");
    let totalPrice = 0;

    // Populate the variety dropdown based on the selected type
    trashTypeSelect.addEventListener("change", function() {
        const selectedType = this.value;
        trashVarietySelect.innerHTML = "";
        Object.keys(trashPrices[selectedType]).forEach(variety => {
            const option = document.createElement("option");
            option.value = variety;
            option.textContent = variety.charAt(0).toUpperCase() + variety.slice(1);
            trashVarietySelect.appendChild(option);
        });
    });

    // Add donated item to the list
    addButton.addEventListener("click", function() {
        const type = trashTypeSelect.value;
        const variety = trashVarietySelect.value;
        const weight = trashWeightInput.value;
        if (!type || !variety || !weight) {
            alert("Please fill in all fields.");
            return;
        }

        // Create form data object
        const formData = new FormData();
        formData.append('trashtype', type);
        formData.append('trashvariety', variety);
        formData.append('trashweight', weight);

        // Send POST request to Flask backend
        fetch('/donate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle response if needed
            console.log('Data successfully added:', data);
            // Refresh page or update UI as needed
            const totalPriceForItem = trashPrices[type][variety] * parseFloat(weight);
            const listItem = document.createElement("li");
            listItem.textContent = `${variety} (${type}), Weight: ${weight} kg, Price: $${totalPriceForItem.toFixed(2)}`;
            donationList.appendChild(listItem);
            totalPrice += totalPriceForItem;
            totalPriceSpan.textContent = totalPrice.toFixed(2);
        })
        .catch(error => {
            console.error('Error adding data:', error);
            // Handle error, show alert, etc.
        });
    });
         // Add donated item to the list
         addButton.addEventListener("click", function() {
            const type = trashTypeSelect.value;
            const variety = trashVarietySelect.value;
            const pricePerKilo = trashPrices[type][variety];
            const donatedWeight = parseFloat(trashWeightInput.value);
            if (isNaN(donatedWeight) || donatedWeight <= 0) {
                alert("Please enter a valid weight.");
                return;
            }
            const totalPriceForItem = pricePerKilo * donatedWeight;
            const listItem = document.createElement("li");
            listItem.textContent = `${variety} (${type}), Weight: ${donatedWeight} kg, Price: $${totalPriceForItem.toFixed(2)}`;
            donationList.appendChild(listItem);
            totalPrice += totalPriceForItem;
            totalPriceSpan.textContent = totalPrice.toFixed(2);
        });
});