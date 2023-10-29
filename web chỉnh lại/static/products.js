const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const toggleCameraButton = document.getElementById("toggle-camera");
const toggleUploadButton = document.getElementById("toggle-upload");
const cameraContainer = document.getElementById("camera-container");
const cameraView = document.getElementById("camera-view");
const capturedPhoto = document.getElementById("captured-photo");
const uploadSection = document.querySelector(".upload");
const takePhotoButton = document.getElementById("take-photo");
const capturedImageData = document.getElementById("captured-image-data"); // Add this line

let mediaStream; // Variable to store the camera stream
let photoCaptured = false; // Variable to track if a photo is captured

// Initially hide the camera container and "Tải ảnh" button
cameraContainer.style.display = "none";
toggleUploadButton.style.display = "none";

let cameraActive = false;

// Function to clear the uploaded image
function clearUploadedImage() {
  imageView.innerHTML = `
    <img src="iconupload.png">
    <p>Kéo và thả hoặc bấm vào đây<br>để tải ảnh lên</p>
    <span>Tải bất kì ảnh từ thiết bị</span>
  `;
}

toggleCameraButton.addEventListener("click", function () {
  if (!cameraActive) {
    // Request camera permission
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        // Start the camera feed
        cameraView.srcObject = stream;
        mediaStream = stream; // Store the camera stream
        cameraActive = true;

        // Toggle button visibility
        toggleCameraButton.style.display = "none";
        toggleUploadButton.style.display = "inline"; // Correct the property name

        // Hide the upload section
        uploadSection.style.display = "none";

        // Show the camera view or the captured photo
        if (photoCaptured) {
          capturedPhoto.style.display = "block";
          cameraView.style.display = "block"; // Show the camera view
        } else {
          cameraView.style.display = "block";
        }

        // Show the camera container
        cameraContainer.style.display = "flex";
      })
      .catch((error) => {
        console.error('Error accessing the camera:', error);
      });
  } else {
    // Stop the camera feed
    mediaStream.getTracks().forEach((track) => track.stop());
    cameraActive = false;

    // Toggle button visibility
    toggleCameraButton.style.display = "inline";
    toggleUploadButton.style.display = "none";

    // Hide the camera container
    cameraContainer.style.display = "none";
  }
});

toggleUploadButton.addEventListener("click", function () {
  // Clear the captured image
  clearUploadedImage();
  // Reset the input file element to clear the selected file
  inputFile.value = ""; // This line resets the input element

  capturedPhoto.src = "";
  capturedPhoto.style.display = "none";
  photoCaptured = false;

  // Switch back to the upload section and stop the camera when the "Tải ảnh" button is clicked
  cameraContainer.style.display = "none";
  uploadSection.style.display = "flex";

  // Stop the camera feed
  if (cameraActive) {
    mediaStream.getTracks().forEach((track) => track.stop());
    cameraActive = false;
  }

  // Toggle button visibility
  toggleCameraButton.style.display = "inline";
  toggleUploadButton.style.display = "none";
});

inputFile.addEventListener("change", uploadImage);

function uploadImage() {
  let imgLink = URL.createObjectURL(inputFile.files[0]);
  imageView.innerHTML = `<img src="${imgLink}">`;
  capturedImageData.value = imgLink; // Add this line to save the captured image data
}

takePhotoButton.addEventListener('click', function () {
  if (!photoCaptured) {
    if (cameraActive) {
      // Create a canvas to capture the image
      const canvas = document.createElement('canvas');
      canvas.width = cameraView.videoWidth;
      canvas.height = cameraView.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(cameraView, 0, 0, canvas.width, canvas.height);

      // Set the captured image as the source for the img element
      capturedPhoto.src = canvas.toDataURL('image/jpeg');
      capturedImageData.value = capturedPhoto.src; // Add this line to save the captured image data

      // Display the captured image
      capturedPhoto.style.display = "block";

      // Hide the camera view
      cameraView.style.display = "none";
      photoCaptured = true;
    }
  } else {
    // Clear the captured image
    capturedPhoto.src = "";
    capturedPhoto.style.display = "none";
    cameraView.style.display = "block";
    photoCaptured = false;
  }
});

dropArea.addEventListener("dragover", function (e) {
  e.preventDefault();
});

dropArea.addEventListener("drop", function (e) {
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage();
});


