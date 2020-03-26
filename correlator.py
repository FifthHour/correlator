from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Button
from bokeh.layouts import row, column, gridplot
from bokeh.plotting import figure

import numpy as np
from scipy.ndimage.filters import uniform_filter1d

# initialise data structures
start_val = 0
global r_lookback
r_lookback = -20

data = {'x': [0],
        'y': [start_val],
        'y2': [start_val],
        'dev': [0],
        'pearson': [0],
        'lma': [0],
        'sma': [0]}

source = ColumnDataSource(data)

# set up figures and widgets
button = Button(label='Go', button_type='success')

tools='xbox_select, box_zoom, wheel_zoom, pan, reset, save'

p1 = figure(plot_width=1000, plot_height=350, title='Timeseries', tools=tools)
p1.circle(x='x', y='y', alpha=0.6, color=None ,source=source, selection_color='Orange')
p1.line(x='x', y='y', alpha=0.6, color='Navy', source=source, legend_label='y1')
p1.line(x='x', y=start_val, color='DarkGrey', source=source)
p1.circle(x='x', y='y2', alpha=0.6, color=None ,source=source, selection_color='Orange')
p1.line(x='x', y='y2', alpha=0.6, color='Firebrick', source=source, legend_label='y2')
p1.legend.location = 'top_left'

p2 = figure(plot_width=800, plot_height=250, title='Std_Dev', tools=tools, x_range=p1.x_range)
p2.circle(x='x', y='dev', color=None, alpha=0.6, source=source)
p2.line(x='x', y='dev', color='Orange', alpha=0.6, source=source)

p3 = figure(plot_width=800, plot_height=250, title="MAs", tools=tools, x_range=p1.x_range,
            y_range=p1.y_range)
#p3.circle(x='x', y='lma', color='Firebrick', alpha=0.6, source=source)
p3.line(x='x', y='lma', color='Black', alpha=0.6, source=source)
#p3.circle(x='x', y='sma', color='Grey', alpha=0.6, source=source)
p3.line(x='x', y='sma', color='Grey', alpha=0.6, source=source)

y_corr = figure(plot_width=400, plot_height=400, title='Corr', tools=tools)
y_corr.circle('y', 'y2', source=source, selection_color='Orange')

pearson = figure(plot_width=1000, plot_height=350, title=('y1/y2 pearson r: lookback ' + str(r_lookback)), tools=tools, x_range=p1.x_range)
pearson.circle(x='x', y='pearson', color='Peru', alpha=0.4, source=source, selection_color='Orange')
pearson.line(x='x', y='pearson', color='Peru', alpha=0.6, source=source)
pearson.line(x='x', y=start_val, color='DarkGrey', source=source)

def animate_update():
    # y values:
    last_y = data['y'][-1]
    new = last_y + np.random.normal()
    data['y'].append(new)

    # y2 values
    last_y2 = data['y2'][-1]
    new = last_y2 + np.random.normal()
    data['y2'].append(new)

    # x index values
    nx = data['x'][-1] + 1
    data['x'].append(nx)
    
    # dev values
    nd = np.std(data['y'])
    data['dev'].append(nd)
    
    # LMA values
    nlma = np.mean(data['y'][-100:])
    data['lma'].append(nlma)

    # SMA values
    nsma = np.mean(data['y'][-20:])
    data['sma'].append(nsma)

    # pearson
    r = np.corrcoef(data['y'][r_lookback:],data['y2'][r_lookback:])
    r_val = r[0,1]
    data['pearson'].append(r_val)

    source.data = data

callback_id = None

def animate():
    global callback_id
    if button.label == 'Go':
        button.label = 'Stop'
        callback_id = curdoc().add_periodic_callback(animate_update, 100)
    else:
        button.label = 'Go'
        curdoc().remove_periodic_callback(callback_id)

button.on_click(animate)

plot_layout = column(button,gridplot([[p1], [pearson]],toolbar_location='right'))

curdoc().add_root(plot_layout)
curdoc().title = 'Timeseries correlation'


