// Function to trigger PDF generation and download
function generateReceipt() {
    // Make a GET request to the server to generate PDF
    fetch('/generate_pdf')
        .then(response => response.blob())
        .then(blob => {
            // Create a blob URL for the PDF
            const url = window.URL.createObjectURL(new Blob([blob]));
            // Create a link element to trigger the download
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'receipt.pdf');
            // Append the link to the document body and trigger the download
            document.body.appendChild(link);
            link.click();
            // Cleanup: remove the link and revoke the blob URL
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        });
}