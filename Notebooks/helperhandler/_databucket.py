import pandas as pd
from tqdm.notebook import tqdm
from ._individual_funcs import *

############################## DATA PATHS ##############################
# USA Consumption
sunspots_datapath = '../Raw Data/Sunspots.csv'
# USA Consumption
usa_cipsu_datapath = '../Raw Data/USA_CIPSU.csv'
# Consumer Price Index for India with Groups and Subgroups
cpi_datapath = '../Raw Data/cpi_states_and_groups.csv'
# Total Air Passengers
airpassengers_datapath = '../Raw Data/AirPassengers.csv'
# Total Air Passengers
houseprices_datapath = '../Raw Data/Housing_data_prices.csv'
# Australlian Monthly Beer Production
beerprod_datapath = '../Raw Data/Australlian_Monthly_Beer_Production.csv'
# Britannia Stock Prices
britanniastock_datapath = '../Raw Data/BRITANNIA.NS.csv'
# Air Gap Data
airgap_datapath = '../Raw Data/airGap.csv'
# Housing Prices with Missing Data
housepmiss_datapath = '../Raw Data/housing-with-missing-value.csv'
# Monthly Milk production
milkprod_datapath = '../Raw Data/monthly-milk-production-pounds.csv'
# Population and Energy Consumption
popenergy_datapath = '../Raw Data/global_pop_energy.csv'
# USA CPI
usacpi_datapath = '../Raw Data/USA_CPI.csv'
# AntiDiabetic DrugSales
antidiabetic_datapath = '../Raw Data/AntiDiabetic_DrugSales_Mn.csv'
# Australlian Electricity Priduction
elecprod_datapath = '../Raw Data/Australlian_Monthly_Electricity_Production_BillionKWh.csv'
# AntiDiabetic DrugSales
antidiabetic_datapath = '../Raw Data/AntiDiabetic_DrugSales_Mn.csv'
# Australlian Visitors
visitors20r_datapath = '../Raw Data/Australlia_Vistors_20Regions_Million.csv'


class DataProcessingClass:
    def __init__(self, raw_datapath, long_desc, short_desc, processing_func, plotfunc):
        self.rpath = raw_datapath
        self.long_description = long_desc
        self.short_description = short_desc
        self._processing_func = processing_func
        self._plot_func = plotfunc
        
        self.data = None
        
    def run_processingfunc(self):
        self.data = self._processing_func(self.rpath)
        
    def exploratory_plot(self):
        self._plot_func(self.data, style='dark_background')
        

class DataHolderClass:
    def __init__(self):
        self.bucket = {}
        self.dataDf = pd.DataFrame(columns=['Handle', 'Short Description'])
        
    def add_data(self, data_key, dpc_ob):
        self.bucket[data_key] = dpc_ob
        self.dataDf = self.dataDf.append({'Handle':data_key,
                                          'Short Description':dpc_ob.short_description},
                                          ignore_index=True)

    def load_data(self):
        for _, edpc in tqdm(self.bucket.items()):
            edpc.run_processingfunc()
            
            
            
            
dpc1 = DataProcessingClass(raw_datapath=airpassengers_datapath, 
                           long_desc = """Air Passengers (Monthly), Numbers in 1000's, from 1949 to 1960""",
                           short_desc = "Air Passengers",
                           processing_func = process_airpassengers,
                           plotfunc = plot_airpassengers)


dpc2 = DataProcessingClass(raw_datapath=milkprod_datapath, 
                           long_desc = """Milk production (Monthly), Numbers in pounds per cow, from 1962 to 1975""",
                           short_desc = "Milk Production",
                           processing_func = process_milkprod,
                           plotfunc = plot_milkproduction)

dpc3 = DataProcessingClass(raw_datapath=britanniastock_datapath, 
                           long_desc = """Britannia's Stock Data (Buisness Daily), including Open, High, Low, Close & Volume of the Ticker, from 1996 to 2020""",
                           short_desc = "Britannia Stock Price",
                           processing_func = process_britanniastockdata,
                           plotfunc = plot_britanniastockdata)


dpc4 = DataProcessingClass(raw_datapath=cpi_datapath, 
                           long_desc = """India's Consumer Price index Data (Monthly), with groups and subgroups starting from 2013 to 2020""",
                           short_desc = "India CPI",
                           processing_func = process_indiacpi,
                           plotfunc = plot_indiacpi)


dpc5 = DataProcessingClass(raw_datapath=beerprod_datapath, 
                           long_desc = """Australlian Beer Production (Monthly), from , Numbers in Million Barrels, from 1956 to 1995""",
                           short_desc = "Beer Production",
                           processing_func = process_beerproduction,
                           plotfunc = plot_beerproduction)


