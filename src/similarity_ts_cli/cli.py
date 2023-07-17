import json
import os
import argparse
import warnings
import sys
from tqdm import tqdm
from datetime import datetime
from similarity_ts.similarity_ts_config import SimilarityTsConfig
from similarity_ts.metrics.metric_config import MetricConfig
from similarity_ts.metrics.metric_factory import MetricFactory
from similarity_ts.plots.plot_config import PlotConfig
from similarity_ts.plots.plot_factory import PlotFactory
from similarity_ts.similarity_ts import SimilarityTs
from similarity_ts.helpers.csv_reader_helper import load_ts_from_csv, load_ts_from_path


def main():
    available_metrics = MetricFactory.find_available_metrics().keys()
    available_figures = PlotFactory.find_available_figures().keys()
    parser = argparse.ArgumentParser(
        usage='similarity-ts-cli -ts1 path_to_file_1 -ts2_path path_to_files_2 [--metrics] [js ...] [--figures] [tsne ...] \
            [--header] [--timestamp_frequency_seconds] 300 [--stride] 2 [--window_selection_metric] metric_name'
    )
    parser.add_argument(
        '-ts1',
        '--time_series_1_filename',
        help='<Required> Include a csv filename that represents a time series. If ts1 is bigger than time series in ts2_path, it will be split in windows.',
        type=str,
        required=True,
    )
    parser.add_argument(
        '-ts2',
        '--time_series_2_path',
        help='<Required> Include the path to a csv file or a directory with csv files, each one representing time series.',
        type=str,
        required=True,
    )
    parser.add_argument(
        '-m',
        '--metrics',
        nargs='+',
        help='<Optional> Include metrics to be computed as a list separated by spaces.',
        choices=available_metrics,
        required=False,
    )
    parser.add_argument(
        '-f',
        '--figures',
        nargs='+',
        help='<Optional> Include figure names to be generated as a list separated by spaces.',
        choices=available_figures,
        required=False,
    )
    parser.add_argument(
        '-head',
        '--header',
        help='<Optional> If the time-series includes a header row.',
        required=False,
        action='store_true',
    )
    parser.add_argument(
        '-ts_freq_secs',
        '--timestamp_frequency_seconds',
        help='<Optional> Include the frequency in seconds in which samples were taken.',
        required=False,
        default=1,
        type=int,
    )
    parser.add_argument(
        '-strd',
        '--stride',
        help='<Optional> Include the stride to be used in moving windows over samples.',
        required=False,
        default=1,
        type=int,
    )
    parser.add_argument(
        '-w_select_met',
        '--window_selection_metric',
        help='<Optional> Include the chosen metric used to pick the best window in the first time series.',
        required=False,
        default='dtw',
        type=str,
    )
    args = parser.parse_args()
    __main_script(args)


def __main_script(arguments):
    ts1, header_ts1 = load_ts_from_csv(arguments.time_series_1_filename, arguments.header)
    ts2_dict = load_ts_from_path(arguments.time_series_2_path, header_ts1, arguments.header)
    similarity_ts_config = __create_similarity_ts_config(arguments, list(ts2_dict.keys()), header_ts1)
    similarity_ts = SimilarityTs(ts1, list(ts2_dict.values()), similarity_ts_config)
    save_directory_folder = f'results/{datetime.now().strftime("%Y-%m-%d-%H-%M")}'
    if similarity_ts_config.metric_config.metrics:
        __compute_metrics(similarity_ts, save_directory_folder)
    if similarity_ts_config.plot_config.figures:
        __compute_figures(similarity_ts, save_directory_folder)
    __print_warnings()


all_warnings_messages = []


def warning_handler(message, category, filename, lineno, file=None, line=None):
    all_warnings_messages.append(
        f'{category.__name__} at: {os.path.basename(filename)}. Details: {message}')


warnings.showwarning = warning_handler


def __print_warnings():
    if all_warnings_messages:
        for warning in all_warnings_messages:
            print(warning, file=sys.stderr)


def __compute_figures(similarity_ts, save_directory_path):
    plot_computer_iterator = similarity_ts.get_plot_computer()
    tqdm_plot_computer_iterator = tqdm(plot_computer_iterator, total=len(plot_computer_iterator),
                                       desc='Computing plots  ', dynamic_ncols=True)
    for ts2_name, plot_name, generated_plots in tqdm_plot_computer_iterator:
        tqdm_plot_computer_iterator.set_postfix(file=f'{ts2_name}|{plot_name}')
        __save_figures(ts2_name, plot_name, generated_plots, path=save_directory_path)


def __compute_metrics(similarity_ts, save_directory_path):
    metrics_results = {}
    metric_computer_iterator = similarity_ts.get_metric_computer()
    tqdm_metric_computer_iterator = tqdm(metric_computer_iterator, total=len(metric_computer_iterator),
                                         desc='Computing metrics')
    for ts2_name, metric_name, computed_metric in tqdm_metric_computer_iterator:
        if ts2_name not in metrics_results:
            tqdm_metric_computer_iterator.set_postfix(file=f'{ts2_name}|{metric_name}')
            metrics_results[ts2_name] = {}
        metrics_results[ts2_name][metric_name] = computed_metric
    __save_metrics(json.dumps(metrics_results, indent=4, ensure_ascii=False).encode('utf-8'),
                   path=f'{save_directory_path}/metrics')


def __create_similarity_ts_config(arguments, ts2_names, header_names):
    metric_config = None
    plot_config = None if arguments.timestamp_frequency_seconds is None else PlotConfig(None,
                                                                                        arguments.timestamp_frequency_seconds)
    if arguments.metrics is not None or arguments.figures is not None:
        metric_config = MetricConfig(arguments.metrics) if arguments.metrics else MetricConfig([])
        plot_config = PlotConfig(arguments.figures,
                                 arguments.timestamp_frequency_seconds) if arguments.figures else PlotConfig([],
                                                                                                             arguments.timestamp_frequency_seconds)
    return SimilarityTsConfig(metric_config, plot_config, arguments.stride, arguments.window_selection_metric,
                              ts2_names,
                              header_names)


def __save_figures(filename, plot_name, generated_plots, path='results/figures'):
    for plot in generated_plots:
        try:
            dir_path = __create_directory(filename, f'{path}/figures', plot_name)
            plot[0].savefig(f'{dir_path}{plot[0].axes[0].get_title()}.pdf', format='pdf', bbox_inches='tight')
        except FileNotFoundError as file_not_found_error:
            print(f'Could not create the figure in path: {file_not_found_error.filename}. This is probably because the path is too long.')


def __create_directory(filename, path, plot_name):
    try:
        if plot_name in PlotFactory.get_instance().figures_requires_all_samples:
            dir_path = f'{path}/{plot_name}/'
        else:
            original_filename = os.path.splitext(filename)[0]
            dir_path = f'{path}/{original_filename}/{plot_name}/'
        os.makedirs(dir_path, exist_ok=True)
    except FileNotFoundError as file_not_found_error:
        print(f'Could not create the directory in path: {file_not_found_error.filename}. This is probably because the path is too long.')
    return dir_path


def __save_metrics(computed_metrics, path='results/metrics'):
    try:
        os.makedirs(f'{path}', exist_ok=True)
        with open(f'{path}/results.json', 'w', encoding='utf-8') as file:
            file.write(computed_metrics.decode('utf-8'))
    except FileNotFoundError as file_not_found_error:
        print(f'Could not store the metrics in path: {file_not_found_error.filename}. This is probably because the path is too long.')


if __name__ == '__main__':
    main()
