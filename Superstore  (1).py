#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from  sklearn.metrics import *
from sklearn.linear_model import LinearRegression
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.express as px
import seaborn as sns


# In[2]:


df = pd.read_excel(r"C:\Users\ibori\OneDrive\Documenten\Global Superstore.xls")

##loading the data set


# In[3]:


df.head(2).T


# In[4]:


missingpercent=np.round(df.isnull().sum()/len(df)*100,2)
missingpercent


## Calculating the Percentage of null values from each Columns 


# In[5]:


df.info()


# In[6]:


### will be dropping the postal code columns because it has more than 80% empty records and also the Row ID column

df.drop(['Postal Code','Row ID'],axis=1,inplace = True)


# In[7]:


df.head(2).T


# In[8]:


corr= df.corr(numeric_only=True)
sns.heatmap(corr,annot=True,fmt='.2%',cmap='Blues')
plt.show()


### the correlation of numerical varaibles 


# In[9]:


corr=pd.DataFrame(df.corrwith(df['Sales'],numeric_only=True))


sns.heatmap(corr,cmap='Blues',annot=True,fmt='.2%')
plt.show

### correlating the sales with other numerical columns 


# #### The Sales column is positively related to all other numerical columns exept Discount columns meaning when the discount price is up the payment gotten as sales price will be down which makes sense although  the corrrelation is not that impactive since its less that 10%

#  ###### Exploratory Data Analysis (EDA)

# In[10]:


segment = ['State','City','Country','Market','Region','Category','Sub-Category','Order Priority','Ship Mode','Segment']


# In[11]:


for i in segment:
    print(f'Unique counts of {i}:{df[i].nunique()}')


# In[12]:


### will be analysing the dataset from the list to highest base on the unique counts to find patterns
#(Ptofit,Sales,Discount,Quentity sold)


# #### 1 Category (3)

# In[78]:


category = df.groupby('Category').agg(Total_sales = ('Sales','sum'),Total_Profit=('Profit','sum'),
                                         Total_Quantity=('Quantity','sum'),
                                        Total_Discount=('Discount','sum'),
                                        Total_customers=('Customer ID','count'),
                                        Total_Orders=('Order ID','count'),
                                        Total_Avg=('Sales','mean'),
                                        Total=('Profit','mean')).reset_index().round(2)
category.sort_values(by='Total_Profit',ascending=False)


# In[14]:


fig = px.bar(category, x='Category', y=['Total_Quantity', 'Total_Discount'],
             color_discrete_map={ 'Total_Profit': 'pink','Total_Discount':'red'},
             title='Total Profit and Discount by Category',
             labels={'value':'Amount' ,'variable':'Labels'},
            barmode='group')

fig.show()


# ####  Office Supplies Category has the highest Quantity sold and discount.

# In[15]:


# Assuming 'category' is your DataFrame
fig = px.pie(category, names='Category', values='Total_Quantity',
             title='Total Quantity Sold By Category',
             labels={'value': 'Total Quantity'})

fig.show()


# In[16]:


fig = px.pie(category, names='Category', values='Total_customers',
             title='Total Customers By Category',
             labels={'value': 'Total Quantity'})

fig.show()


# In[17]:


fig = px.pie(category, names='Category', values='Total_sales',
             title='Total Sales By Category',
             labels={'value': 'Total Quantity'})

fig.show()


# #### Total Sales By category illustrate that Technology has the highest amount of sales followed by  Furniture and lastly Office supplies which makes sense even though office supplies has more quantity sold it did not generate the highest amount of sales because items like Television, Computers will be more expensive than furnitures and office supplies and also office supplies are bought often hence more quantity sold . Check the average sales column from the table created from the grouping 

# In[18]:


import plotly.express as px

# Assuming 'category' is your DataFrame
fig = px.bar(category, x='Category', y=['Total_sales', 'Total_Profit','Total_Quantity',],
             title='Total Sales, Quantity and Profit by Category',
             labels={'value': 'Total Amount', 'variable': 'Metric'},
             color='variable',
             barmode='group')  # Set barmode to 'group' for clustered bars

fig.show()


# #### 2 Segment(3)

# In[77]:


