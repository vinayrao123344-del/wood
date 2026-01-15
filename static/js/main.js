document.addEventListener('DOMContentLoaded', () => {

    // Dynamic Subtype Loading for Calculator
    const woodTypeSelect = document.getElementById('wood_type');
    const subtypeSelect = document.getElementById('wood_subtype');

    if (woodTypeSelect) {
        woodTypeSelect.addEventListener('change', async (e) => {
            const typeId = e.target.value;
            subtypeSelect.innerHTML = '<option value="">Loading...</option>';
            subtypeSelect.disabled = true;

            if (!typeId) {
                subtypeSelect.innerHTML = '<option value="">First Select Wood Type</option>';
                return;
            }

            try {
                const response = await fetch(`/get_subtypes/${typeId}`);
                const subtypes = await response.json();

                subtypeSelect.innerHTML = '<option value="">Select Sub-type</option>';
                subtypes.forEach(subtype => {
                    const option = document.createElement('option');
                    option.value = subtype.id;
                    option.textContent = `${subtype.name} (₹${subtype.price_per_sqft}/sqft)`;
                    subtypeSelect.appendChild(option);
                });
                subtypeSelect.disabled = false;
            } catch (error) {
                console.error('Error fetching subtypes:', error);
                subtypeSelect.innerHTML = '<option value="">Error loading</option>';
            }
        });
    }

    // Calculator Form Submission
    const calculatorForm = document.getElementById('calculatorForm');
    const resultBox = document.getElementById('resultBox');

    if (calculatorForm) {
        calculatorForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                width: parseFloat(document.getElementById('width').value),
                height: parseFloat(document.getElementById('height').value),
                subtype_id: document.getElementById('wood_subtype').value
            };

            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('res_area').textContent = `${data.area} sqft`;
                    document.getElementById('res_rate').textContent = `₹${data.wood_rate} /sqft`;
                    document.getElementById('res_wood_cost').textContent = `₹${data.wood_cost}`;
                    document.getElementById('res_labor_cost').textContent = `₹${data.labor_cost}`;
                    document.getElementById('res_total').textContent = `₹${data.total_cost}`;

                    resultBox.classList.remove('hidden');
                    // Smooth scroll to result
                    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } else {
                    alert(data.error || 'Calculation failed');
                }
            } catch (error) {
                console.error('Calculation error:', error);
                alert('An error occurred during calculation');
            }
        });
    }
});
