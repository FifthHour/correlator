from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Button, Slider
from bokeh.layouts import row, column, gridplot
from bokeh.plotting import figure

import numpy as np

start_val = 0

# set up data structures
data = {'x': [0],
        'y1': [start_val],
        'y2': [start_val],
        'pearson': [0],
        'y1_lma': [0],
        'y1_sma': [0],
        'y2_lma': [0],
        'y2_sma': [0]}

source = ColumnDataSource(data)

# set up figures and widgets
button = Button(label='Go', button_type='success')
r_slider = Slider(title='r lookback', value=20, start=5, end=100,step=-5)
lma_slider = Slider(title='LMA length', value=100, start=20, end=200, step=5)
sma_slider = Slider(title='SMA length', value=20, start=5, end=100, step=5)

tools='xbox_select, box_zoom, wheel_zoom, pan, reset, save'

# initialise start values

# global r_lookback
# r_lookback = r_slider.value

# timeseries data chart
p1 = figure(plot_width=1000, plot_height=350, title='Timeseries', tools=tools)

p1.circle(x='x', y='y1', alpha=0.6, color=None ,source=source, selection_color='Orange')
p1.line(x='x', y='y1', alpha=0.6, color='Blue', source=source, legend_label='y1')
p1.circle(x='x', y='y2', alpha=0.6, color=None ,source=source, selection_color='Orange')
p1.line(x='x', y='y2', alpha=0.6, color='Red', source=source, legend_label='y2')
p1.line(x='x', y=start_val, color='DarkGrey', source=source)

p1.legend.location = 'top_left'
p1.legend.click_policy = 'hide'

# pearson r chart
pearson = figure(plot_width=1000, plot_height=350, title='y1/y2 pearson r', tools=tools, x_range=p1.x_range)

pearson.circle(x='x', y='pearson', color='Peru', alpha=0.4, source=source, selection_color='Orange')
pearson.line(x='x', y='pearson', color='Peru', alpha=0.6, source=source)

pearson.line(x='x', y=start_val, color='DarkGrey', source=source)

# MA chart
ma = figure(plot_width=1000, plot_height=350, title='Moving Averages', tools=tools, x_range=p1.x_range, y_range=p1.y_range)

ma.line(x='x', y='y1_lma', alpha=0.6, color='Navy', source=source, legend_label='y1 LMA')
ma.line(x='x', y='y1_sma', alpha=0.8, color='LightBlue', source=source, legend_label='y1 SMA')
ma.line(x='x', y='y2_lma', alpha=0.6, color='DarkRed', source=source, legend_label='y2 LMA')
ma.line(x='x', y='y2_sma', alpha=0.8, color='LightPink', source=source, legend_label='y2 SMA')

ma.circle(x='x', y='y1_lma', alpha=0.6, color=None, source=source, legend_label='y1 LMA', selection_color='Orange')
ma.circle(x='x', y='y1_sma', alpha=0.8, color=None, source=source, legend_label='y1 SMA', selection_color='Orange')
ma.circle(x='x', y='y2_lma', alpha=0.6, color=None, source=source, legend_label='y2 LMA', selection_color='Orange')
ma.circle(x='x', y='y2_sma', alpha=0.8, color=None, source=source, legend_label='y2 SMA', selection_color='Orange')

ma.legend.location = 'top_left'
ma.legend.click_policy = 'hide'

def animate_update():

    # x index values
    nx = data['x'][-1] + 1
    data['x'].append(nx)

    # y1 values:
    last_y1 = data['y1'][-1]
    new = last_y1 + np.random.normal()
    data['y1'].append(new)

    # y2 values
    last_y2 = data['y2'][-1]
    new = last_y2 + np.random.normal()
    data['y2'].append(new)

    # get LMA and SMA slider values: get slider value and flip to negative
    LMA_len = int(lma_slider.value) * -1
    SMA_len = int(sma_slider.value) * -1

    # y1 LMA values
    n_y1_lma = np.mean(data['y1'][LMA_len:])
    data['y1_lma'].append(n_y1_lma)

    # y1 SMA values
    n_y1_sma = np.mean(data['y1'][SMA_len:])
    data['y1_sma'].append(n_y1_sma)

    # y2 LMA values
    n_y2_lma = np.mean(data['y2'][LMA_len:])
    data['y2_lma'].append(n_y2_lma)

    # y2 SMA values
    n_y2_sma = np.mean(data['y2'][SMA_len:])
    data['y2_sma'].append(n_y2_sma)

    # pearson
    r_lookback = int(r_slider.value) * -1
    r = np.corrcoef(data['y1'][r_lookback:],data['y2'][r_lookback:])
    r_val = r[0,1]
    data['pearson'].append(r_val)

    source.data = data

callback_id = None

def animate():
    global callback_id
    if button.label == 'Go':
        button.label = 'Stop'
        callback_id = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = 'Go'
        curdoc().remove_periodic_callback(callback_id)

button.on_click(animate)

plot_layout = column(button, gridplot([[p1], [r_slider], [pearson], [sma_slider], [lma_slider], [ma]],toolbar_location='right'))

curdoc().add_root(plot_layout)
curdoc().title = 'FH Correlator'


