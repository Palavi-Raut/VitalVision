require('dotenv').config(); // Load environment variables

const express = require('express');
const mongoose = require('mongoose');

const app = express();
const PORT = process.env.PORT || 3002; // Define PORT before using it

mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log("Connected to MongoDB");
}).catch((err) => {
    console.error("MongoDB Connection Error:", err);
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});