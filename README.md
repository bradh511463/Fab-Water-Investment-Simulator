# Fab-Water-Investment-Simulator

## What it is:
This project was built to help evaluate the tradeoffs between Water Investment for Wafer Fabrications centers to their ultimate financial goals. Can alignment exist where because of the investments made that fabrication centers become more profitable?  To answer that question the goal was to develop an interactive decision-support dashboard that models this systemic relationship. Rather than merely optimizing for cost or water savings, the system enables users to explore the dynamic trade-offs between investment in water-efficient technologies and financial outcomes delivering both business rationale and sustainability alignment

## Features
- Scenario sliders for water-technology investments  
- ROI & water-savings forecasts over time  
- Composite sustainability scoring  
- Causal loop diagram (CAS) visualization  
- Auto-downloadable large water-model `.pkl`

## File Structure
# Main launcher
-  v7_1_streamlit.py         
# ROI logic & metrics
- v7_4_roi_streamlit.py
# CAS flow visualization module
- v7_3_cas_st.py
# ML Model for Wafer Intention Multiplier effect on revenue
- revenue_multiplier_model.pkl 
# Downloaded at runtime
- v6_1_water_model_boosted.pkl  # Downloaded at runtime
# Python dependencies
- requirements.txt           
# This file
-  README.md                

## Dependancies
Please refer to requirements.txt 

List:
- streamlit
- pandas
- numpy
- joblib
- gdown
- plotly
- scikit-learn



## Installation and Run
'''bash
git clone https://github.com/bradh511463/Fab-Water-Investment-Simulator.git
cd Fab-Water-Investment-Simulator
pip install -r requirements.txt
streamlit run v7_1_streamlit.py


## Google Drive Link
The water-model (v6_1_water_model_boosted.pkl) is hosted externally—if you need to grab it manually, here’s the link:
https://drive.google.com/file/d/1pZ_vFRfqx1mw1RpoMR_fanrrOvHHMDiN/view?usp=sharing

## Deployment on Streamlit
Deploy on Streamlit Cloud (select repo, set main file to v7_1_streamlit.py).


## Contributing & License
Feedback is always welcomed. Please reach out to bllarso2@asu.edu if running into any issues. 

