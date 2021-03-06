#config running environment
import os
import tempfile
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()
#import section
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")
# data config
# Add 'overweight' column
df['overweight'] = np.where((10_000*(df['weight']/(df['height'])**2))>25, 1, 0 )

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
cholest=df['cholesterol'].value_counts()
if len(cholest)>2:
    for i in cholest.index:
        if i==1:
            df=df.replace({'cholesterol': {i:0}})
        elif i>1:
            df=df.replace({'cholesterol':{i:1}})

gluc=df['gluc'].value_counts()
if len(gluc)>2:
    for i in gluc.index:
        if i==1:
            df=df.replace({'gluc': {i:0}})
        elif i>1:
            df=df.replace({'gluc':{i:1}})
        
# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat=pd.melt(df, id_vars=['cardio'],value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    #df_cat['total']=1
    #df_cat=df_cat=df_cat.groupby(["cardio", "variable", "value"], as_index=False).count()
    df_cat=df_cat.groupby(["cardio", "variable", "value"]).size().reset_index()
    df_cat=df_cat.rename(columns={0:'total'})

    # Draw the catplot with 'sns.catplot()'
    fig=sns.catplot(data=df_cat, x='variable', y='total', hue='value', col="cardio", kind='bar').fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])&(df['height'] >= df['height'].quantile(0.025))&(df['height']<=df['height'].quantile(0.975))&(df['weight']>= df['weight'].quantile(0.025))&(df['weight']<= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr(method='pearson')
    

    # Generate a mask for the upper triangle
    mask = np.triu(corr)


    # Set up the matplotlib figure
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr, mask=mask, annot=True,fmt=".1f", center=.08, square=True, cbar_kws={'shrink':0.5})
    #fig = fig.figure
    
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
