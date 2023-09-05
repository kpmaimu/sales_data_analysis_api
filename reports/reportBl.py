import datetime
import json
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
#nltk.download('stopwords')
from nltk import word_tokenize,sent_tokenize


def getReport (fileName=''):
    global df
    print("in function..")
    #read dataset
    df = pd.read_excel (fileName)        
    #start first algorithm to find total sale and profit
    df["total_sale"]=df["Sales"]*df["Quantity"]#calculate sale=sale*count
    totalSale=df['total_sale'].sum()#sum the whole columns of sale 
    df["total_profit"]=df["Profit"]*df["Quantity"]#calculate profit=profit*count
    totalProfit=df['total_profit'].sum()#sum the whole profit
    ##start second algorithm to find most running and least running month
    df["total_sale"]=df["Sales"]*df["Quantity"]#calculate total sale 
    df['month'] = pd.DatetimeIndex(df['Order Date']).month#add a column month and get values
    df_sale=df[['month', 'total_sale']]#create subtable with month and total sale
    table = pd.pivot_table(df_sale,index=["month"],
               values=["total_sale"],
               aggfunc=[np.mean],fill_value=0)#create pivot table of table applying mean to sales
    x=df_sale['total_sale'].idxmax()#return index of table of max value of sale in pivot table
    y=df_sale.at[x,'month']#return month of index
    #SAME FOR MIN
    x=df_sale['total_sale'].idxmin()#return index of table of max value of sale in pivot table
    z=df_sale.at[x,'month']#return month of index
    ###start third algorithm to find least running and most running category
    df_cat1 = df.groupby('Category')['Quantity'].sum().reset_index(name='Count')
    # print(df_cat1['Count'].idxmax())#return index with maximum count value
    x=df_cat1['Count'].idxmax()#store it in variable x
    s=df_cat1['Count'].idxmin()#store it in variable x
    v=df_cat1.at[x,'Category']#return and print value in category column where index=x
    w=df_cat1.at[s,'Category']#return and print value in category column where index=x
    #c=df_cat1.at[x,'Count']
    #d=df_cat1.at[s,'Count']
    ####start fourth algorithm
    sub_cat = df.groupby('Sub-Category')['Quantity'].sum().reset_index(name='Count')
    x=sub_cat['Count'].idxmax()#index of subcategory with maximum value in count
    u=sub_cat['Count'].idxmin()#index of subcategory with minimum value in count
    a=sub_cat.at[x,'Sub-Category']#return and print value in Sub-Category column where index=x
    b=sub_cat.at[u,'Sub-Category']
    #####start fifth algorithm
    df_reg=df[['Region', 'total_sale']]
    df_reg = df.groupby('Region')['total_sale'].sum().reset_index(name='Count')
    reg_x=df_reg['Count'].idxmax()#index of subcategory with maximum value in count
    reg_z=df_reg['Count'].idxmin()#index of subcategory with minimum value in count
    r=df_reg.at[reg_x,'Region']#return and print value in Sub-Category column where index=x
    t=df_reg.at[reg_z,'Region']
    ######start sixth algorithm
    df_cus=df[['Customer Name','Customer ID', 'total_sale']]
    df_cus= df_cus.groupby('Customer ID')['total_sale'].sum().reset_index(name='Count')
    cus_x=df_cus['Count'].idxmax()#index of subcategory with maximum value in count
    cus_z=df_cus['Count'].idxmin()#index of subcategory with minimum value in count
    cr=df_cus.at[cus_x,'Customer ID']#return and print value in Sub-Category column where index=x
    ct=df_cus.at[cus_z,'Customer ID']#return and print value in Sub-Category column where index=x
    ##########start seventh algorithm
    df_cus1=df[['Customer Name','Customer ID', 'Quantity']]
    df_cus1= df_cus1.groupby('Customer ID')['Quantity'].sum().reset_index(name='Count')
    cus1_x=df_cus1['Count'].idxmax()#index of subcategory with maximum value in count
    cus1_z=df_cus1['Count'].idxmin()#index of subcategory with minimum value in count
    cr1=df_cus1.at[cus1_x,'Customer ID']#return and print value in Sub-Category column where index=x
    ct1=df_cus1.at[cus1_z,'Customer ID']#return and print value in Sub-Category column where index=x
    
    data={"least_amount_customer":ct1, "most_amount_customer":cr1,"least_quantity_customer ":ct, "most_quantity_customer ":cr,"laest_region":t, "most_region":r,"least_subcategory":a, "most_subcategory":b,"least_category":w, "most_category":v,"least_month":int(z), "most_month":int(y),"totalSales":totalSale, "totalProfit":totalProfit}        
    
    return data

def getCategoryReport(fileName,filter):
    df = pd.read_excel(fileName)
    # resultCategrory = df.groupby()['Quantity'].sum().reset_index(name='Count')
    resultCategrory = df.groupby(filter)['Quantity'].sum().reset_index(name='Count')
    print(resultCategrory)
    return(resultCategrory)

# def getSubCategoryReport(fileName):
#     df = pd.read_excel(fileName)
#     # resultCategrory = df.groupby('Product Name')['Quantity'].sum().reset_index(name='Count')
#     resultCategrory = df.groupby('Sub-Category')['Quantity'].sum().reset_index(name='Count')
#     return(resultCategrory)
def getMonthReport(fileName):
    df = pd.read_excel(fileName)
    df["total_sale"]=df["Sales"]*df["Quantity"]#calculate total sale 
    df['month'] = pd.DatetimeIndex(df['Order Date']).month#add a column month and get values
    df_sale=df[['month', 'total_sale']]#create subtable with month and total sale
    table = pd.pivot_table(df_sale,index=["month"],
               values=["total_sale"],
               aggfunc=[np.mean],fill_value=0)#create pivot table of table applying mean to sales
    month_data = []
    for index, row in table.iterrows():
        data = {}
        data['month'] = index
        data['averageSale'] = row[table.columns.values][0]
        month_data.append(data)
    return (month_data)
def getRegionReport(fileName):
    df = pd.read_excel(fileName)
    df["total_sale"]=df["Sales"]*df["Quantity"]#calculate total sale
    df_reg=df[['Region', 'total_sale']]
    df_reg = df.groupby('Region')['total_sale'].sum().reset_index(name='Count')
    return(df_reg)

def percent(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    percentage = 0
    if num2>0:
        percentage = '{0:.2f}'.format((num1 / num2 * 100))
    return percentage

def sentiment(review):
    tokenized_text = sent_tokenize(review)
    tokenized_word = word_tokenize(review)
    stop_words = set(stopwords.words("english"))
    filtered_sent = []
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    po = set(stopwords.words("positive-words"))
    po_fi = []
    for w in filtered_sent:
        if w in po:
            po_fi.append(w)
    ne = set(stopwords.words("negative-words"))
    ne_fi = []
    for w in filtered_sent:
        if w in ne:
            ne_fi.append(w)
    a = len(po_fi)
    b = len(ne_fi)
    c = a+b
    x=percent(a,c)
    return x
def getSentiment(fileName, filter):
    df = pd.read_excel(fileName)        
    category_comment = df[[filter, 'Comments']]    
    modifiedResult = category_comment.groupby(
        filter)['Comments'].apply(lambda x: "{%s}" % ' '.join(x))
    modifiedResultDf = pd.DataFrame(
        {filter: modifiedResult.index, 'Value': modifiedResult.values})
    new_dict = {}
    for index, row in modifiedResultDf.iterrows():
        res = sentiment(row['Value'])
        new_dict.update({row[filter]: res})
    return new_dict
