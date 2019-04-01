def heatingAndCoolingDegreeDays(filename, referenceTemperature):
    """
    This function calculates the number of heating and cooling degree days
    for contam weather files. This is done for each hour of the year.
    
    Input:
        filename - name of the contam weather file to process
        referenceTemperature - temperature to reference the degree days to (C)
                                (This is usually 18.3 C, or 65 F.)
    Created on Thu Feb 28 15:11:18 2019
    
    @author: Von P. Walden, Washington State University
    """
    import pandas as pd
    
    # Convert reference temperature to K.
    referenceTemperature = referenceTemperature + 273.15
    
    # Read the contam weather file.
    year = filename.split('_')[1]
    wth  = pd.read_csv(filename, skiprows=371, header=0, sep='\t', names=['Date','Time','Ts','Ps','Ws','Wd','HRs','Ith','Idn','Tsfc','Rn','Sn'])
    wth.index = [pd.to_datetime(year + '/' + row[1].Date + ' ' + row[1].Time) for row in wth.iterrows()]
    
    # Compute the heating and cooling degree days.
    HDD = -wth.Ts[wth.Ts<referenceTemperature] + referenceTemperature
    CDD =  wth.Ts[wth.Ts>referenceTemperature] - referenceTemperature
    
    return HDD, CDD
