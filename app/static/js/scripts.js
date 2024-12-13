const form = document.getElementById('pdfForm');
const fileInput = document.getElementById('file');
const fileName = document.getElementById('fileName');
const notification = document.getElementById('notification');
const notificationMessage = document.getElementById('notificationMessage');
const notificationClose = document.getElementById('notificationClose');

fileInput.addEventListener('change', (e) => {
    fileName.textContent = fileInput.files[0] ? fileInput.files[0].name : "Choose a file";
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    showNotification("Processing your request...", "border-blue-500");

    const formData = new FormData(form);
    try {
        const response = await fetch('/api/v1/compress', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (result.status === "success") {
            showNotification(result.message, "border-green-500");
            const link = document.createElement('a');
            link.href = result.download_url;
            link.download = '';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            showNotification(result.message, "border-red-500");
        }
    } catch (error) {
        showNotification("An error occurred. Please try again!", "border-red-500");
    }

    notificationClose.addEventListener('click', () => {
        notification.classList.remove('active');
    });

    function showNotification(message, borderClass) {
        notificationMessage.textContent = message;
        notification.className = `flex items-center p-4 bg-white shadow-lg rounded-lg active ${borderClass}`;
    }
});