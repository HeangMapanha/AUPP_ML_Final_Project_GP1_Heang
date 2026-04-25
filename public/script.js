// # something something


// # Dataset taken from Trashnet
// # Refine Dataset and Augment
// # Build ML model using CNN feature + Boost + Decision Tree + Random Forest + Linear Regression + Soft voting
// # Testing model
// # Build API for implementation
// # 


const video = document.getElementById("video");
const buttoncamera = document.getElementById("startcamera");
stream = null;

async function startCamera(){
    try {
        const constraints = {
            video: {
                facingMode: "environment"
            }
        };
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
    
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