# AGRI ASSISTANCE: An intelligent Machine Learning approach towards Crop Recommendation and Weed Detection

## Visit https://github.com/SureshKrishnaaR/Crop-Recommendation-Weed-Detection-Frontend for Frontend

## DESKTOP INTERFACE

### Requirements

❖ Browser - Chrome/Opera/Safari/Edge  
❖ Camera  
❖ Browser Navigator (Location Access)

### Application Demo

![alt text](https://github.com/vishwa-jith/Crop-recommendation-Weed-detection/blob/master/docs/DESKTOPUI.gif?raw=true)

## MOBILE INTERFACE

### Requirements

❖ Browser - Chrome/Opera/Safari/Edge  
❖ Camera  
❖ Browser Navigator (Location Access)

### Application Demo

![alt text](https://github.com/vishwa-jith/Crop-recommendation-Weed-detection/blob/master/docs/MOBILEUI.gif?raw=true)

## Dataset Collections

| <b>Discipline             | <b> Dataset Link                                                                          |
| :------------------------ | :---------------------------------------------------------------------------------------- |
| <b> Crop Recommendation   | <b> https://www.kaggle.com/atharvaingle/crop-recommendation-dataset                       |
| <b> Crop Yield            | <b> https://www.kaggle.com/ananysharma/crop-yield                                         |
| <b> Fertilizer Prediction | <b> https://www.kaggle.com/gdabhishek/fertilizer-prediction                               |
| <b> Weed Detection        | <b> https://www.kaggle.com/ravirajsinh45/crop-and-weed-detection-data-with-bounding-boxes |

## 3rd Party API's

### Weather API

Real-time or current JSON weather and XML weather API provides access to near real-time weather information for millions of locations worldwide.

Use below link to access API via API key.  
https://www.weatherapi.com/

## Steps to start the Application (Backend)

```
git clone https://github.com/vishwa-jith/Crop-recommendation-Weed-detection.git
```

**Creating and Activating Virtual Environment**

```
pip install virtualenv

# or

pip install venv
```

**Setup Virtual Environment**

```
python -m venv env
```

**Activate Virtual Environment**

```
# activate env (windows)

.\env\scripts\activate

# activate env (Linux/Mac)

source env/bin/activate
```

**Installing Dependencies**

```
pip install -r requirements.txt
```

**Creating database DB (SQLite)**

```
py do_clean.py

# or

python do_clean.py
```

**Starting Application**

```
flask_app.py
```

**Deactivating Virtual Environment**

```
deactivate env
```

Visit http://localhost:5000 or http://0.0.0.0:5000 or http://yourIp:5000

## Access Permissions Required

No permissions required

## Tools and Technologies Used

Code Editor - VS Code  
Analytical IDE - Jupyter Notebook  
Continuous Integration - GitHub  
Deployment - Heroku

## Software Requirements

❖ Python @3.8 (only acceptable till 3.8 --version)  
❖ Nodejs  
❖ npm (Node Package Manager)  
❖ Git Bash

## Other Requirements

❖ virtualenv (python)  
❖ create-react-app (npm)

## Dependencies

matplotlib==3.3.4  
numpy==1.19.5  
opencv-python==4.5.1.48  
pandas  
seaborn==0.11.1  
sklearn==0.0  
tensorflow==2.4.1  
tqdm==4.57.0  
Flask_SQLAlchemy==2.4.4  
requests==2.25.1  
Flask==1.1.2  
geocoder==1.38.1  
Werkzeug==1.0.1  
PyJWT==1.7.1  
gunicorn==20.1.0

## Objective

❖ It is very essential for the farmers to choose a crop that best suits the land being used for cultivation. Farmers should get benefited by cultivating the **best fitting crops** rather than cultivating unsuitable crops.

❖ The objective of this project is to develop a system that would be useful for farmers in order to **predict the suitable crop, fertilizer, and crop yield**.

❖ **Weeds** results in **yield reduction**. We are using **Image processing** and **Deep learning** techniques which would extract the features that can distinguish between crop leaves and weed leaves.

## Problem Statement

❖ The common difficulty present among the Indian farmers is, they don’t opt for the **proper crop** based on their soil requirements. Due to this, they face a serious **setback in productivity**.

❖ Choosing **incorrect decisions** would lead to crop failure, and this would result in a complete loss to farmers.

❖ **Weeds** are the plants growing in the wrong place which competes with crops for water, light, nutrients, and space, causing **reduction in yield**. And in order to **remove weeds**, farmers started using **deadly poisons** as herbicides. By doing so they had success in increasing productivity but they’ve forgotten the **damage done to the environment**.

## Why do we need this system?

❖ A single **misguided or incorrect decision** taken by a novice farmer can have undesirable consequences contributing to the **countless suicide cases** of farmers that we hear from media on a daily basis.

❖ A right decision in the **selection of crops** to be grown will ultimately result in a **successful farming** venture.
Total **economic loss** of about USD 11 billion was estimated **due to weeds** alone in 10 major field crops in 18 states of India. So, the control of weeds is of vital importance in agriculture.

## Literature Survey

| **S.** |                                         **Title**                                         |                    **Author** | **Journal, Year**                                                                                                               |                                                                                                                                                **Methodology Used**                                                                                                                                                |
| :----- | :---------------------------------------------------------------------------------------: | ----------------------------: | :------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| 1      | Agro Consultant: Intelligent Crop Recommendation System Using Machine Learning Algorithms |            Zeel Doshi,et al., | 25 April 2019 Fourth International conference on Computing Communication Control and Automation (ICCUBEA)                       |                                          To eliminate the aforementioned drawbacks, we propose Agro Consultant- which takes into consideration all the appropriate parameters, including temperature, rainfall, location and soil condition, to predict crop suitability.                                          |
| 2      | Crop Recommendation System through Soil Analysis Using Classification in Machine Learning |   Dr. A. K. Mariappan,et al., | IEEE Access, Vol. 29, 2020                                                                                                      |                                                                                                        The proposed system obtains the soil and crop parameters and maps those to list the suitable crops.                                                                                                         |
| 3      |                    Crop Recommendation and Fertilizer Purchase System                     |         Mansi Shinde, et al., | Mansi Shinde et al, / (IJCSIT) International Journal of Computer Science and Information Technologies, Vol. 7 (2) , 2016.       |                                            This paper summarizes an efficient recommendation system for fertilizers and crops based on the NPK values and region. This application also allows users to purchase the recommended fertilizers from the purchase portal.                                             |
| 4      |                 AGRIGRASS: Precision Farming for Weed Detection & Control                 | Margesh M. Ambilwade, et al., | International Journal of Future Generation Communication and Networking Vol. 13, No. 3s, (2020)                                 |                                                               In this system, Feature Extraction is done using CNN. Features such as color, shape, size of a particular weed are extracted and then weed classification is done using KNN algorithm.                                                               |
| 5      |                            Image Processing for Weed Detection                            |       R.Anirudh Reddy,et al., | International Journal of Engineering Technology, Management and Applied Sciences, April 2017, Volume 5, Issue 4, ISSN 2349-4476 |      This paper introduces the system implementation of image processing technique for weed detection and removal. It involves simple edge detection technique using various filters such as Gaussian and Laplacian. It finally concludes with the feature extraction, results that implement ORB algorithm.       |
| 6      |    Crop Recommendation System to Maximize Crop Yield using Machine Learning Technique     |     Rohit Kumar Rajak,et al., | International Research Journal of Engineering and Technology (IRJET) Volume: 04 Issue: 12, Dec-2017                             | In this paper, the data from soil testing lab is given to the recommendation system it will use the collected data and do ensemble model with majority voting technique using support vector machine (SVM) and ANN as learners, to recommend a crop for site specific parameter with high accuracy and efficiency. |

## Proposed System Methodology

### CROP RECOMMENDATION

To predict the most suitable crop, we use two different approaches,

**Approach 1**

**Step 1**:

**Process** - Recommend a **crop** considering the environmental factors such as **temperature**, **humidity** and **rainfall** (predicted using **Weather API**).  
**Algorithm** - Random Forest (Classification).  
**Reason** - RF is an ensemble classifier, which is a most effective algorithm as it uses bagging approach to solve the problem.  
**Accuracy Score** - 95.83%

**Step 2**:

**Process** - Predict the ideal NPK values based on environmental factors and previously predicted crop.  
**Algorithm** - Gradient Boosting Regressor  
**Reason** - GBR uses weak learners as classifiers, and they learn from their previous mistakes.

**Step 3**:

**Process** - Recommend a fertilizer based on the environmental factors, soil type and crop type.  
**Algorithm** - Support Vector Machines  
**Reason** - SVM will have higher accuracy when we have many features(high dimensional spaces).  
**Accuracy Score** - 97.5%

### CROP RECOMMENDATION

**Approach 2**

**Step 1**:

Collect the NPK values from the farmer.

**Step 2**:

**Process** - Predict a best suitable crop based on the NPK values and environmental factors(temperature, humidity, rainfall).  
**Algorithm** - Random Forest  
**Reason** - Random Forest uses ensemble approach, so it has a very good accuracy compared to other algorithms.  
**Accuracy Score** - 98.33%

## CROP YIELD / PRODUCTION

❖ We also predict the **amount of crop** that the farmer can cultivate, this prediction is based on the **farmer’s location, seasonal changes, crop type and the amount of area** used for cultivation.

❖ This prediction would help to take fair and **correct decisions** which would make their **yield more productive**.

❖ So based on this the farmer can decide whether to go ahead with the chosen crop or to choose a different crop.

❖ And here we use **SGD - Stochastic Gradient Descent Algorithm** to predict the value of **crop yield** and this regression analysis is based on **crop** **type**, **location**, **area**and **season**.

## CROP - WEED DETECTION

❖ Weed detection is very much helpful for farmers for boosting their annual production.

❖ In this project, we use OpenCV image processing techniques which does the following operations,

❖ Then we use a deep learning model, which has multiple layers to progressively extract high-level features from the input image, and using these features crop-weed classification is carried out.

## Architecture

![alt text](https://github.com/vishwa-jith/Crop-recommendation-Weed-detection/blob/master/docs/flow-img1.png?raw=true)

![alt text](https://github.com/vishwa-jith/Crop-recommendation-Weed-detection/blob/master/docs/flow-img2.png?raw=true)

## References

[1] Z. Doshi, S. Nadkarni, R. Agrawal and N. Shah, "Agro Consultant: Intelligent Crop Recommendation System Using Machine Learning Algorithms," 2018 Fourth International Conference on Computing Communication Control and Automation (ICCUBEA), Pune, India, 2018, pp. 1-6, doi:10.1109/ICCUBEA.2018.8697349.

[2] Dr. A. K. Mariappan, Ms. C. Madhumitha, Ms. P. Nishitha, Ms. S. Nivedhitha, “Crop Recommendation System through Soil Analysis Using Classification in Machine Learning”, IJAST, vol. 29, no. 3, pp. 12738 - 12747, Mar. 2020.

[3] Mansi Shinde, Kimaya Ekbote, Sonali Ghorpade, Sanket Pawar, Shubhada Mone, “Crop Recommendation and Fertilizer Purchase System”, IJAST, vol. 7, no. 2, pp. 665-667, 2016.

[4] Margesh M. Ambilwade, Aumkar A. Deshpande, Rucha K. Ugemuge, Pooja N. Vengurlekar “AGRI GRASS: Precision Farming for Weed Detection & Control”, International Journal of Future Generation Communication and Networking Vol. 13, No. 3s, (2020), pp. 121–127.

[5] R.Anirudh Reddy, G.Laasya, T.Sowmya, P.Sindhuja, Mudasar Basha, “Image Processing For Weed Detection”, International Journal of Engineering Technology, Management and Applied Sciences, April 2017, Volume 5, Issue 4, ISSN 2349-4476.

[6] Rohit Kumar Rajak, Ankit Pawar, Mitalee Pendke, Pooja Shinde, Suresh Rathod, Avinash Devare, ”Crop Recommendation System to Maximize Crop Yield using Machine Learning Technique”, International Research Journal of Engineering and Technology (IRJET), Volume: 04 Issue: 12 | Dec-2017.

## Developer Information

| <b>Name of Developer | <b> Vishwajith V                   |
| :------------------- | :--------------------------------- |
| <b> Institute        | <b> Sri Sairam Engineering College |
| <b> Email id         | <b> vishwajith567@gmail.com        |
| <b> Department       | Computer Science Engineering       |

| <b>Name of Developer | <b> Suresh Krishnaa R              |
| :------------------- | :--------------------------------- |
| <b> Institute        | <b> Sri Sairam Engineering College |
| <b> Email id         | <b> shyrams1346@gmail.com          |
| <b> Department       | Computer Science Engineering       |
