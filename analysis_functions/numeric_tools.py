from typing import Dict
from jinjasql import JinjaSql
import pandas
import numpy
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import DBSCAN


def dataframe_from_sql_template(
    dal,
    session_scope,
    path: str,
    query_params: Dict[str, str],

) -> pandas.core.frame.DataFrame:

    """ Returns python pandas dataframe from an sql query file
    using jinja to inject parameters that are arguments in this function.
    """

    with open(path, 'r') as file:
        sql_query = file.read()

    jinja_query = JinjaSql(param_style='pyformat')
    parametrised_query, bind_params = jinja_query.prepare_query(
        sql_query,
        query_params
        )

    with session_scope(dal) as session:
        result = pandas.read_sql(
                    parametrised_query,
                    dal.engine,
                    params=bind_params
                 )
        session.close()

    return result

def humidity_mapper(
    df: pandas.core.frame.DataFrame
    ) -> pandas.core.frame.DataFrame:
    """ function to calculate humidity at the chip per
    each scan record from pre-san-dump.
    """
    df['humidity_at_chip'] = numpy.NaN
    
    for i in df.index:
        df.at[i, 'humidity_at_chip'] = (
            df.at[i, 'sample_flow'] *
            df.at[i, 'amb_hu_h2o_conc'] /
            df.at[i, 'internal_flow']
        )
    return df

def match_quant(
    df: pandas.core.frame.DataFrame,
    set_pt: str,
    reading: str
    ) -> float:
    """ Returns a single digit metric of two vector euclidean similarity
    scaled to the number of records in that vector. 
    """
    numerator = numpy.sum((df[reading]-df[set_pt])**2)
    denominator = numpy.sum(df[reading]**2) + numpy.sum(df[set_pt]**2)
    answer = numerator / denominator
    return answer / len(df[reading])

def optimize_dbscan_hyperparams(
    data,
    eps_range,
    min_samples_range,
    metric,
    features,
    amount_clusters,
    no_repetitions
):
    """Returns a dictionary of optimal set of parameters to achieve
    specific amount of clusters in a dataset. """
    
    results = {'eps': [],
               'min_samples': [],
               'misclassified': []
    }
    numpy.random.seed(1)
    while len(results['eps']) < no_repetitions:
        for step, size in zip(
            eps_range[0] + numpy.random.ranf([1]) * (eps_range[1] - eps_range[0]),
            min_samples_range[0] + numpy.rint(numpy.random.ranf([1]) * (min_samples_range[1] - min_samples_range[0]))
        ):
            X = posmode_peaks[features]
            X = RobustScaler().fit_transform(X)
            db = DBSCAN(
                eps=step,
                min_samples=size,
                metric=metric
            )
            metrics = db.fit_predict(X)
            if numpy.unique(metrics).size == amount_clusters:
                results['eps'].append(step)
                results['min_samples'].append(size)
                results['misclassified'].append((metrics == -1).sum())
    return results


class PolyMask:
    """docstring for PolyMask"""
    def __init__(self, degree):
        self.degree = degree
        self._fit_central = None

    #@property
    def fit_central(self, df, min_height):
        posmode_filter = df.height >= min_height
        posmode_peaks = df[posmode_filter].copy()
        answer = numpy.polyfit(
            posmode_peaks.compensation,
            posmode_peaks.dispersion,
            deg=self.degree
            )
        self._fit_central = answer
        return self._fit_central

    def return_masked(self, df, right_offset, left_offset, visualize=False):
        new_peaks = df.copy()
        new_peaks['min_disp'] = numpy.polynomial.polynomial.polyval(
            new_peaks.compensation - right_offset,
            numpy.flip(self._fit_central)
            )
        new_peaks['max_disp'] = numpy.polynomial.polynomial.polyval(
            new_peaks.compensation + left_offset,
            numpy.flip(self._fit_central)
            )
        new_peaks = new_peaks[new_peaks.dispersion.between(
            new_peaks.min_disp,
            new_peaks.max_disp
            )]        
        return new_peaks
