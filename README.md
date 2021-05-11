# Brain Tumor Detection

## Project Status
This project is currently under development. Users can upload an image file of a Brain MRI. Once the image is submitted, the app will detect whether the patient has a brain tumor. The dataset was taken from: (https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection)[https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection]

## Installation and Setup Instructions

In the 'frontend' directory, you can run:

### `npm install`
Installs the required node modules.

### `npm start`
Runs the app in the development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

In the 'backend' directory, you can run:

### `python api.py`
Runs the Flask app

## Project Structure
```
├── node_modules (.gitignore)
├── public
│   ├── favicon.ico
│   ├── index.html
│   ├── robots.txt
│   └── manifest.json
├── src
│   ├── assets
│   ├── components
│   │   ├── CheckoutForm
│   │   ├── Firebase
│   │       └── Firebase.js     // Holds Firebase Configuration
│   ├── pages
│   │   ├── Home
│   │       ├── Home.css
│   │       └── Home.js
│   ├── App.css
│   ├── App.js
│   ├── App.test.js
│   ├── index.css
│   ├── index.js
│   ├── reportWebVitals.js
│   └── setupTests.js
├── .gitignore
├── .firebaserc
├── package.json
├── package-lock.json
└── README.md
```
## Future Development
- Increase ML model accuracy
- Show confidence percentage of model
- Deploy app/api to a hosting platform