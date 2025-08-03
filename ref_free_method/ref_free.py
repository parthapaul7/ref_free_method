import pandas as pd
import numpy as np

def local_min(df, column_name='Edis'):
    y = df[column_name].values
    x = df['cell_length'].values
    
    # Second derivative approximation: +1 means a local minimum
    minima_mask = np.diff(np.sign(np.diff(y))) > 0
    indices = np.where(minima_mask)[0] + 1  # offset by 1 due to diff

    if len(indices) == 0:
        print('No local minima found')
        new_df = pd.DataFrame(columns=['cell_length', column_name])
        new_df.loc[0] = [0, 0]
        return new_df

    return df.iloc[indices][['cell_length', column_name]].reset_index(drop=True)

def local_max(df, column_name='Edis'):
    y = df[column_name].values
    x = df['cell_length'].values
    
    # Second derivative approximation: -1 means a local maximum
    maxima_mask = np.diff(np.sign(np.diff(y))) < 0
    indices = np.where(maxima_mask)[0] + 1  # offset by 1 due to diff

    if len(indices) == 0:
        print('No local maxima found')
        new_df = pd.DataFrame(columns=['cell_length', column_name])
        new_df.loc[0] = [0, 0]
        return new_df

    return df.iloc[indices][['cell_length', column_name]].reset_index(drop=True)



def find_error(df, column_name='Edis'):
    abs_max = df[column_name].iloc[-1]
    max_val = max(local_max(df)[column_name])
    min_val = min(local_min(df)[column_name])
    min_val_idx = local_min(df)[local_min(df)[column_name] == min_val].index[0]
    min_length = local_min(df).loc[min_val_idx, 'cell_length']

    max_val_idx = local_max(df)[local_max(df)[column_name] == max_val].index[0]

    # equation of line between two points (x1, y1) and (x2, y2)
    x1 = local_max(df).loc[max_val_idx, 'cell_length'] 
    x2 = df['cell_length'].iloc[-1]

    y1 = max_val
    y2 = abs_max
    # print(min_length)
    
    # Finding the maximum slope
    max_slope = float('-inf')
    best_x2 = x2
    best_y2 = y2
    
    # Get the dataframe points after x1
    points_after_x1 = df[df['cell_length'] > x1][['cell_length', 'Edis']]
    
    # Iterate through all points after x1
    for idx, row in points_after_x1.iterrows():
        temp_x2 = row['cell_length']
        temp_y2 = row['Edis']
        temp_slope = (y1 - temp_y2) / (x1 - temp_x2)
        
        if temp_slope > max_slope:
            max_slope = temp_slope
            best_x2 = temp_x2
            best_y2 = temp_y2
    
    x2 = best_x2
    y2 = best_y2
    slope = max_slope
    intercept = y2 - slope * x2

    if y2 < y1:
        slope = 0
        intercept = y1

    #value of y when x = min_length
    y_at_min_length = slope * min_length + intercept

    diff = abs(min_val - y_at_min_length)
    return diff