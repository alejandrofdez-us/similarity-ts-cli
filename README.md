[![version](https://img.shields.io/badge/pypi-1.0.1-blue)](https://pypi.org/project/similarity-ts-cli/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-darkgreen)](https://www.python.org/downloads/release/python-390/)
[![last-update](https://img.shields.io/badge/last_update-07/18/2023-brightgreen)](https://github.com/alejandrofdez-us/similarity-ts-cli/commits/main)
[![license](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

# SimilarityTS-cli: Command-line interface for SimilarityTS package

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Description

SimilarityTS-cli is a command-line interface tool that act as an interface of the [SimilarityTS package](https://github.com/alejandrofdez-us/similarity-ts). Similarity-TS package facilitates the evaluation and comparison of
multivariate time series data. It provides a comprehensive toolkit for analyzing, visualizing, and reporting multiple
metrics and figures derived from time series datasets. The toolkit simplifies the process of evaluating the similarity of
time series by offering data preprocessing, metrics computation, visualization, statistical analysis, and report generation
functionalities. With its customizable features, SimilarityTS empowers researchers and data
scientists to gain insights, identify patterns, and make informed decisions based on their time series data.

This command-line interface is OS independent and can be easily installed and used.

### Available metrics

This toolkit can compute the following metrics:

- `kl`: Kullback-Leibler divergence
- `js`: Jensen-Shannon divergence
- `ks`: Kolmogorov-Smirnov test
- `mmd`: Maximum Mean Discrepancy
- `dtw` Dynamic Time Warping
- `cc`: Difference of co-variances
- `cp`: Difference of correlations
- `hi`: Difference of histograms

### Available figures

This toolkit can generate the following figures:

- `2d`: the ordinary graphical representation of the time series in a 2D figure with the time represented on the x axis
  and the data values on the y-axis for
    - the complete multivariate time series; and
    - a plot per column.

  Each generated figure plots both the `ts1` and the `ts2` data to easily obtain key insights into
  the similarities or differences between them.
    <div>
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/2d_sample_3_complete_TS_1_vs_TS_2.png?raw=true" alt="2D Figure complete">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/2d_sample_3_cpu_util_percent_TS_1_vs_TS_2.png?raw=true" alt="2D Figure for used CPU percentage">
    </div>
- `delta`: the differences between the values of each column grouped by periods of time. For instance, the differences
  between the percentage of cpu used every 10, 25 or 50 minutes. These delta can be used as a means of comparison between
  time series short-/mid-/long-term patterns.
    <div>
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/delta_sample_3_cpu_util_percent_TS_1_vs_TS_2_(grouped_by_10_minutes).png?raw=true" alt="Delta Figure for used CPU percentage grouped by 10 minutes">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/delta_sample_3_cpu_util_percent_TS_1_vs_TS_2_(grouped_by_25_minutes).png?raw=true" alt="Delta Figure for used CPU percentage grouped by 25 minutes">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/delta_sample_3_cpu_util_percent_TS_1_vs_TS_2_(grouped_by_50_minutes).png?raw=true" alt="Delta Figure for used CPU percentage grouped by 50 minutes">
    </div>

- `pca`: the linear dimensionality reduction technique that aims to find the principal components of a data set by
  computing the linear combinations of the original characteristics that explain the most variance in the data.
    <div align="center">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/PCA.png?raw=true" alt="PCA Figure" width="450">
    </div>
- `tsne`: a tool for visualising high-dimensional data sets in a 2D or 3D graphical representation allowing the creation
  of a single map that reveals the structure of the data at many different scales.
    <div align="center">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/t-SNE-iter_300-perplexity_5.png?raw=true" alt="TSNE Figure 300 iterations 5 perplexity" width="450">
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/t-SNE-iter_1000-perplexity_5.png?raw=true" alt="TSNE Figure 1000 iterations 5 perplexity" width="450">
    </div>
- `dtw` path: In addition to the numerical similarity measure, the graphical representation of the DTW path of each
  column can be useful to better analyse the similarities or differences between the time series columns. Notice that
  there is no multivariate representation of DTW paths, only single column representations.
    <div>
    <img src="https://github.com/alejandrofdez-us/similarity-ts/blob/e5b147b145970f3a93351a1004022fb30d20f5f0/docs/figures/DTW_sample_3_cpu_util_percent.png?raw=true" alt="DTW Figure for cpu">
    </div>

## Installation

To install the tool in your local environment, just run follow command:

```Bash
pip install similarity-ts-cli 
```

## Usage

Users must provide `.csv` files containing multivariate time series by using the arguments `-ts1` and `-ts2`.

- `-ts1` should point to a single `csv` filename. This time series may represent the baseline or ground truth time
  series.
- `-ts2` can point to another single `csv` filename or a directory that contains multiple `csv` files to be
  compared with `-ts1` file.
- `-head` if your time series files include a header this argument must be present. If not present, the software
  understands that csv files don't include a header row.

Constraints:

- `-ts1` time-series file and `-ts2` time-series file(s) must:
    - have the same dimensionality (number of columns)
    - not include a timestamp column
    - include only numeric values
    - include the same header (if present)
- if a header is present as first row, use the `-head` argument.
- all `-ts2` time-series files must have the same length (number of rows).

Note: the column delimiter is automatically detected.

If your data include categorical values, it might be pre-processed to convert them to numerical values. All `ts2s` time-series must have the same length (number of rows).

If `-ts1` time-series file is longer (more rows) than `-ts2` time-series file(s), the `-ts1` time series will be
divided in windows of the same
length as the `-ts2` time-series file(s).

For each `-ts2` time-series file, the most similar window (*) from `-ts1` time series is selected.

Finally, metrics and figures that assess the similarity between each pair of `-ts2` time-series file and its
associated most similar `-ts1` window are computed.

(*) `-w_select_met` is the metric used for the selection of the most
similar `-ts1` time-series window per each `-ts2` time-series file(s).`dtw` is the default value, however, any of
the
[metrics](#available-metrics) are also available for this purpose using this argument.

Users can provide metrics or figures to be computed/generated:

- `-m` the [metrics](#available-metrics) names to be computed as a list separated by spaces.
- `-f` the [figures](#available-figures) names to be computed as a list separated by spaces.

If no metrics nor figures are provided, the tool will compute all the available metrics and figures.

The following arguments are also available for fine-tuning:

- `-ts_freq_secs` the frequency in seconds in which samples were taken just to generate the delta figures. By default is
  `1` second.
- `-strd` when `ts1` time-series is longer than `ts2` time-series file(s) the windows are computed by using a
  stride of `1` by default. Sometimes using a larger value for the stride parameter improves the performance by skipping
  the computation of similarity between so many windows.

### Basic usage examples:

Some examples of evaluation of similarity are shown below. You can download some test data by running the following command:

```Bash
wget https://github.com/alejandrofdez-us/similarity-ts-cli/raw/main/data_samples.zip && unzip data_samples.zip
```
Or manually download and unzip from https://github.com/alejandrofdez-us/similarity-ts-cli/raw/main/data_samples.zip .

1. A time series and all time series computing all metrics and figures:
    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2 -head
    ```
   Every metric computation and figure generated will be found in the `results/{timestamp}/` directory.

1. Two time series computing only DTW metric and DTW figure:
    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2/sample_0.csv -head -m dtw -f dtw
    ```

1. A time series and all time series within a directory computing every metric and figure in SimilarityTS toolkit:
    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2 -head -m js mmd dtw ks kl cc cp hi -f delta dtw 2d pca tsne
    ```

1. Comparison between time series specifying the frequency in seconds in which samples were taken:
    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2 -head -m dtw -f dtw -ts_freq_secs 300
    ```

1. Comparison between time series specifying the stride that determines the step or distance by which a fixed-size
   window moves over the first time series:
    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2 -head -m dtw -f dtw -strd 5
    ```

1. Comparison between time series specifying the window selection metric to be used when selecting the most similar
   windows in
   the first time series:

    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2 -head -m dtw -f dtw -w_select_met js
    ```

1. Using our sample time series to compute every single metric and figure with a fixed timestamp frequency and stride:

    ```Bash
    similarity-ts-cli -ts1 data_samples/alibaba2018/ts1_machine_usage_days_1_to_8_grouped_300_seconds.csv -ts2 data_samples/alibaba2018/ts2 -head -m mmd dtw ks kl cc cp hi -f delta dtw 2d pca tsne -w_select_met cc -ts_freq_secs 300 -strd 5
    ```
## License

SimilarityTS toolkit is free and open-source software licensed under the [MIT license](LICENSE).

## Acknowledgements
Project PID2021-122208OB-I00, PROYEXCEL\_00286 and  TED2021-132695B-I00 project, funded by MCIN / AEI / 10.13039 / 501100011033, by Andalusian Regional Government, and by the European Union - NextGenerationEU.