seg = df.groupby('Segment').agg(Total_Sales=('Sales','sum'),
                               Total_Profit=('Profit','sum'),
                               Total_Discount=('Discount','sum'),
                               Total_Customers=('Customer ID','count'),
                               Total_Quantity=('Quantity','sum'),
                               Total_Avg=('Profit','mean')
                               ).reset_index().round(2)
seg


# In[20]:


fig= px.bar(seg,x='Segment',y=['Total_Sales','Total_Profit'],
           title='Sales And Profit By Segment',
           labels={'value':'Amount','variable':'Labels'},
           barmode='group')
fig.show()


# #### If you remember when we checked the correlation of Sales and Other Numerical columns it was possitively correlated with all except Discount from the above bar chat it can be seen that grouping by segment Consumer segment has more Sales nd in turn has more profit made. from the graph it is ideal and plausible because consumer items will be purchased more followed my corperate and lastly Home office items because not everyone has home office even though they work 

# In[21]:


fig = px.bar(seg,x='Segment',y=['Total_Discount','Total_Customers','Total_Quantity'],
            title='Total Discount, Quantity And Customers By Segment',
                    labels={'value':'Unit','variable':'Labels'},
             barmode='group'
    )
fig.show()


# #### 3 Order Priority:4

# In[73]:


Priority = df.groupby('Order Priority').agg(Total_sales=('Sales','sum'),
                                           Total_Profit=('Profit','sum'),
                                           Total_Quantity=('Quantity','sum'),
                                           Total_Discount=('Discount','sum'),
                                           Total_customers=('Customer ID','count'),
                                           Total_avr=('Sales','mean')).reset_index().round(2)
Priority


# In[23]:


fig = px.bar(Priority,x='Order Priority',y=['Total_sales','Total_Profit',],
            title='Total Sales And Total Profit By Order Priority',
            barmode='group')
fig.show()


# ##### The correlation can also be seen in the Order priority Grouping

# In[24]:


fig = px.bar(Priority,x='Order Priority',y=['Total_Quantity','Total_Discount','Total_customers'],
            title='Total Quantity Sold,Total Customers And Total Discount By Priority',
            barmode='group',
            labels={'value':'Total','variable':'Label'},
            template='plotly')
fig.show()


# ##### 4 Ship mode (4)

# In[72]:


Shipmode = df.groupby('Ship Mode').agg(Total_sales=('Sales','sum'),
                                      Total_Profit=('Profit','sum'),
                                      Total_Quatity=('Quantity','sum'),
                                      Total_Discount=('Discount','sum'),
                                      Total_customers=('Customer ID','count'),
                                      Total_avgcost=('Shipping Cost','mean')).reset_index().round(2)
Shipmode


# In[26]:


fig = px.bar(Shipmode,x='Ship Mode',y=['Total_sales','Total_Profit'],
            labels={'value':'Amount','variable':'Labels'},
            barmode='group')
fig.show()


# In[27]:


fig = px.bar(Shipmode,x='Ship Mode',y=['Total_Quatity','Total_Discount','Total_customers'],
            title='Total Quantity Total Customers And Total Discount By Shipmode',
            barmode='group',
            labels={'value':'Value','varaible':'Labels'})
fig.show()


# #### Most Customers make use of the Standard shipmode and rarely use same day shipment mode, looking at the average shipping cost of all the shipping mode standard class is cheapest hence the more use by customers. 

# #### 5 Market (7)

# In[82]:


Market = df.groupby('Market').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_customers=('Customer ID','count'),
                                 Total_avr=('Sales','mean'),
                                 Total_P=('Profit','mean')).reset_index().round(2).sort_values(by='Total_Sales',ascending=False)
Market


# In[29]:


fig = px.bar(Market,x=['Total_Sales','Total_Profit'],y='Market',
barmode='group',
title='Total Sales And Profit By Market',
labels= {'value':'Amount','variable':'Label'})
fig.show()


# ###### APAC has the highest sales and made the highest Profit foolowed by EU and US Canada has the lowest Sales and Profit Although Africa has more Profit than EMEA it has less Sales than EMEA thats why the correlation between sales and profit is not equal 1. Corr(ranges from -1 to 1)

# In[30]:


fig= px.bar(Market,x=['Total_customers','Total_Quantity'],y='Market',
           labels={'value':'Total_Count','variable':'Labels'},
           title='Total Customers and Quantity Sold By Market',
           barmode='group')
