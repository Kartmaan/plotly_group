import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from IPython.display import Image

def plot_group(series, title='', x_label='', y_label='', 
    intervals=None, higher_vals=False, kind='bar', grid=False,
    bar_color='#1776f2', output='fig'):
    """ 
    Group values from a Pandas Series according to given 
    intervals and represent them graphically in the form of 
    bar chart or pie chart.

    PARAMETERS INFO :
    
    series : must be a Pandas Series containing int/float numbers
    
    title : plot title

    x_label : x axis label

    y_label : x axis label

    intervals : intervals for value grouping, must be a list 
    containing lists of value pairs (example: [[0,5], [5,10],...])
    if None default intervals will be offered. (default =  None)

    higher_vals : an interval will be added for all values greater 
    than the last interval (default = False)

    kind : plot kind, 'bar' for bar chart, 'pie' for pie chart
    (default = 'bar')

    grid : show grid True/False 
    (only for bar chart, default = False)

    bar_color : bar chart color, can be RGB values 
    (tuple, list or 'rgb(255,255,255)', hexadecimal value (#str) 
    or a css color name (str lowercase). (default = '#1776f2')

    output : 
    'img' : returns non-interactive image (need plotly-orca)
    'bytes' : returns image in bytes (need plotly-orca)
    'fig' : returns interactive Plotly figure (default)
    'fig_obj' : returns Plotly Figure object (contained in a variable)
    """

    # -------------- SERIES CHECK --------------
    if not isinstance(series, pd.core.series.Series):
        raise TypeError("'series' must be a Pandas Series, "+
        f"{type(series)} given")
    
    else:
        series = series.dropna()

        for idx, val in enumerate(series.values):
            if not isinstance(val, (int, float, np.int32,
            np.int64, np.float32, np.float64)):
                raise ValueError('Series values must only '+
                f'contain int or float, {type(val)} '+ 
                f'given at index {idx}')
            else:
                continue
    
    # -------------- BAR COLOR CHECK --------------
    # The color of the bars (if 'kind' = 'bar') 
    # can be presented in different ways: 
    # as an iterable (list or tuple) when dealing with RGB values
    # or as str when dealing with hexadecimal values ('#b4522b'),
    # rgb values ('rgb(125,45,32)') or css color name

    # Wrong type
    if not isinstance(bar_color, (tuple, list, str)):
        raise TypeError('bar_color must be a tuple, list or str,'+
        f'{type(bar_color)} given')
    
    # Type is iterable
    # By default Plotly's RGB values should be presented as 
    # 'rgb(125,45,32)', however, in this function we allow 
    # them to be iterable as list or tuple
    elif isinstance(bar_color, (tuple, list)):

        # Wrong length
        if len(bar_color) != 3:
            raise ValueError('Iterable must contain 3 RGB values,'+
            f' {len(bar_color)} given')

        # RGB values control
        boo = []
        for val in bar_color:
            if isinstance(val, int) and 0 <= val <= 255:
                boo.append(True)
            else:
                boo.append(False)
        
        # Correct RGB
        if all(boo):
            if isinstance(bar_color, tuple):
                bar_color = f"rgb{str(bar_color)}"
            else:
                bar_color = tuple(bar_color)
                bar_color = f"rgb{str(bar_color)}"
        
        # Wrong RGB
        else:
            raise ValueError('Wrong RGB format, must be '+
            '3 int values between 0 and 255')

    # Type is str
    # At this point the color can either be of hexadecimal type 
    # (example: '#b4522b'), or of type 'rgb(125,45,32)' 
    # or a css color name (in lower case). In case of error 
    # the Plotly module will display them
    else:
        pass

    # -------------- DEFAULT INTERVALS --------------
    # User has not specified custom intervals 
    # (intervals is None) : so default intervals will be defined, 
    # based on the values from the provided Pandas Series.
    #
    # To define the intervals adaptively and taking into account 
    # the dispersion, we calculate the 80th percentile of the 
    # values of the Pandas Series and divide this value by the 
    # number of intervals (5), thus, 80% of the most represented 
    # values will appear in the first 5 slices, the remaining 20% 
    # will be added to a 6th and last slice thanks to the 
    # activation of the 'higher_vals' parameter. The result of 
    # this division is rounded up to the next hundred by the 
    # lambda function
    # 
    # If the maximum value of the Series is less than the 
    # number of intervals (data with small values), we simply 
    # divide the value maximum value by the number of intervals, 
    # without using the roundup function (but still rounding 
    # the results to 3 digits after the decimal point to avoid 
    # displaying texts that are too long on the x axis)

    if intervals is None:
        percent = np.percentile(series.values, 80)
        nbr_of_intervals = 5

        roundup = lambda x : int(ceil(x/100)) * 100

        if percent > nbr_of_intervals:
            interval_unit = roundup(percent/nbr_of_intervals)
            higher_vals = True
        else:
            interval_unit = round(percent/nbr_of_intervals, 3)
            higher_vals = True

        intervals = []
        frm = 0
        to = interval_unit

        while len(intervals) < nbr_of_intervals:
            itrvl = [frm, to]
            intervals.append(itrvl)
            if percent > nbr_of_intervals:
                frm = frm+interval_unit
                to = to+interval_unit
            else:
                frm = round(frm+interval_unit, 3)
                to = round(to+interval_unit, 3)
        
        intervals = np.array(intervals)

    # -------------- INTERVALS CHECK --------------
    # A custom intervals has been defined, verification is needed
    else:
        # Not a list
        if not isinstance(intervals, list):
            raise TypeError('intervals must be a list, ' + 
            f'{type(intervals)} given')

        # Iterating intervals looking for errors
        for idx, val in enumerate(intervals):

            # One of the elements isn't a list
            if not isinstance(val, list):
                raise TypeError('intervals must only contains lists '+
                f'{type(intervals[idx])} given at index {idx} \n'+
                f'--> {intervals[idx]}')

            # One sublist doesn't have a length of 2
            elif not len(val) == 2:
                raise TypeError('An interval must contain 2 values '+
                f'{len(intervals[idx])} given at index {idx} \n'+
                f'--> {intervals[idx]}')

            # One sublist does not contain a valid number
            elif not isinstance(val[0], (int, float)) or \
                not isinstance(val[1], (int, float)):
                raise ValueError('An interval must contain 2 numbers, '+
                f'int or float. --> {intervals[idx]} at index {idx}')
            
            # The 2nd value isn't greater than the 1st
            elif not val[0] < val[1]:
                raise ValueError('The 2nd value of an interval '+
                'must be greater than the 1st \n'+
                f'--> {intervals[idx]} at index {idx}')
            
            # Everything is OK
            else:
                intervals = np.array(intervals)

    # -------------- GROUPING --------------
    # The validity of custom intervals has been ensured, 
    # the grouping can begin. 
    # For this operation, we create a dictionary which 
    # will contain as key the title of each interval in the form of 
    # str (example: '5-10'), and as values a list containing: 
    # (idx 0) : The numpy array containing all the values of the 
    # desired interval (Not used in this function but still 
    # recovered to adapt to future needs). 
    # (idx 1) : The length of this numpy list

    intervals_dict = {}

    # Series values are filtered according to each interval 
    # of 'intervals' and the informations stored in the dictionary
    for itrvl in intervals:
        part = series.loc[lambda x : (x > itrvl[0]) & (x <= itrvl[1])]
        part = np.array(part.values)
        
        intervals_dict[f'{itrvl[0]}-{itrvl[1]}'] = [part, len(part)]
    
    if higher_vals:
        part = series.loc[lambda x : x > intervals[-1][1]]
        part = np.array(part.values)

        intervals_dict[f'+{intervals[-1][1]}'] = [part, len(part)]        
    
    # -------------- PLOTING --------------
    x = []
    y = []

    # Creation of the x and y axes according to the information 
    # obtained from the dictionary
    for key, val in intervals_dict.items():
        x.append(key)
        y.append(val[1])
    
    # Bar chart
    if kind == 'bar':
        fig = px.bar(
            x=x, 
            y=y,
            title=title,
            labels={'x': x_label, 'y': y_label},
            text_auto='.5'
            )
    
        fig.update_traces(
            marker_color=bar_color
            )
        
        if grid:
            fig.update_yaxes(showgrid=True, gridcolor='black',
            gridwidth=0.5)

    # Pie chart
    elif kind == 'pie':
        fig = go.Figure(data=[go.Pie(
            labels=x, 
            values=y,
            hole=.5
            )])
        
        fig.update_layout(
            title_text = f'{title}')

    # Wrong input in 'kind' parameter
    else:
        raise NameError(
            'Wrong "kind" parameter, please check parameter')
    
    # -------------- OUTPUT --------------
    # The output can take several forms:

    # output = 'img': Static image (non-interactive), requires 
    # the plotly-orca module

    # output = 'bytes': Image in bytes format, requires 
    # the plotly-orca module

    # output='fig': Interactive Plotly Figure

    # output = 'fig_obj': Figure Object

    if output == 'img' or output == 'bytes':
        img_bytes = pio.to_image(
            fig,
            format='png',
            validate=True,
            engine='orca'
        )

        # Output : static image
        if output == 'img':
            return Image(img_bytes)
        
        # Output : bytes type image
        else:
            return img_bytes

    # Output : Interactive plotly figure
    elif output == 'fig':
        return fig.show()

    # Output : Return a plotly Figure object
    elif output =='fig_obj':
        return fig
    
    # Wrong input for 'output' parameter
    else:
        raise NameError('Unrecognized "output" parameter')