import plotly.plotly as py
import plotly.graph_objs as go


class GraphUtils(object):

    @classmethod
    def plot_data(cls, file_source, file_target, edit_distance_counts):
        cls._sign_in()
        print "Collecting data points for graph..."
        x_axis_data_points = [] # edit distances
        y_axis_data_points = [] # counts

        for filename in edit_distance_counts.iterkeys():
            x_coordinates = []
            y_coordinates = []
            for e_dist, count in edit_distance_counts[filename].iteritems():
                x_coordinates.append(e_dist)
                y_coordinates.append(count)

            x_axis_data_points.append( x_coordinates )
            y_axis_data_points.append( y_coordinates )

        cls._create_graph(file_source, file_target, x_axis_data_points, y_axis_data_points)

    @staticmethod
    def _create_graph(file_source, file_target, x_axis_data_points, y_axis_data_points):
        print "Creating graph..."
        lang1 = go.Scatter(
            x=x_axis_data_points[0],
            y=y_axis_data_points[0],
            mode="markers",
            marker = dict(
                size=10,
                color='rgba(244, 66, 66, .8)' ),
            text="Source Lang",
            name=file_source
        )
        lang2 = go.Scatter(
            x=x_axis_data_points[1],
            y=y_axis_data_points[1],
            mode="markers",
            marker = dict(
                size=10,
                color='rgba(66, 166, 244, .5)' ),
            text="Target Lang",
            name=file_target
        )
        data = go.Data( [lang1, lang2] )

        layout = go.Layout(
            title='Edit Distance Counts by Language',
            xaxis=dict(
                title='Edit Distance',
            ),
            yaxis=dict(
                title='Count',
            ),
            showlegend=True
        )
        fig = go.Figure(data=data, layout=layout)

        print py.plot(fig)

    @staticmethod
    def _sign_in():
        py.sign_in('Andrew.Hearst75', 'd5R5jd7z5BqSCot4ClrL')
