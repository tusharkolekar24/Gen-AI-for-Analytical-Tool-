function toggleSidebar() {
    const sidebar = document.querySelector('.sidenav');
    sidebar.classList.toggle('toggled');
    document.querySelector('.content').classList.toggle('toggled');
}       
const config = {
            displaylogo: false,
            modeBarButtonsToRemove: [
                'resetAxes', 'spikelines', 'zoomIn2d', 'zoomOut2d',
                'zoom2d', 'pan2d', 'select2d'
            ]
        };

document.querySelector('.dropdown-button').addEventListener('click', function() {
    var formContainer = this.nextElementSibling;
        if (formContainer.style.display === 'block') {
            formContainer.style.display = 'none';
        } else {
            formContainer.style.display = 'block';
        }
});


const fileInput = document.getElementById("fileUpload");
const fileNameText = document.getElementById("fileName");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      fileNameText.textContent = fileInput.files[0].name;
      document.getElementById("uploadForm").submit();  // Automatically send to Flask
    }
});