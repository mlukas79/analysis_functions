""" A collection of functions to facilitate data analysis and visualisation.
"""
import plotly
import colorlover

def plotter3d(df, plot_title, kwargs=None):
    """Returns a plotly 3d plot
    """
    
    PARAMETERS = {
    'plot_title': 's',
    'x': 'compensation',
    'x_units': 'Td',
    'y': 'av_disp',
    'y_units': 'Td',
    'z': 'height',
    'z_units': 'pA',
    'groupvar': 'band',
    'groupvar_values': [0,1,2,3,4,5,6,7,8],
    }
    
    if kwargs is None:
        kwargs = PARAMETERS
    traces = []
    #colors = colorlover.to_rgb(colorlover.scales[str(len(kwargs['groupvar_values']).unique())]['div']['RdBu'] )
    for j, i in enumerate(kwargs['groupvar_values'].unique()):
        trace = plotly.graph_objs.Scatter3d(
        x = getattr(df[df[kwargs['groupvar']]==i],kwargs['x']),
        y = getattr(df[df[kwargs['groupvar']]==i],kwargs['y']),
        z = getattr(df[df[kwargs['groupvar']]==i],kwargs['z']),
        mode='markers',
        marker=dict(size=5,
                    line=dict(width=1),
                    #color=colors[j]
                   ),
        name=f"{kwargs['groupvar']} {i}",
        )
        traces.append(trace)

    layout_comp = plotly.graph_objs.Layout(
        title= plot_title,
        hovermode='closest',
        scene=plotly.graph_objs.Scene(
            xaxis=plotly.graph_objs.XAxis(title='{}{}{}'.format(kwargs['x'],' ',kwargs['x_units'])),
            yaxis=plotly.graph_objs.YAxis(title='{}{}{}'.format(kwargs['y'],' ',kwargs['y_units'])),
            zaxis=plotly.graph_objs.ZAxis(title='{}{}{}'.format(kwargs['z'],' ',kwargs['z_units'])),
        )
    )
    fig = plotly.graph_objs.Figure(data=traces, layout=layout_comp)
    plotly.offline.iplot(fig)
    return fig
    
def cluster_assign_plotter(dataframe):
    """ Returns a plotly plot of track assignment using the labels given in a frame.
    """
    
    labels = dataframe.label.unique()
    all_tracks = []
    for label in labels:
        all_tracks.append(
            plotly.graph_objs.Scatter(
                x=dataframe[dataframe.label==label].compensation,
                y=dataframe[dataframe.label==label].dispersion,
                mode='markers',
                marker=dict(size=5,
                    line=dict(width=1),
                   ),
        name=f'Track {label}'))

    layout_comp = plotly.graph_objs.Layout(
        title="Track assignment",
        hovermode='closest',
        xaxis=dict(
            title='Compensation (Td)',
            ticklen=3,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Dispersion (Td)',
            ticklen=5,
            gridwidth=2,
        ),
    )
    fig = plotly.graph_objs.Figure(data=all_tracks, layout=layout_comp)
    plotly.offline.iplot(fig)
    return fig

def hist_1ftr_1grp(df, group, feature):
    """ Returns a histogram of a selected column in pandas
        DataFrame grouped by another column's values.
    """
    traces = []
    for gr in getattr(df, group).unique():
        traces.append(
            plotly.graph_objs.Histogram(
                x=df[df[group] == gr][feature],
                opacity=0.75,
                name=f"group: {gr}"))    

    layout_comp = plotly.graph_objs.Layout(
        title=f'count of {feature} at every {group}',
        hovermode='closest',
        xaxis=dict(
            title=feature,
            ticklen=3,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Count',
            ticklen=5,
            gridwidth=2,
        ),
    )
    fig = plotly.graph_objs.Figure(data=traces, layout=layout_comp)
    plotly.offline.iplot(fig)
    return fig