fig.show()


# #### Canada has the lowest Customers hence less Quantity Sold And also worth stating US has less customers but have more quantity sold which can be possible because of othe social contraint like standard of living of the different Market Geography 

# #### 6 Region (13)

# In[83]:


Region = df.groupby('Region').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_customers=('Customer ID','count'),
                                 Total_avr=('Sales','mean'),
                                 Total_P=('Profit','mean')).reset_index().round(2).sort_values(by=['Total_Profit'],ascending=False).head(10)
Region


# In[32]:


fig = px.bar(Region,x=['Total_Profit'],y='Region',
            title = 'Top 10 Region by Profit ',
            labels= {'value':'Amount','variable': 'Labels'}
            )
fig.show()


# In[33]:


Region = df.groupby('Region').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_customers=('Customer ID','count')).reset_index().round(2).sort_values(by=['Total_Sales'],ascending=False).head(10)
Region

fig = px.bar(Region,x=['Total_Sales'],y='Region',
            title = 'Top 10 Region by Sales ',
            labels= {'value':'Amount','variable': 'Labels'}
            )
fig.show()


# In[34]:


Region = df.groupby('Region').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_customers=('Customer ID','count')).reset_index().round(2)
Region


# In[35]:


fig = px.bar(Region,x=['Total_Discount','Total_Quantity','Total_customers'],y='Region',
            title='Total Discount, Quantity And Customers By Region',
            labels={'value':'Unit','variable':'Labels'},
            barmode='group')
fig.show()


# ##### 7 Sub-Category(17)

# In[89]:


Sub = df.groupby('Sub-Category').agg(Total_Sales=('Sales','sum'),
                                    Total_Profit=('Profit','sum'),
                                    Total_Quantity=('Quantity','sum'),
                                    Total_Discount=('Discount','sum'),
                                    Total_Customers=('Customer ID','count'),
                                    Total_avr=('Sales','mean'),
                                    Total=('Profit','mean')).reset_index().round(2).sort_values(by='Total_Sales',ascending=False).head(10)
Sub


# In[37]:


fig = px.bar(Sub,x=['Total_Sales'],y='Sub-Category',
            title='Top 10 Sub_Category By Sales',
            labels={'value':'Amount','variable':'Labels'},
            )
fig.show()


# ##### Remember when we checked the Sales,Profit of different category (Technology , Furnitures and office supplies ) Technology has the highest Sales Amount followed by Fuenitures and lastly office supplies even when Ofices supplies has more quantity sold. As they say if you beat up a dataset it will confess lol. so from the top 10 sub category by sales we can see that it is mostly dominated by Technology eqiupment and Furnitures.

# In[90]:


Sub = df.groupby('Sub-Category').agg(Total_Sales=('Sales','sum'),
                                    Total_Profit=('Profit','sum'),
                                    Total_Quantity=('Quantity','sum'),
                                    Total_Discount=('Discount','sum'),
                                    Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values(by='Total_Profit',ascending=False).head(10)
Sub


# In[91]:


fig = px.bar(Sub,x='Sub-Category',y='Total_Profit',
            title='Top 10 Sub-Category By Profit',
            barmode='group',
            )
fig.show()


# In[92]:


Sub = df.groupby('Sub-Category').agg(Total_Sales=('Sales','sum'),
                                    Total_Profit=('Profit','sum'),
                                    Total_Quantity=('Quantity','sum'),
                                    Total_Discount=('Discount','sum'),
                                    Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values(by='Total_Quantity',ascending=False)
fig = px.bar(Sub,x=['Total_Quantity','Total_Customers','Total_Discount'],y='Sub-Category',
            title='Total Quantity, Cusomers And Discount By Sub-Category',
            barmode='group',
            labels= {'value':'','variable':'Labels'})
fig.show()


# ##### This bar graph above just comfirmed the earlier stated assumptions 

# ##### 8 Country(147)

# In[93]:


Country = df.groupby('Country').agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count'),
                                    Total_avr=('Sales','mean'),
                                 Total_P=('Profit','mean')
                                   ).reset_index().round(2).sort_values('Total_Sales',ascending=False).head(10)
Country


# In[42]:


Country = df.groupby('Country').agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Sales',ascending=False).head(10)



fig = px.bar(Country,y='Total_Sales',x='Country',
            title='Top 10 Country by Sales',
            color='Total_Customers'  # Set color based on Total_Sales
              )
fig.show()


# ###### United States has more customers hence more sales. key piont to note is that Even when Mexico has more cutomers it has lower sales than China and Germany again this can be explianed by other socio-political contraint like unemployment rate and poverty-index level.

# In[43]:


Country = df.groupby('Country').agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Profit',ascending=False).head(10)


fig = px.bar(Country,y='Country',x='Total_Profit',
            title='Top 10 Country by Profit',
            color='Total_Sales'  # Set color based on Total_Sales
              )
fig.show()


# #### This further support my first assumptions we can see even when Countris like Australia has more sales it does not imply that more profit will be made, fir instance countries like India, United Kingdom has less sales but Profit is high in such countries this can be possible by other constraint like ease of starting up a business.

# In[94]:


Country = df.groupby('Country').agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count'),
                                   Total_avr=('Sales','mean'),
                                 Total_P=('Profit','mean')).reset_index().round(2).sort_values('Total_Profit',ascending=False).tail(10)


