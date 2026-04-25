const express = require('express');
const axios   = require('axios');
const path    = require('path');
const app     = express();

app.use(express.json({ limit: '5mb' }));
app.use(express.static(path.join(__dirname, 'public')));    

// Receive image from frontend
// Forward to FastAPI ML server
app.post('/detect', async (req, res) => {
    try {

        const response = await axios.post('http://localhost:8000/predict', {
            image: req.body.image
        });


        res.json({ 
            result: response.data.result,
            confidence: response.data.confidence
         });

    } catch (err) {
        res.status(500).json({ result: "Detection failed" });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/test', (req, res) => {
    res.send('Server is working!')
});

app.listen(4000, () => {
    console.log('Node.js running on port 4000')
});