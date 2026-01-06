// Payment processing functionality for AaplaBazaar

document.addEventListener('DOMContentLoaded', function() {
    // Initialize payment form
    initPaymentForm();
    initPaymentMethodSwitcher();
    initUpiScanner();
});

// Initialize payment form handling
function initPaymentForm() {
    const checkoutForm = document.getElementById('checkout-form');
    
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            // Standard form submission handled by Flask
            // This can be enhanced with client-side validation
            
            // Validate required fields
            const requiredFields = checkoutForm.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                    
                    // Create or update validation message
                    let feedbackElement = field.nextElementSibling;
                    if (!feedbackElement || !feedbackElement.classList.contains('invalid-feedback')) {
                        feedbackElement = document.createElement('div');
                        feedbackElement.classList.add('invalid-feedback');
                        field.parentNode.insertBefore(feedbackElement, field.nextSibling);
                    }
                    
                    feedbackElement.textContent = 'This field is required.';
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                showFlashMessage('Please fill in all required fields.', 'danger');
                
                // Scroll to first invalid field
                const firstInvalid = checkoutForm.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            } else {
                // Show loading state
                const submitButton = checkoutForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = true;
                    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                }
            }
        });
        
        // Remove validation errors on input
        const formInputs = checkoutForm.querySelectorAll('input, textarea, select');
        formInputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    }
    
    // Add address autofill functionality
    const useProfileAddressCheckbox = document.getElementById('use-profile-address');
    if (useProfileAddressCheckbox) {
        useProfileAddressCheckbox.addEventListener('change', function() {
            const addressField = document.getElementById('shipping_address');
            const cityField = document.getElementById('shipping_city');
            const stateField = document.getElementById('shipping_state');
            const pincodeField = document.getElementById('shipping_pincode');
            
            if (this.checked) {
                // Use data attributes to get profile address
                addressField.value = this.getAttribute('data-address') || '';
                cityField.value = this.getAttribute('data-city') || '';
                stateField.value = this.getAttribute('data-state') || '';
                pincodeField.value = this.getAttribute('data-pincode') || '';
                
                // Remove any validation errors
                [addressField, cityField, stateField, pincodeField].forEach(field => {
                    field.classList.remove('is-invalid');
                });
            } else {
                // Clear fields
                addressField.value = '';
                cityField.value = '';
                stateField.value = '';
                pincodeField.value = '';
            }
        });
    }
}

// Toggle payment method specific UI
function initPaymentMethodSwitcher() {
    const paymentSelect = document.getElementById('payment_method');
    const codInfo = document.getElementById('cod-info');
    const upiSection = document.getElementById('upi-section');
    const upiInput = document.getElementById('upi_reference');

    if (!paymentSelect) return;

    const toggleSections = () => {
        const method = paymentSelect.value;
        const isUpi = method === 'upi';

        if (codInfo) codInfo.classList.toggle('d-none', isUpi);
        if (upiSection) upiSection.classList.toggle('d-none', !isUpi);
        
        // Make UPI ID mandatory only when UPI is chosen
        if (upiInput) {
            if (isUpi) {
                upiInput.setAttribute('required', 'required');
            } else {
                upiInput.removeAttribute('required');
                upiInput.classList.remove('is-invalid');
            }
        }
    };

    paymentSelect.addEventListener('change', toggleSections);
    toggleSections();
}

// Basic UPI QR scanning using html5-qrcode (graceful fallback when unavailable)
function initUpiScanner() {
    const scanButton = document.getElementById('start-upi-scan');
    const readerElement = document.getElementById('qr-reader');
    const resultElement = document.getElementById('qr-result');
    const upiInput = document.getElementById('upi_reference');

    if (!scanButton || !readerElement) return;

    let html5QrCode = null;
    let isScanning = false;

    const stopScanner = () => {
        if (html5QrCode) {
            html5QrCode.stop().then(() => {
                html5QrCode.clear();
            }).catch(() => {});
        }
        isScanning = false;
        readerElement.classList.add('d-none');
        scanButton.innerHTML = '<i class="fas fa-camera me-2"></i>Scan UPI QR';
    };

    const onScanSuccess = (decodedText) => {
        if (upiInput) {
            upiInput.value = extractUpiId(decodedText);
            upiInput.dispatchEvent(new Event('input'));
        }
        if (resultElement) {
            resultElement.textContent = `Scanned: ${decodedText}`;
        }
        stopScanner();
    };

    scanButton.addEventListener('click', () => {
        if (isScanning) {
            stopScanner();
            return;
        }

        if (typeof Html5Qrcode === 'undefined') {
            alert('QR scanning is not supported on this device/browser.');
            return;
        }

        html5QrCode = new Html5Qrcode(readerElement.id);
        readerElement.classList.remove('d-none');
        scanButton.innerHTML = '<i class="fas fa-stop me-2"></i>Stop Scan';

        html5QrCode.start(
            { facingMode: 'environment' },
            { fps: 10, qrbox: 250 },
            onScanSuccess,
            () => {}
        ).then(() => {
            isScanning = true;
        }).catch(() => {
            stopScanner();
            alert('Unable to access camera for scanning.');
        });
    });
}

// Extract VPA/UPI ID from decoded QR text
function extractUpiId(decodedText) {
    try {
        const url = new URL(decodedText);
        const vpa = url.searchParams.get('pa');
        if (vpa) return vpa;
    } catch (e) {
        // Not a valid URL, fall back to raw text
    }
    return decodedText;
}

// Handle payment success response
function handlePaymentSuccess(sessionId) {
    // Show success message
    showFlashMessage('Payment successful! Your order has been placed.', 'success');
    
    // Redirect to order confirmation page
    setTimeout(() => {
        window.location.href = `/order/confirmation/${sessionId}`;
    }, 1500);
}

// Handle payment error response
function handlePaymentError(errorMessage) {
    // Show error message
    showFlashMessage(errorMessage || 'Payment processing failed. Please try again.', 'danger');
    
    // Enable submit button again
    const submitButton = document.querySelector('#checkout-form button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Place Order';
    }
}
