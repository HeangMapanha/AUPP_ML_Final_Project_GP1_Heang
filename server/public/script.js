// # something something


// # Dataset taken from Trashnet
// # Refine Dataset and Augment
// # Build ML model using CNN feature + Boost + Decision Tree + Random Forest + Linear Regression + Soft voting
// # Testing model
// # Build API for implementation
// # 


const video = document.getElementById("video");
const buttoncamera = document.getElementById("startcamera");
const canvas = document.getElementById("canvas")
const result = document.getElementById("result")

stream = null;
isProcessing = false;
detectionLoop = null;


async function startCamera(){
    try {
        const constraints = {
            video: {
                facingMode: "environment"
            }
        };
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;

        video.onloadedmetadata = () => {
            startDetection();
    };
    
    } catch (err) {
        console.error("Camera error", err);
        alert("Could not access Camera");
    }

}

function stopCamera() {
    if(stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        stream = null;
    }
    stopDetection();
}

function startDetection() {
    detectionLoop = setInterval(async () => {
        if (isProcessing) return;      

        isProcessing = true;
        await captureAndSend();      
        isProcessing = false;

    }, 2000);                       
}

function stopDetection() {
    if (detectionLoop) {
        clearInterval(detectionLoop);
        detectionLoop = null;
        result.textContent = "No detection yet";
    }
}

async function captureAndSend() {
    // Set canvas size to match video
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame onto canvas
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    // Convert to base64 image — compressed to 50% quality
    const imageData = canvas.toDataURL("image/jpeg", 0.5);

    try {
        // Send to your Node.js backend
        const response = await fetch("/detect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();

        // Show result
        result.textContent = `${data.result} — ${data.confidence}%`;

    } catch (err) {
        console.error("Detection error", err);
        result.textContent = "Detection failed";
    }
}

buttoncamera.addEventListener("click",() => {
    if (!stream) {
        startCamera();
        buttoncamera.textContent = "Stop Camera";

    } else {
        stopCamera();
        buttoncamera.textContent = "Start Camera";
    }
});