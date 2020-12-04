import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpl
plt.rcParams['legend.facecolor'] = 'darkgray'


############################## SUNSPOTS ##############################
def process_sunspots(path):
    data=pd.read_csv(path, index_col=[0], usecols=[1,2], parse_dates=True)
    data.index.name = 'Month'
    data.columns = ['MMTS']
    data = data.sort_index()
    return data
    
def plot_sunspots(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='Monthly Mean of Sunspots observed')
    _=plt.title('Sunspots')
    _=plt.ylabel('Mean Sunspots Numbers')
    



############################## USA ECONOMIC ##############################
def process_usaeconomic(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.index.name = 'Date'
    return data
    
def plot_usaeconomic(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='USA-Consumption, Income, Production, Savings & Unemployment Pct Changes')
    
    

############################## VISITORS TO 20 REGIONS ##############################
def process_20rvisitors(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.index=pd.to_datetime(data.index.str.replace(' ',''))
    data.columns = ['Regions', 'Visitors']
    data.index.name = 'Quarter'
    
    return data
    
def plot_20rvisitors(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=sns.lineplot(x='Quarter', y='Visitors', hue='Regions', data=data.reset_index())
    _=plt.title('Quaterly Vistors to 20 regions in Australlia')
    _=plt.ylabel('Visitors (Million)')
    
    

############################## ELECTRICITY PRODUCTION ##############################
def process_electricityprod(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['Production']
    return data
    
def plot_electricityprod(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='Australlian Monthly Electricity Production')
    _=plt.ylabel('Billion kWh')
    _=plt.xlabel('Dates')


############################## ANTI-DIABETIC DRUG SALES ##############################
def process_antidiabeticdrugs(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    return data
    
def plot_antidiabeticdrugs(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='AntiDiabetic Drug Sale')
    _=plt.ylabel('$ Mn')
    _=plt.xlabel('Dates')
    


############################## USA-CPI ##############################
def process_usacpi(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.index.name = 'Date'
    data.columns = ['CPI']
    
    return data
    
def plot_usacpi(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='USA-Consumer Price Index')
    
    

############################## POPULATION & ENERGY ##############################
def process_popenergy(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data['Renewable_Energy_TWh'] = data[['Hydropower_TWh', 'Solar_TWh',
                                                            'OtherRenewables_TWh', 'TraditionalBiomass_TWh',
                                                            'Wind_TWh', 'Biofuels_TWh']].sum(axis=1)
    data['NonRenewable_Energy_TWh'] = data[['Coal_TWh', 'Oil_TWh', 'Gas_TWh']].sum(axis=1)
    data['Nuclear_Energy_TWh'] = data[['Nuclear_TWh']]
    data = data[['Population', 'Renewable_Energy_TWh', 'NonRenewable_Energy_TWh', 'Nuclear_Energy_TWh']]
    return data
    
def plot_popenergy(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.iloc[:,1:].plot(title='Energy Consumption across various segments')




############################## HOUSING-GAP ##############################
def process_housinggap(path):
    data = pd.read_csv(path, index_col=0)
    return data
    
def plot_housinggap(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot()


############################## AIR PASSENGERS-GAP ##############################
def process_airpassengersgap(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['Passengers']
    data.index.name = 'Date'

    return data
    
def plot_airpassengersgap(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.Passengers.plot(marker='o', markersize=3.5, title='Air Passengers - Monthly Data - With Gap')


############################## INDIA CPI ##############################
def process_housingprices(path):
    
    data = pd.read_csv(path, index_col=0)
    data = data.drop(['RegionID', 'SizeRank', 'StateName'], axis=1)
    data = data[~data.RegionName.duplicated()]
    data = data.melt(id_vars='RegionName')
    data.columns=['Region', 'Month', 'Price']
    persistent_regions = set(data.Region.unique())
    for eset in data.dropna().groupby('Month').Region.unique().apply(set):
        persistent_regions = persistent_regions.difference(persistent_regions.difference(eset))
    data=data[data.Region.isin(persistent_regions)].copy()
    data.index = pd.to_datetime(data.Month)
    data.drop('Month', axis=1, inplace=True)

    return data
    
def plot_housingprices(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    pltdata = data.copy()
    random_regions = np.random.choice(pltdata.Region,10) # Pick 10 random regions
    pltdata = pltdata[pltdata.Region.isin(random_regions)]
    _=sns.lineplot(x='Month', y='Price', data=pltdata, hue='Region',
                marker='o', markersize=2)
    _=plt.legend(loc=1)
    _=plt.title('10 Random Regions House Prices')
    
    

############################## USA HOUSING PRICES ##############################
def process_indiacpi(path):
    
    data = pd.read_csv(path, header=[1])
    data = data.reset_index()
    data = data.drop(['index', 'Group', 'Sub Group', 'Status'], axis=1) # Unrequired Columns
    data = data.dropna(how='all', axis=1)
    data['Month'] = pd.to_datetime(data.Month, format='%B').dt.month
    data['Day'] = '01'
    # Create Date
    data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])
    data.drop(['Year', 'Month', 'Day'], axis=1, inplace=True)

    return data
    
def plot_indiacpi(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    pltdata=data.set_index('Date').copy()
    pltdata=pltdata[pltdata.State.isin(['Delhi', 'Uttar Pradesh'])]
    pltdata=pltdata[pltdata.Description.isin(['Health', 'Meat and fish', 'Spices',
                                        'Clothing and footwear', 'Housing',
                                        'Fuel and light','Vegetables'])]

    _=pltdata.groupby(['State', 'Description']).Combined.plot(legend=True, marker='o', markersize=3)
    _=plt.legend(ncol=2)
    
    
    
    
############################## BRITANNIA STOCK DATA ##############################
def process_britanniastockdata(path):
    
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data = data.dropna()
    return data
    
def plot_britanniastockdata(data, style='ggplot'):
    mpl.plot(data[-50:], figsize=(15,7), type='candle', volume=True, style='mike', title='Candlestick Chart')
    


############################## BEER PRODUCTION DATA ##############################
def process_beerproduction(path):
    
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['MBP']
    return data
    
def plot_beerproduction(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='Monthly Beer Production in Australlia')

############################## AIR PASSENGERS ##############################
def process_airpassengers(path):
    
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['Passengers']
    return data
    
def plot_airpassengers(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(marker='o', markersize=3.5, title='Air Passengers')
    _=plt.ylabel("Air Passengers (1000's)")
    
    
############################## MILK PRODUCTION ##############################
def process_milkprod(path):
    data = pd.read_csv(path, index_col=0)
    data.columns = ['MilkProduction']
    data.index = pd.to_datetime(data.index)
    return data

def plot_milkproduction(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(marker='o', markersize=3.5, title='Milk Production')
    _=plt.ylabel("Milk Production (Pounds per cow)")
    
    
    
    