fig = px.bar(Country,y='Country',x='Total_Profit',
            title='Bottom 10 Country by Profit'
             # Set color based on Total_Sales
              )
fig.show()


# In[95]:


Country


# ##### Bottom countries by Profit countries like Nigeria and  turkey  is not ptofitable to start up a business there hence the negative in profit. sales does not imply that a seller will be in profit sometimes losses occur.
# 

# In[45]:


Country = df.groupby('Country').agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Sales',ascending=False).tail(10)


fig = px.bar(Country,y='Country',x='Total_Sales',
            title='Bottom 10 Country by Sales'
             # Set color based on Total_Sales
              )
fig.show()


# ##### 9 State()

# In[46]:


Top10State = df.groupby(['State']).agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Sales',ascending=False).head(10)

fig = px.bar(Top10State,y=['Total_Sales','Total_Profit'],x='State',
            title= 'Top 10 Sales by State',
             barmode='group'
            )
fig.show()

Bottom10State = df.groupby(['State']).agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Sales').head(10)

fig = px.bar(Bottom10State,y='Total_Sales',x='State',
            title= 'Bottom 10 Sales by State'
            )
fig.show()

Bottom10StateC = df.groupby(['State']).agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Customers',ascending=False).head(10)


fig = px.bar(Bottom10StateC,y='Total_Customers',x='State',
            title= 'Top 10 State by Customers Count'
            )
fig.show()


# In[47]:


Top10State = df.groupby(['State']).agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Profit',ascending=False).head(10)

fig = px.bar(Top10State,y=['Total_Profit'],x='State',
            title= 'Top 10 Profit by State',
             barmode='group',
             labels={'value':'Amount','variable':'Labels'}
            )
fig.show()

Bottom10State = df.groupby(['State']).agg(Total_Sales=('Sales','sum'),
                                   Total_Profit=('Profit','sum'),
                                   Total_Quantity=('Quantity','sum'),
                                   Total_Discount=('Discount','sum'),
                                   Total_Customers=('Customer ID','count')).reset_index().round(2).sort_values('Total_Profit').head(10)

fig = px.bar(Bottom10State,y=['Total_Profit','Total_Sales'],x='State',
            title= 'Bottom 10 Profit by State',
             barmode='group',
             labels={'value':'Amount','variable':'Labels'}
            )
fig.show()


# ##### From the bottom 10 states by profit we can see that states like instabul and lagos that are located in turkey and Nigeria respectively the profit is negative even when sales where made for and even the profit loss is higher than sales this is possible because the company ,might have spent more on  high operating costs, unexpected expenses, or inefficient business operations.

# #### 10 City ()
# 

# In[48]:


Top10city =df.groupby('City').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Customers=('Customer ID','count')).reset_index().sort_values(by='Total_Sales',ascending=False).head(10)
fig = px.bar(Top10city,x='City',y=['Total_Sales','Total_Profit'],
            title='Top 10 City By Sales',
             barmode='group'
            )
fig.show()

