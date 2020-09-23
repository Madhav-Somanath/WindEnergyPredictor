import streamlit as slt 
import joblib
import random
import time
from PIL import Image

slt.beta_set_page_config(page_title="Wind Energy Predictor", page_icon="🌪")

def main():
    model = joblib.load("lasso.pk1")
    day = random.randint(1,30)
    
    directiondict = {"N":0, "NNE":30, "NEE":60, "E":90, "SEE":120, "SSE":150, "S":180, "SSW":210, "SWW":240, "W":270, "NWW":300, "NNW":330}
    def wind_direction(x):
        for x in directiondict:
            return directiondict[x]

    monthdict = {"January":1, "Febrauary":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11}
    def find_month(x):
        if x in monthdict:
            return monthdict[x]
        else:
            return 12 
    
    imgdict = {"N":'assests/N_Powercurve.jpeg',
               "NNE":'assests/NNE_Powercurve.jpeg',
               "NEE":'assests/NEE_Powercurve.jpeg',
               "E":'assests/E_Powercurve.jpeg',
               "SEE":'assests/SEE_Powercurve.jpeg',
               "SSE":'assests/SSE_Powercurve.jpeg',
               "S":'assests/S_Powercurve.jpeg',
               "SSW":'assests/SSW_Powercurve.jpeg',
               "SWW":'assests/SWW_Powercurve.jpeg',
               "W":'assests/W_Powercurve.jpeg',
               "NWW":'assests/NWW_Powercurve.jpeg',
               "NNW":'assests/NNW_Powercurve.jpeg'}
    
    def draw_graph(x):
        if x in imgdict:
            image = Image.open(imgdict[x])
            return image

    slt.title("WIND ENERY OUTPUT PREDICTOR")
    slt.sidebar.title("PARAMETERS")
    direction = slt.sidebar.selectbox('Cardinal/Intercardinal Direction',('N','NNE','NEE','E','SEE','SSE','S','SSW','SWW','W','NWW','NNW'),key='direction')
    speed = slt.sidebar.slider('Wind Speed',3.0,25.5,step=1.0,key='speed')
    month = slt.sidebar.selectbox('Month',('January','Febraury','March','April','May','June','July','August','September','October','November','December'),key='month')
    time_ = slt.sidebar.number_input('Output Hour',0.0,24.0,step=1.0,key='time_')
    if slt.sidebar.button("Evaluate"):
        with slt.spinner('Predicting output...'):
            time.sleep(1)
            predict = model.predict([[wind_direction(direction),find_month(month),day,time_,speed]])
            slt.write('Predicted Energy Output (KW/h):', predict.round(2))
            slt.success('Evaluated!')
            slt.write("Data collected and evaluated to build model for {} winds".format(direction))
            slt.image(draw_graph(direction),use_column_width=True)

if __name__ == '__main__':
    main()
