
document.addEventListener('DOMContentLoaded', function() {
    const isGiftCheckbox = document.getElementById('is_gift');
    const giftOptionsDiv = document.getElementById('giftOptions');
    const giftWrapSelect = document.getElementById('gift_wrap_type');
    
    if (isGiftCheckbox && giftOptionsDiv) {
        isGiftCheckbox.addEventListener('change', function() {
            giftOptionsDiv.style.display = this.checked ? 'block' : 'none';
        });
    }

    // Update total when gift wrap option changes
    if (giftWrapSelect) {
        giftWrapSelect.addEventListener('change', function() {
            let additionalCost = 0;
            switch(this.value) {
                case 'basic':
                    additionalCost = 50;
                    break;
                case 'premium':
                    additionalCost = 100;
                    break;
                case 'luxury':
                    additionalCost = 200;
                    break;
            }
            
            // Update displayed total
            const totalElement = document.querySelector('.checkout-total span:last-child');
            if (totalElement) {
                let baseTotal = parseFloat(totalElement.getAttribute('data-base-total'));
                if (isNaN(baseTotal)) {
                    // Fallback if data attribute is missing
                    baseTotal = parseFloat(totalElement.textContent.replace(/[^\d.]/g, '')) || 0;
                    totalElement.setAttribute('data-base-total', baseTotal.toString());
                }
                const newTotal = baseTotal + additionalCost;
                totalElement.textContent = '₹' + newTotal;
                document.dispatchEvent(new CustomEvent('checkout:totalUpdated', { detail: { total: newTotal } }));
            }
        });
    }
});
