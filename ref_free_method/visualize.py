import numpy as np
import matplotlib.pyplot as plt
from .ref_free import local_min, local_max, find_error  # Change this to your actual filename (without `.py`)

def visualize(df, column_name='Edis'):
    mins = local_min(df, column_name)
    maxs = local_max(df, column_name)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(df['cell_length'], df[column_name], label='Edis', color='blue')
    ax.scatter(mins['cell_length'], mins[column_name], color='green', label='Local Minima', zorder=5)
    ax.scatter(maxs['cell_length'], maxs[column_name], color='red', label='Local Maxima', zorder=5)

    # Compute points for the line used in error calculation
    abs_max = df[column_name].iloc[-1]
    max_val = max(maxs[column_name])
    min_val = min(mins[column_name])

    min_val_idx = mins[mins[column_name] == min_val].index[0]
    min_length = mins.loc[min_val_idx, 'cell_length']

    max_val_idx = maxs[maxs[column_name] == max_val].index[0]
    x1 = maxs.loc[max_val_idx, 'cell_length']
    y1 = max_val

    # Compute best slope and intercept as in find_error()
    points_after_x1 = df[df['cell_length'] > x1][['cell_length', column_name]]
    max_slope = float('-inf')
    best_x2 = df['cell_length'].iloc[-1]
    best_y2 = df[column_name].iloc[-1]
    for idx, row in points_after_x1.iterrows():
        temp_x2 = row['cell_length']
        temp_y2 = row[column_name]
        temp_slope = (y1 - temp_y2) / (x1 - temp_x2)
        if temp_slope > max_slope:
            max_slope = temp_slope
            best_x2 = temp_x2
            best_y2 = temp_y2

    slope = max_slope
    intercept = best_y2 - slope * best_x2

    if best_y2 < y1:
        slope = 0
        intercept = y1

    # Plot the line
    x_vals = np.array([x1, best_x2])
    y_vals = slope * x_vals + intercept
    ax.plot(x_vals, y_vals, '--', label='Error Reference Line', color='purple')

    # Vertical line to show where error is calculated
    y_at_min_length = slope * min_length + intercept
    ax.plot([min_length, min_length], [min_val, y_at_min_length], 'k--', label='Error')

    error = find_error(df, column_name)
    ax.set_title(f'Local Extrema and Error Visualization\nError = {error:.4f}')
    ax.set_xlabel('cell_length')
    ax.set_ylabel(column_name)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