dpc6 = DataProcessingClass(raw_datapath=houseprices_datapath, 
                           long_desc = """USA Housing Prices Data (Monthly), prices in $, from 2008 to 2020""",
                           short_desc = "Housing Prices",
                           processing_func = process_housingprices,
                           plotfunc = plot_housingprices)

dpc7 = DataProcessingClass(raw_datapath=airgap_datapath, 
                           long_desc = """Air Passengers (Monthly) with Missing Values, Numbers in 1000's, from 1949 to 1960""",
                           short_desc = "Air Passengers - Missing",
                           processing_func = process_airpassengersgap,
                           plotfunc = plot_airpassengersgap)


dpc8 = DataProcessingClass(raw_datapath=housepmiss_datapath, 
                           long_desc = """Housing Data with Missing Values""",
                           short_desc = "Housing Data - Missing",
                           processing_func = process_housinggap,
                           plotfunc = plot_housinggap)


dpc9 = DataProcessingClass(raw_datapath=popenergy_datapath, 
                           long_desc = """Global Population and Energy Consumption across various segments (Yearly), Enegry in kWh, from 1960 to 2016""",
                           short_desc = "Population & Energy",
                           processing_func = process_popenergy,
                           plotfunc = plot_popenergy)

dpc10 = DataProcessingClass(raw_datapath=usacpi_datapath, 
                           long_desc = """USA Consumer Price Index (Monthly), from 2007 to 2020""",
                           short_desc = "USA-CPI",
                           processing_func = process_usacpi,
                           plotfunc = plot_usacpi)


dpc11 = DataProcessingClass(raw_datapath=antidiabetic_datapath, 
                           long_desc = """Anti-Diabetic Drug Sales (Monthly), prices in $ Million, from 1992 to 2008""",
                           short_desc = "AntiDiabetic Drug Sale",
                           processing_func = process_antidiabeticdrugs,
                           plotfunc = plot_antidiabeticdrugs)

dpc12 = DataProcessingClass(raw_datapath=elecprod_datapath, 
                           long_desc = """Australlian Electricity Production (Monthly) with Missing Values, Numbers in billion kWh, from 1956 to 1995""",
                           short_desc = "Electricity Production",
                           processing_func = process_electricityprod,
                           plotfunc = plot_electricityprod)


dpc13 = DataProcessingClass(raw_datapath=visitors20r_datapath, 
                           long_desc = """Number of Visitors in 20 Regions of Australlia (Quaterly), in Million, from 1998 to 2016""",
                           short_desc = "Visitors to 20 Regions",
                           processing_func = process_20rvisitors,
                           plotfunc = plot_20rvisitors)

dpc14 = DataProcessingClass(raw_datapath=usa_cipsu_datapath, 
                           long_desc = """USA Economic Numbers  (Quaterly), in Million, from 1970 to 2016""",
                           short_desc = "USA Economic Numbers",
                           processing_func = process_usaeconomic,
                           plotfunc = plot_usaeconomic)
dpc15 = DataProcessingClass(raw_datapath=sunspots_datapath, 
                           long_desc = """Monthly Mean of Sunspots observed (Monthly), from 1749-01 to 2019-12""",
                           short_desc = "Sunspot Numbers",
                           processing_func = process_sunspots,
                           plotfunc = plot_sunspots)

    
dataHolder = DataHolderClass()
dataHolder.add_data(data_key='airp_data', dpc_ob=dpc1)
dataHolder.add_data(data_key='mprod_data', dpc_ob=dpc2)
dataHolder.add_data(data_key='brit_stock', dpc_ob=dpc3)
dataHolder.add_data(data_key='india_cpi', dpc_ob=dpc4)
dataHolder.add_data(data_key='beer_prod', dpc_ob=dpc5)
dataHolder.add_data(data_key='house_price', dpc_ob=dpc6)
dataHolder.add_data(data_key='airp_data_missing', dpc_ob=dpc7)
dataHolder.add_data(data_key='housing_missing', dpc_ob=dpc8)
dataHolder.add_data(data_key='pop_ener', dpc_ob=dpc9)
dataHolder.add_data(data_key='usa_cpi', dpc_ob=dpc10)
dataHolder.add_data(data_key='anti_diabetic', dpc_ob=dpc11)
dataHolder.add_data(data_key='aus_elecprod', dpc_ob=dpc12)
dataHolder.add_data(data_key='visitor_20r', dpc_ob=dpc13)
dataHolder.add_data(data_key='usa_economic', dpc_ob=dpc14)
dataHolder.add_data(data_key='sunspots', dpc_ob=dpc15)


