# Podium.ai

*An AI Model to predict F1 Race Results with an interactive user interface*

---

### WEBSITE
You can find the website hosted [here.](https://podiumai.up.railway.app/alt)  
It consists of an interactive UI to query results from the model based on the latest grand prix
or the upcoming one.  

*Functionality to view past races predictions and explore performance by model will be added soon*

---

### REPO STRUCTURE
* Predictor: Consists of real data pre-processing and prediction scripts,
                as well as relevant models and label encoders.
* Scraper: Consists of scripts to query latest qualiyfing data from 
           the official F1 website along with relevant calendar and circuit data
* Static: Consists of static elements (JavaScript, HTML, Images) for the frontend
* Templates: Contains views for the site
* Training: Consists of all the training scripts used to create the models as well as datasets
            from FastF1 API.

*See app.py to check out how the Flask server is setup to query data*

---

### MODELS
Currently, only one model is supported but more models will be added 
based on differing training features as well as architecture.  
*Model Alpha* is an LGBM Regressor Model from the Scikit-learn library.
Check out the features used to train it in the Training directory.