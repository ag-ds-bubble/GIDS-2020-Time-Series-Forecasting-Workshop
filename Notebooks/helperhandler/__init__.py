from ._databucket import dataHolder

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss
from warnings import filterwarnings
filterwarnings('ignore')
import copy
from IPython.display import display

def get_ts_strength(decomp_obj):
    
    tt = decomp_obj.trend
    st = decomp_obj.seasonal
    rt = decomp_obj.resid
    
    trend_strength = np.var(rt)/np.var(tt+rt)
    trend_strength = max([0, 1-trend_strength])

    seasonal_strength = np.var(rt)/np.var(st+rt)
    seasonal_strength = max([0, 1-seasonal_strength])
    
    sdf = pd.DataFrame([trend_strength, seasonal_strength],
                         columns=['Strength'], index=['Trend', 'Seasonal'])
    
    return sdf

def adf_test(timeseries, autolag='AIC',**kwargs):
    dftest = adfuller(timeseries, autolag=autolag, **kwargs)
    df = pd.Series(dftest[0:4],
                   index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        df['Critical Value (%s)'%key] = value
    return df.to_frame()

def kpss_test(timeseries, regression='c', nlags="auto", **kwargs):
    kpsstest = kpss(timeseries, regression=regression, nlags=nlags, **kwargs)
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    return kpss_output.to_frame()


def plot_diagnostics():
    pass



def ro_framework(data, model, model_params, 
                 target_col, feature_cols,
                 test_start, cv_window, ahead_offest,
                 metric='MAPE', debug=True, ahead_offest_freq='days'):
    # Three libraries - statsmodels, sklearn, prophet
    
    # Checks
    _tfreq = ['years', 'months', 'weeks', 'days', 'hours', 'minutes',
              'seconds', 'microseconds', 'nanoseconds']
    if not (hasattr(model, 'fit') & hasattr(model, 'predict')):
        raise ValueError("Model Passed should be having '.fit' & '.predict' methods, i.e foloowing the sklearn API")
    if data.shape[0]<10:
        raise ValueError("Data used for modelling should be greater than 10 datapoints")
    if type(data) != pd.core.frame.DataFrame:
        raise ValueError("Data should be a pandas dataframe of type 'pd.DataFrame'")
    if type(data.index) != pd.core.indexes.datetimes.DatetimeIndex:
        raise ValueError("Data should be having index of type 'pd.DatetimeIndex'")
    if not (type(test_start) == str or type(test_start) == pd._libs.tslibs.timestamps.Timestamp):
        raise ValueError("'test_start' should be a 'pd.Timestamp' or 'str'")
    if not (pd.to_datetime(test_start)>data.index[0] and pd.to_datetime(test_start)<data.index[-1]):
        raise ValueError("'test_start' should be in between {0} and {1}".format(data.index.min(),
                                                                                data.index.max()))
    if not type(ahead_offest) == pd._libs.tslibs.offsets.DateOffset:
        raise ValueError("'ahead_offest' should be a 'pd.DateOffset'")
    if type(cv_window) != int:
        raise ValueError("'cv_window' should be an `int`")
    if not any([ahead_offest_freq==k for k in _tfreq]):
        raise ValueError(f"'ahead_offest_freq' should be one of {_tfreq}")
    if getattr(ahead_offest, ahead_offest_freq) <= 0:
        raise ValueError(f"'ahead_offest' should be greater than `0 {ahead_offest_freq}`")
    if target_col not in data.columns:
        raise ValueError(f"{target_col} not found in `data`")
    if feature_cols:
        missing_feats = [k for k in feature_cols if k not in data.columns]
        if missing_feats:
            raise ValueError(f"{missing_feats} columns not present in the dataset")
    if data.index.freq == None:
        raise ValueError(f"data.index.freq should not be `None`")

    # Initialisations
    cvDF = pd.DataFrame(columns = ['Actual', 'Forecast', metric])
    testDF = pd.DataFrame(columns=['Actual', 'Forecast', metric])
    
    model = copy.deepcopy(model)
    
    modelling_data = data.copy()
    modelling_data.sort_index(inplace=True)
    
    training_data = data[data.index<test_start].copy()
    testing_data = data[data.index>=test_start].copy()

    train_start = training_data.index[0]
    
    test_start = pd.to_datetime(test_start)
    test_end = modelling_data.index[-1]
    
    if cv_window > training_data.shape[0]*0.5:
        raise ValueError("`cv_window` should be less than {}".format(int(training_data.shape[0]*0.5)))
    
    
    
    # Fore debugging purpose
    if debug:
        debugDF = pd.DataFrame(columns=['Train Start', 'Train End', 'CV Point', 'Diff'])
        for cv_date in training_data.index[-cv_window:]:
            train_end = cv_date-ahead_offest
            _packet = {'Train Start': train_start, 'Train End': train_end,
                       'CV Point': cv_date, 'Diff': str(getattr(ahead_offest, ahead_offest_freq))+' '+ahead_offest_freq}
            debugDF = debugDF.append(_packet, ignore_index=True)
        display(debugDF)
    
    
    # Picking the Metrics
    if metric == 'MAPE':
        metric_func = lambda y,yhat: np.round(100*(abs(np.array(y)-np.array(yhat))/np.array(y)),2)
    elif metric == 'MSE':
        metric_func = lambda y,yhat: np.round(100*(abs(np.array(y)-np.array(yhat))/np.array(y)),2)
    
    
    # Cross Validation Loop
    for cv_date in training_data.index[-cv_window:]:
        train_end = cv_date-ahead_offest
        
        # Filter the data
        _train_data = training_data.truncate(before=train_start, after=train_end)
        _cv_data = training_data.loc[cv_date].to_frame().T
        
        if feature_cols:
            # Multivariate
            pass
        else:
            # Univariate
            if 'statsmodels' in str(model):
                # Update Model Params Based on library
                model_params['endog'] = _train_data[target_col]
                modeldef = model(**model_params)
                
                fitted_model = modeldef.fit()
                _forecast = fitted_model.predict(start=cv_date, end=cv_date).values[0]
                _actual = _cv_data[target_col].values[0]

        # Update Metric Sheets
        cvDF.loc[cv_date, 'Actual'] = _actual
        cvDF.loc[cv_date, 'Forecast'] = _forecast
        cvDF.loc[cv_date,  metric] = metric_func(_actual, _forecast)
    
    
    # Testing - Using the last fitted_model
    if 'statsmodels' in str(model):
        testDF['Actual'] = testing_data[target_col]
        testDF['Forecast'] = fitted_model.predict(start=test_start, end=test_end)
        testDF[metric] = testDF.apply(lambda x : metric_func(x.Actual, x.Forecast), axis=1)
    
    # Prepare Overall Metric
    overallDF = pd.DataFrame([cvDF[metric].mean(), testDF[metric].mean()],
                             columns=['Overall '+metric],
                             index=['CV', 'Test'])
    
    return cvDF, testDF, overallDF, fitted_model