Bottom10city =df.groupby('City').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Customers=('Customer ID','count')).reset_index().sort_values(by='Total_Sales').head(10)
fig = px.bar(Bottom10city,x='City',y='Total_Sales',
            title='Bottom 10 City by Sales'
            )
fig.show()

Top10cityP =df.groupby('City').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Customers=('Customer ID','count')).reset_index().sort_values(by='Total_Profit',ascending=False).head(10)
fig = px.bar(Top10cityP,x='City',y='Total_Profit',
            title='Top 10 City by Profit'
            )
fig.show()

Bottom10cityP =df.groupby('City').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Customers=('Customer ID','count')).reset_index().sort_values(by='Total_Profit').head(10)
fig = px.bar(Bottom10cityP,x='City',y='Total_Profit',
            title='Bottom 10 City by Profit'
            )
fig.show()


Bottom10cityC =df.groupby('City').agg(Total_Sales=('Sales','sum'),
                                 Total_Profit=('Profit','sum'),
                                 Total_Quantity=('Quantity','sum'),
                                 Total_Discount=('Discount','sum'),
                                 Total_Customers=('Customer ID','count')).reset_index().sort_values(by='Total_Customers',ascending=False).head(10)
fig = px.bar(Bottom10cityC,x='City',y='Total_Customers',
            title='Top 10 City by Customers Count'
            )
fig.show()


# In[49]:


df1= df.copy()


# #### (11) Date (Year and Month) Trend  (Order Date)

# In[50]:


df1['MonthOrder']=pd.to_datetime(df['Order Date']).dt.month_name()
df1['YearOrder']=pd.to_datetime(df['Order Date']).dt.strftime('%Y')
df1['DayOrder'] = pd.to_datetime(df['Order Date']).dt.dayofweek+1
df1['MonthNo']=pd.to_datetime(df['Order Date']).dt.strftime('%m')
df1['Dayname'] = pd.to_datetime(df['Order Date']).dt.day_name()


# In[51]:


df1.info()


# In[52]:


df1['Year-Month'] = df1['YearOrder']+ '-' + df1['MonthNo'] 


# In[53]:


Yeartrend=df1.groupby('YearOrder').agg(Total_Sales=('Sales','sum'),Total_Profit=('Profit','sum'),Total_Orders=('Order ID','count')).reset_index().round(2)
Yeartrend


# In[54]:


fig = px.line(Yeartrend,x='YearOrder',y=['Total_Sales','Total_Profit'],
             title='Profit And Sales Yearly Trend',
              markers=True
             )
fig.show()


# ##### Sales and Profit is in a yearly uptrend meaning the business is growing and should continue with all of thier current policy and improve in where they need to improve on .

# In[96]:


Month_agg =df1.groupby(['MonthNo','MonthOrder']).agg(Total_Sales=('Sales','sum'),
                                                    Total_Profit=('Profit','sum'),
                                                     Total_Quantity=('Quantity','sum'),
                                                    Total_avr=('Sales','mean'),
                                 Total_P=('Profit','mean')).reset_index().round(2).sort_values(by='MonthNo')
Month_agg


# In[56]:


fig = px.line(Month_agg,x='MonthOrder',y=['Total_Sales','Total_Profit'],
             title='Profit And Sales Monthly Trend',
              markers=True
             )
fig.show()


# ##### Monthly Projections February as the lowest sales and profit although between June to August(July) there is sharp drop of sales and profit and December as more sales but more profit is made in November

# In[57]:


Year_Month = df1.groupby(['Year-Month','MonthOrder']).agg(Total_Sales=('Sales','sum'),Total_Profit=('Profit','sum')).reset_index().round(2)
Year_Month


# In[58]:


fig = px.line(Year_Month,x='Year-Month',y=['Total_Sales','Total_Profit'],
             title='Profit And Sales Yearly/Monthly Trend',
              labels={'value':'Amount','variable':'Labels'},
              markers=True
             )
fig.show()


# In[97]:


DailyTrend = df1.groupby(['Dayname','DayOrder']).agg(Total_Sales=('Sales','sum'),
                                                   Total_Profit=('Profit','sum'),
                                                   Total_Quantity=('Quantity','sum'),
                                                   
                                                   Total_Discount=('Discount','sum'),
                                                    Total_avr=('Sales','mean'),
                                 Total_P=('Profit','mean')).reset_index().round(2).sort_values(by='DayOrder')
