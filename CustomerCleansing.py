# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:29:04 2022

@author: Saba.Is
"""


import numpy as np
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import plotly.graph_objects as go
from io import BytesIO




# add search file to the sidebar



st.title("Customer Cleansing Application", anchor=None)
excelfile=st.sidebar.file_uploader("Select Excel-File for cleansing",key="Raw_Data")

if excelfile==None:
    st.balloons()
    st.info("Please select the Customer File to be cleansed")
else:

    sheet=st.sidebar.selectbox(
        "Select sheet to be cleansed",
        ("BUT000 - General","BUT100 - Role",
         "BUT0ID - Identifier",
         "ADRC - Address",
         "ADR6 - E-Mail"
         )
        )
    
    
    
    
    if sheet=="BUT000 - General":
        col1,col2,col3,col4=st.columns([5,1,10,1])
        sheets_requiredfields_rules={
            "BUT000 - General":{
              "TYPE":1,
              "BU_GROUP":4,
              "BU_SORT1":20,
              "NAME_ORG1":40}}
        Violationanalysis=pd.DataFrame.from_dict(sheets_requiredfields_rules["BUT000 - General"],orient="index",columns=["Allowed Length"])
        Source_ID=[]
        LengthList=[]
        MissingList=[]
        General=pd.read_excel(excelfile,header=None,sheet_name=sheet)
        
        Multi_header_selection=General[0:7].fillna("").values.tolist()
        
        Multi_header = [Multi_header_selection[0],
                        Multi_header_selection[1],   ###header
                        Multi_header_selection[2],
                        Multi_header_selection[3],
                        Multi_header_selection[4],
                        Multi_header_selection[5],
                        Multi_header_selection[6]]                
        
        column_structure=General.iloc[1]                     ####Define new columns
        General=General.rename(columns=column_structure) ##implement new columns
    
        
        ###Eliminating leading and trailing spaces
        General = General.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            
        
        General=General[7:] ###all data are from row onwards                
        General.index=np.arange(0,len(General.index))
        SourceID_Set=set(General["SOURCE_ID"].values)
        Source_ID.append(SourceID_Set)
        
        Required_Fields_per_Sheet=list(sheets_requiredfields_rules[sheet].keys())
        
        
    
        
        
        for col in Required_Fields_per_Sheet:
            General[col]=General[col].fillna("Missing")                
            if col=="BU_SORT1":
                General[col]=General[col].str.capitalize()     
                
            if col=="NAME_ORG1":
                General[col]=General[col].str.capitalize()                         
    
            General[col]=General[col].astype(str)
            General[col]=np.where((General[col].str.len() <= sheets_requiredfields_rules[sheet][col]) | (General[col] == "Missing"), 
                                            General[col], 
                                            General[col].astype(str) + " - Violation of Rule")
        
    
        #####DONT DELETE THIS LINE 
        General.fillna(" ",inplace=True)
        
        
    
        
        
        
    
        
        
        
        
    
        grid_return=AgGrid(General, editable=True)
        General=grid_return["data"]
        General.replace(" ","",inplace=True)
        
    
        StringlengthFrame=General[["TYPE","BU_GROUP","BU_SORT1","NAME_ORG1"]]
        
        for col in Required_Fields_per_Sheet:
            StringlengthFrame[col+" "+ "Length"]=StringlengthFrame[col].str.len()
            limit=sheets_requiredfields_rules[sheet][col]
            count=StringlengthFrame[col+" "+ "Length"][StringlengthFrame[col+" "+ "Length"]>limit].count()
            MissingElements=(StringlengthFrame[col]=="Missing").sum()
            MissingList.append(MissingElements) ##Number of not filled (missing) elements for required column
            LengthList.append(count)            ##Number fo elements violating string length
    
        
        
        
           
        
        
        
        labels=["TYPE","BU_GROUP","BU_SORT1","NAME_ORG1"]
        ValuesLength=LengthList
        ValuesMissing=MissingList
        fig=go.Figure(
            go.Pie(labels=labels,values=ValuesLength,textinfo="value")
            )
        fig1=go.Figure(
            go.Pie(labels=labels,values=MissingList,textinfo="value")
            )
        
        # fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
        st.plotly_chart(fig1)
        
    
    
        # # def color_violation(val):
        # #     color="red" if "- Violation of Rule" in str(val) else ""
        # #     return 'color: %s' % color
        # # General=General.style.applymap(color_violation)
        # # RequiredFieldsFrame=RequiredFieldsFrame.style.applymap(color_violation)
        
    
        
        
        
        
        
        # def to_excel(df):
        #     output = BytesIO()
        #     writer = pd.ExcelWriter(output, engine='xlsxwriter')
        #     df.to_excel(writer, index=False, sheet_name='BUT000 - General report')
        #     workbook = writer.book
        #     worksheet = writer.sheets['BUT000 - General report']
        #     format1 = workbook.add_format({'num_format': '0.00'}) 
        #     worksheet.set_column('A:A', None, format1)  
        #     writer.save()
        #     processed_data = output.getvalue()
        #     return processed_data    
    
        # df_xlsx = to_excel(General)
        # st.sidebar.download_button(label="Download current sheet",data=df_xlsx,file_name="GeneralSheet.xlsx")
    
    
    
    
    
    
    
    
    
    
    
    
    
        
