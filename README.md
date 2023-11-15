# Coconut-Mature-Classification
This repository hosts an AI-based system for accurately classifying the maturity of coconuts (young, mature, old) by utilizing computer vision techniques to make accurate maturity assessments based on coconut images.

# Table of Contents
* Motivation
* Web Application
* Dataset
* Installation
* Usage
* Training
* Evaluation
* Results
* Limits
* Contributions

# Motivation
### Background
* Coconut farming and its related industries play a crucial role in many tropical regions
* Ensuring the quality of coconuts at different maturity stages is essential for both farmers and downstream industries
* Currently, the assessment of coconut maturity relies heavily on manual labor making it a time-consuming and often subjective process.
    
### Pain point
* The traditional method of assessing coconut maturity is fraught with challenges and pain points:
  * Subjectivity,
  * Labor-intensive,
  * Time-consuming,
  * Resource drain.
* The pain point lies in the need for a more efficient, objective, and accurate method to assess coconut maturity.
    
### Objective
* Develop a computer vision-based system for coconut age classification
* Implement machine learning algorithms for image analysis and classification
* Enhance the accuracy and speed of coconut quality assessment 
* Facilitate decision-making in coconut processing industries
* Reduce human labor and error in coconut quality assessment.

# Web Application

### Diagram
![diagram](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/121301557/63fd97c7-3290-44f0-a91e-ee75a751e360)

      
# Dataset
Link dataset: https://drive.google.com/drive/folders/1IoUpBAI8BWnbe_s-eyFtMbCO16AEHO8b?usp=sharing
Dataset description:
* Original data:
    * Dừa non: 407
    * Dừa nạo: 1142
    * Dừa già: 1024
    * Khác: 1061
### Data Preprocessing
* Crop image: Crop all images in the dataset into squares
* Data augmentation with 'young coconut' class
* Run file: ``` DataAugmentation.py ```
------------------------------------
    transforms.RandomHorizontalFlip(): Apply random horizontal flip to the image with a default probability of 0.5
    transforms.RandomRotation(10): Apply random rotation to the image with a rotation range of ±10 degrees
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)): Apply random resized crop to the image, resizing it to 224x224, with a scale factor between 0.8 and 1.0
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)): Apply random affine transformation to the image with a rotation range of 0 degrees and translation of 0.1 in both directions
    transforms.RandomPerspective(distortion_scale=0.2, p=0.5): Apply random perspective transformation to the image with a distortion scale of 0.2 and a probability of 0.5

### Data Distribution visualization:

![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/88047081/d53e6bf2-72cb-4d99-99fd-f7f4241c7c48)

### Data Splitting
* Run file: ``` DataSplit.py ```
![image](https://github.com/TruongTrongTien/Coconut-Mature-Classification/assets/88047081/f92cd668-38c5-45be-9a97-2436b01308dc)


# Installation

Follow these steps to install and run the project on your local machine.
### Prerequisites
Make sure you have the following prerequisites installed on your system:
- [Python](https://www.python.org/) (version 3.9 or later)
- [pip](https://pip.pypa.io/en/stable/)
### Clone the Repository
```bash
git clone https://github.com/TruongTrongTien/Coconut-Mature-Classification.git
cd Coconut-Mature-Classification
```

### Set up a Virtual Environment
Create a virtual environment to isolate project dependencies:
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows:
```bash
.\venv\Scripts\activate
```

- On UNIX or MacOS:
```bash
source venv/bin/activate
```

### Install Dependencies 
```bash
pip install -r requirements.txt
```

# Usage

### Run the Application
```bash
flask run
```

# Training
# Evaluation
# Results
# Limits
# Contributions