DailyTrend


# In[60]:


fig = px.line(DailyTrend,x='Dayname',y=['Total_Sales','Total_Profit'],
            title= 'Daily Sales And Profit Trend',
            labels={'value':'Amount','variable':'Labels'},
              markers='True'
            )
fig.show()


# #### less sales and profit on weekends Saturday and sunday because probably its not workdays ans offices are often close and even when open they often close earlier than usual. looking at friday it can be deduced that customers tend to fill up items for the weekends since they might not be chanced to come in on saturday and sundays,hence friday more sales are made with wednesday having the lowest sales amount  

# ##### ShipDate

# In[61]:


df1['MonthShip']=pd.to_datetime(df['Ship Date']).dt.month_name()
df1['YearShip']=pd.to_datetime(df['Ship Date']).dt.strftime('%Y')
df1['DayOrders'] = pd.to_datetime(df['Ship Date']).dt.dayofweek+1
df1['MonthNos']=pd.to_datetime(df['Ship Date']).dt.strftime('%m')
df1['Daynames'] = pd.to_datetime(df['Ship Date']).dt.day_name()


# In[65]:


Shipyear = df1.groupby('YearShip').agg(Total_Shipments=('Order ID','count'),Total_ShipCost=('Shipping Cost','sum'),
                                      Total_Profit=('Profit','sum')).reset_index().round(2)
Shipyear


# In[67]:


fig = px.line(Shipyear,x='YearShip',y=['Total_Shipments','Total_ShipCost','Total_Profit'],
             title='Profit And Sales Yearly/Monthly Trend',
              labels={'value':'Unit','variable':'Labels'},
              markers=True
             )
fig.show()


# #### Data Cleaning 
# 
# #### Drop columns : Yes 
# ###### Row ID AND Postal ID
# 
# ### Summary 
# 
# ###### The Sales column is possitively correlated with all other numeric collumns except the discount column, although it is not significant because its below 10%
# ###### From the average Sales and profit of items based on category, Technolgy items are more expensive and more profitable followed by Furniture and lastly office suppliers
# ###### Comparing By Order Priority Meduim priority has more sales amount but critical has more sales per item meaning critical priority items are more expensive the lowest among this category is low priority.
# ###### Most customers make use of the standard shipmode because as seen in the average shipment cost standard ship mode is the cheapest 
# ###### Apac has more sales among the market followed by EU nad US, Canada has the lowest quantity sold and  lowest total  sales although it has higher average sales than market like Africa and EMEA. This is possible because of other social-political constraint like Unemployment, Insecurities e.t.c
# ###### Although  USA has the highest Profit,Quantity sold and Sales it is not the best performing market . fro instance India has the highest average Sales and Profit.
# ###### From the yearly trend its safe to say that the market is on an yearly  uptrend 
# ###### From the monthly trend More sales amount occur in December  but if we use average sales and profit  October is the best performing month this can be possible if for instance more expensive items where bought with less transaction and quantity sold
# ##### Less sales on weekends and more on weekdays.

# ## Recommendations 
# 
# ###### Since all Business are set up for profit making except non-profit organizations i will recommend that the company try to gear thier policy towards maket segment that are profit and try to prevent loss for instance 
# ###### They should try and review thier weekdays opening hours if they usualy close early on friday they should try extend to few hours late to check out if it will impact profit since they make more profit on fridays 
# ##### Also using the monthly average profit we can see that october is a unique month and should be given more attension to make more more profit and for months that profit are low the company should investigate if it has to organization setbacks or customers churning thier products for competitors 
# ##### Using the shipping mode as a case study since the customers use the lowest on average ship cost (standard mode) i recommend the process should be rid of setbacks like delay this will improve customers satisfaction which will in turn improve sales and Profit.
# ##### As seen from the EDA performed on the dataset it can be said that Sales does not connotes Profit for instance countries like Nigeria and Turkey has negative profit amounts and some even have more negative profit than sales amount meaning the country  as high operating costs, unexpected expenses, or inefficient business operations.Hence i will recommend if they cant find a way to prevent the loss they should close up thier branches in that country 
# 
# 
# 
# 
# 
# 
# 
# 

# ### ''THANKS FOR READING''

# In[ ]:




