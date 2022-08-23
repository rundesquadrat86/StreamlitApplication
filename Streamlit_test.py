import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

testFrame=pd.DataFrame({"col1":[np.nan,1,2,4],"col2":[np.nan,np.nan,np.nan,np.nan]})
grid_return=AgGrid(testFrame, editable=True)
General=grid_return["data"]
new_df=General
st.write(new_df.fillna(""))
