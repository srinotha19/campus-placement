from flask import Flask, render_template, request
import pickle
import numpy as np

# import os
# os.getcwd
# os.chdir('D:\CBIT_EEE_CampusPlacement_Prediction-main\placement.csv')


model = pickle.load(open('campusplacementpredictor.pkl', 'rb'))

app = Flask(__name__)


def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 4)
    loaded_model = pickle.load(open("campusplacementpredictor.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

def ProbPredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 4)
    loaded_model = pickle.load(open("campusplacementpredictor.pkl", "rb"))
    probability = loaded_model.predict_proba(to_predict)[:,-1]
    return probability

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)  
        if int(result)== 1:
            prediction ='Chance Is There To Be Placed'

        else:
            prediction ='Need to work harder! Try Again'
        probability = np.round(ProbPredictor(to_predict_list),4)
        return render_template("placementanalysis.html", prediction = prediction ,probability=probability*100)




        



@app.route('/')
def man():
    return render_template('placementanalysis.html')




if __name__ == "__main__":
   app.run(debug=False,port=8950)
