const video = document.getElementById('video');

const constraints = {
  video: {
    facingMode: { ideal: "environment" } 
  }
};

navigator.mediaDevices.getUserMedia(constraints)
  .then(stream => {
    video.srcObject = stream;
    const track = stream.getVideoTracks()[0]; 
    const imageCapture = new ImageCapture(track);  

   
    const fastCapture = () => {
      imageCapture.takePhoto()
        .then(blob => {
          const formData = new FormData();
          formData.append('image', blob, 'snapshot.jpg');

      
          fetch('/upload', {
            method: 'POST',
            body: formData
          }).then(() => {
            
            requestAnimationFrame(fastCapture);
          });
        })
        .catch(console.error);
    };

  
    fastCapture();
  })
  .catch(err => console.error('Camera access denied:', err));  
