# Brain Tumor Detection

## Project Status
This project is currently under development. Users can upload an image file of a Brain MRI. Once the image is submitted, the app will detect whether the patient has a brain tumor. The dataset was taken from: [Kaggle](https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection). The model performs with an accuracy of 95%+. 

This app is hosted with Firebase Hosting at [Brain Tumor Detection App](https://brain-tumor-detection-aa187.web.app). The api must be run in the backend directory using `python3 api.py`.

## Installation and Setup Instructions

In the 'frontend' directory, you can run:

#### `npm install`
Installs the required node modules.

#### `npm start`
Runs the app in the development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

#### `npm run build`
Creates optimize production build

#### `firebase deploy`
Deploys app to [https://brain-tumor-detection-aa187.web.app](https://brain-tumor-detection-aa187.web.app).

In the 'backend' directory, you can run:

#### `python3.8 api.py`
Runs the Flask app

## Project Structure
```
├── .gitignore
├── model_training.py // trains model on dataset and outputs .h5 file
├── brain_tumor_dataset
    ├── Normal
    ├── Tumor
├── backend
    ├── api.py // Run this file
    ├── trained_model.h5 // Holds ML model
    ├── requirements.txt
    ├── Procfile
    ├── uploaded_image.png
├── frontend
    ├── node_modules (.gitignore)
    ├── public
    ├── src
    │   ├── assets
    │   ├── components
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
    ├── .firebaserc
    ├── package.json
    ├── package-lock.json
    └── README.md
```
## Future Development
- Deploy api to a hosting platform
