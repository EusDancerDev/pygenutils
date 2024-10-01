# Changelog

## [v9.0.0] - 2024-10-01

### Added

<!--SOILIK ONDOKO LEHEN GIDOIAREN BARNEKOA FALTAN-->
- Add the following modules in `utilities` subpackage:
	- **Pandas Utils**: 
		- `conversions`: 
		- `data_manipulation`: 
		- `pandas_obj_handler`: 

- Add the following modules in `statistics` subpackage:
	- **Core Statistics**: 
		- `approximation_techniques`: for methods focusing on general approximation techniques not necessarily tied to specific curve fitting or interpolation.
		- `curve_fitting`: for methods like polynomial fitting and other curve fitting techniques.
		- `interpolation_methods`: for interpolation techniques, including the `hdy_interpolation` method.
	- **Climate Statistics** (`fields/climatology`)
		- `representative_series`: analysis of time series resulting from representativity criteria.

### Changed

- Once above creations done, the following moves and/or renamings have been made:

**Methods**

1. In `statistics` subpackage:

<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>polynomial_fitting</th>
		<th>regressions</th>
		<th>statistics/core</th>
		<th>(unchanged)</th>
		<th>curve_fitting</th>
		<th>(unchanged)</th>
		
	</tr>
	<tr>
		<th>calculate_HDY</th>
		<th>variables</th>
		<th>statistics/fields/climatology</th>
		<th>(unchanged)</th>
		<th>representative_series</th>
		<th>(unchanged)</th>
	</tr>
	<tr>
		<th>hdy_interpolation (once moved, changed visibility to internal)</th>
		<th>variables</th>
		<th>statistics/fields/climatology</th>
		<th>(unchanged)</th>
		<th>representative_series</th>
		<th>(unchanged)</th>
	</tr>	
	
2. To `time_handling` subpackage:

<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>infer_full_period_of_time (first time)</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>date_and_time_operators</th>
		<th>time_handling</th>
	</tr>
	<tr>
		<th>infer_full_period_of_time (second time)</th>
		<th>netcdf_handler</th>
		<th>climate_data_utils</th>
		<th>(unchanged)</th>
		<th>date_and_time_operators</th>
		<th>time_handling</th>
	</tr>
	<tr>
		<th>find_date_key</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>date_and_time_operators</th>
		<th>time_handling</th>
	</tr>
	<tr>
		<th>infer_full_period_of_time</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>date_and_time_operators</th>
		<th>time_handling</th>
	</tr>
	<tr>
		<th>infer_time_frequency</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>date_and_time_operators</th>
		<th>time_handling</th>
	</tr>
</table>

3. To `utilities/pandas_utils` subpackage (depth level 2)
<br>

3.1  To `conversions.py` module

<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>create_pivot_table</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>conversions</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>df_to_structured_array</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>conversions</th>
		<th>utilities/pandas_utils</th>
	</tr>
</table>

<br>
3.2 To `data_manipulation` module
	
<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>concat_dfs_aux</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>count_data_by_concept</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>insert_column_in_df</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>insert_row_in_df</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>polish_df_column_names</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>reindex_df</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>sort_df_indices</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>sort_df_values</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>data_manipulation</th>
		<th>utilities/pandas_utils</th>
	</tr>
</table>
<br>

3.3  To `pandas_obj_handler` module
	
<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>csv2df</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>excel_handler</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>merge_csv_files</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>merge_excel_files</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>merge_ods_files</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>ods_handler</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>read_table</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>save2csv</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>save2excel</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
	<tr>
		<th>save2ods</th>
		<th>data_frame_handler</th>
		<th>pandas_data_frames</th>
		<th>(unchanged)</th>
		<th>pandas_obj_handler</th>
		<th>utilities/pandas_utils</th>
	</tr>
</table>

**Modules**
	
</table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>---</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
		<th>---</th>
		<th>indicators</th>
		<th>(unchanged)</th>
	</tr>
	<tr>
		<th>---</th>
		<th>climate_variables</th>
		<th>statistics/fields/climatology</th>
		<th>---</th>
		<th>variables</th>
		<th>(unchanged)</th>
	</tr>
	<tr>
		<th>---</th>
		<th>calendar_operators</th>
		<th>time_handling</th>
		<th>---</th>
		<th>calendar_utils</th>
		<th>(unchanged)</th>
	</tr>
</table>

### Removed

- Once every addition and changes performed, removed subpackage `pandas_data_frames`.

---

## [v8.0.0] - 2024-09-29

### Added

1. Subpackage `climate_data_utils`:

- Handles operations focused on data manipulation for climate datasets, with a special focus on file management, downloads, and plotting.
- The following content has been added, each supporting specific utilities:

<u>**Modules**</u>

* `cdo_tools.py`
	- Provides wrappers and utilities for working with the Climate Data Operators (CDO) tool.
	- Contains functions to interact with the Climate Data Store (CDS) API for downloading and managing climate data from the Copernicus Climate Data Store.
	- Facilitates data requests and efficient downloads of large datasets.

* `cds_tools.py`
	- Contains functions to interact with the Climate Data Store (CDS) API for downloading and managing climate data from the Copernicus Climate Data Store.
	- Facilitates data requests and efficient downloads of large datasets.
	
* `detect_faulty_ncfiles`
	- Implements functionality to detect and manage faulty NetCDF files, ensuring data integrity during processing and analysis.

* `extract_netcdf_basics`
	- Provides functions for extracting basic information from NetCDF files, such as metadata and variable summaries, facilitating data exploration.

* `nco_tools`
	- Offers utilities for working with the NetCDF Operators (NCO) tool, allowing for data manipulation and operations specific to NetCDF file formats.

* `netcdf_handler`
	- Central module for handling various operations related to NetCDF files, including reading, writing, and modifying NetCDF datasets.

* `weather_software_file_creator`
	- Contains functions for creating weather software files based on processed climate data, ensuring compatibility with various weather analysis tools.

<u>**Further subpackages**</u>

* `complementary-to_remodule`
	- A subpackage containing various auxiliary and complementary functions aimed at climate data analysis and visualization. It includes:
		- <b>auxiliary_functions</b>: Utility functions to assist with common tasks such as file handling, data transformations, and helper routines.
		- <b>ba_mean_and_var</b>: Implements methods to compute bias-adjusted mean and variance from climate data.
		- <b>ba_mean</b>: Provides functions for calculating bias-adjusted means from climate datasets, allowing for more accurate representation of data characteristics.

* `data_downloads`
	- A module dedicated to managing the download of climate data. It contains:
		- <b>codes</b>: Includes scripts and configurations necessary for utilizing the Copernicus API for efficient data downloads.
		- <b>input_data</b> A folder for storing downloaded climate data, ensuring organized access to data files.


2. Subpackage `statistics`:

- Introduced a new subpackage `statistics` to encapsulate numerical and statistical methods.,<br>
  aiming for modularity and organization across general and field-specific domains.

- **Core Modules:**
	- `time_series.py`: General methods for time series analysis, including signal processing.
	- `regressions.py`: Polynomial regression and other regression models.
	- `signal_forcing.py`: Signal whitening and noise handling.
- **Domains Supported:**
	- **Time Series Analysis:** Methods for handling trends, noise, and filtering in time-series data.
	- **Signal Processing:** Includes signal filtering, whitening, and band-pass filters.
	- **Statistical Testing:** Initial support for statistical tests.

- **Improved Structure:** Consolidated statistical logic from various modules under a unified subpackage, with plans for expanding into domain-specific methods.


3. `statistical_tests` as a `core` module:

- **Hypothesis Testing**:
	* Added basic methods for hypothesis testing in the `statistical_tests.py` module, including:
		* `z_test_two_means` and `chi_square_test` which provide common statistical hypothesis tests.
	* Each method includes a full docstring with parameter descriptions, examples, and returns, designed to be easily expanded for more complex use cases in the future.


### Changed

- Many functions have been moved out from the modules in the old `weather_and_climate` subpackage to `statistics`.
- Information about the original module and new function name and location is displayed next:
  
<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>calculate_WSDI</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>WSDI</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_SU</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>SU</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_CSU</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>CSU</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_FD/th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>FD</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_TN</th>
		<th>TN</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_RR</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>RR</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_CWD</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>CWD</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_HWD</th>
		<th>HWD</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_HWD</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>HWD</th>
		<th>climate_indicators</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_HDY</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>HDY</th>
		<th>climate_variables</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>hdy_interpolation</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>climate_variables</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_biovars</th>
		<th>climate_indicators</th>
		<th>weather_and_climate</th>
		<th>biovars</th>
		<th>climate_variables</th>
		<th>statistics/fields/climatology</th>
	</tr>
</table>
	
<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>periodic_statistics</th>
		<th>climate_statistics</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>time_series</th>
		<th>statistics/core</th>
	</tr>
	<tr>
		<th>climat_periodic_statistics</th>
		<th>climate_statistics</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>periodic_climat_stats</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>calculate_and_apply_deltas</th>
		<th>climate_statistics</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>simple_bias_correction</th>
		<th>statistics/fields/climatology</th>
	</tr>
	<tr>
		<th>window_sum/th>
		<th>climate_statistics</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>moving_operations</th>
		<th>statistics/core</th>
	</tr>
	<tr>
		<th>moving_average</th>
		<th>climate_statistics</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>moving_operations</th>
		<th>statistics/core</th>
	</tr>
</table>

<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>autocorrelate</th>
		<th>climatic_signal_modulators</th>
		<th>weather_and_climate</th>
		<th>(unchanged)</th>
		<th>time_series</th>
		<th>statistics/core</th>
	</tr>
</table>

<table>
	<tr>
		<th><span style="font-size:13.7pt">Original function name</span></th>
		<th><span style="font-size:13.7pt">Original module</span></th>
		<th><span style="font-size:13.7pt">Original subpackage path</span></th>
		<th><span style="font-size:13.7pt">New function name</span></th>
		<th><span style="font-size:13.7pt">New module</span></th>
		<th><span style="font-size:13.7pt">New subpackage path</span></th>
	</tr>
	<tr>
		<th>get_1hour_time_step_data</th>
		<th>consecutive_idx_statistics</th>
		<th>weather_and_climate</th>
		<th>hourly_ts_cumul</th>
		<th>time_series</th>
		<th>statistics/core</th>
	</tr>
	<tr>
		<th>count_consecutive_days_maxdata</th>
		<th>consecutive_idx_statistics</th>
		<th>weather_and_climate</th>
		<th>consec_occurrences_maxdata</th>
		<th>time_series</th>
		<th>statistics/core</th>
	</tr>
	<tr>
		<th>count_consecutive_days_mindata</th>
		<th>consecutive_idx_statistics</th>
		<th>weather_and_climate</th>
		<th>consec_occurrences_mindata</th>
		<th>time_series</th>
		<th>statistics/core</th>
	</tr>
</table>
	
- <u>**NOTE**</u>: prior to these movements, every single method until here has been refactored, functionalities enhanced and optimised inner codes.

5. Rest of the content:

- The following content has been moved to the new subpackage `climate_data_utils`:

1. **Modules**:
	* `cdo_tools`
	* `cds_tools`
	* `detect_faulty_ncfiles`
	* `extract_netcdf_basics`
	* `__init__`
	* `meteorological_variables`
	* `nco_tools`
	* `netcdf_handler`
	* `weather_software_file_creator`
	
2. **Further Subpackages**:
	* `data_downloads`
	* `complementary-to_remodule`

### Removed

- Once every operation above performed, delete subpackage `weather_and_climate`.

---

## [v7.3.3] - 2024-09-28

### Added

`climatic_signal_modulators`

- **Autocorrelation Function**:
   * Streamlined the logic by handling smaller arrays using `numpy.correlate` and larger arrays with `scipy.signal.correlate`.
   * Updated the docstring to clarify parameters and computation flow, explaining when to use two-sided or one-sided autocorrelation.

- **Signal Whitening Methods**:
   * Developed two signal whitening methods: `signal_whitening_classic` and `signal_whitening_pca`.
   * `signal_whitening_classic` applies a traditional approach using Cholesky decomposition with `numpy.linalg`.
   * `signal_whitening_pca` uses Principal Component Analysis (PCA) via `sklearn` for whitening data.
   * Enhanced docstrings for both methods, clarifying inputs, outputs, and providing comprehensive usage examples.
   
- **Band-Pass Filtering Methods**:
	* Refined three band-pass filtering methods (`band_pass1`, `band_pass2`, `band_pass3`), created during the Master in Meteorology, now translated:
		* Simplified internal variable names and loops for more concise code.
		* Added detailed docstrings, explaining how each method works with frequency domain transformations and filtering based on custom low and high-frequency ranges.
		* Used consistent terminology and enhanced explanations for different approaches to band-pass filtering.
   
- **Low and High-Pass Filtering Methods**:
	- Refined `low_pass_filter` and `high_pass_filter` methods, also created during the Master in Meteorology: 
		* Improved performance by applying zero-phase filtering and optimizing how filters are designed based on cutoff frequencies.
		* Expanded the docstring to include explanations on filter design and its effect on different time series data.

### Changed

1. `climatic_statistics`

- `window_sum`:
	* Optimized performance by using `np.convolve` for faster sliding window summation.
	* Added edge case handling for empty arrays or when the window size exceeds the array length.
	* Refined docstring to clarify input parameters, particularly around window size and handling of edge cases.

- `moving_average`:
	* Rewritten using `np.convolve` for efficient computation of moving averages over a window.
	* Added option for handling arrays shorter than the window size, ensuring graceful failure or warning.
	* Clarified the docstring, highlighting that this method handles general numerical arrays, and specifying the nature of the windowing process.
	
2. `climatic_signal_modulators`

- `polynomial_fitting`
	 * Optimized the logic by simplifying variable names and improving handling of edge cases.
	 * Enhanced the docstring to detail the parameters, added alternative polynomial function usage, and described the fixing of edges in polynomial interpolation.

---

## [v7.0.0] - 2024-09-26

### Changed
- Delete part of the file name `arrays_` contained in all modules of the subpackage `arrays_and_lists`,<br>
  then delete all old-named modules.
- Module `climate_statistics`: refactor the following methods to improve performance, readability and maintainability:
	* `periodic_statistics`
	* `climat_periodic_statistics`
	* `calculate_and_apply_deltas`
	* `window_sum`
	* `moving_average`
- Remove the substring `array_` of methods `select_array_elements` (module `patterns`), <btr>
  `sort_array_rows_by_column` and `sort_array_columns_by_row` (both in module `data_manipulation`).
- Remove triple quoted template string.

---

## [v6.8.2] - 2024-09-25

### Changed
- Improve readability and streamline functions
- Substitute `print_exit_info` with `exit_info` as done in the original module `os_operations`
- Replace varname `time_format` by `dt_format` as this generally represents both date and time (abbreviated as `dt`).

### Added
- Add functionalities to media manipulation methods for merging and cutting audio/video files
- Add two external programs that apply methods of the module `audio_and_video_manipulation`.
- Add and reorganize section header comments

---

## [v6.6.0] - 2024-09-23

### Changed
- Rename method `remove_elements_from_array` to `remove_elements`
- Eliminate `exec_command_shell` method and, if present, `catch_shell_prompt_output` <br>
  in favour of the renewed and complete `run_system_command` from module `os_operations`
- Refactor command execution module

### Added
- Add docstring for every method
- Add module to store configuration data like credentials, host info, etc.
- Add type to every parameter missing it in all docstrings
- Add dictionary with conversion factors from the provided floated time to the given unit

---

## [v6.3.4] - 2024-09-20

### Changed
- Delete `todo` from the code as the task there is already done
- Specify the name and type of the returning variable in method `string_underliner`

### Added
- Add optional argument, comments explaining key parts of the code and simplify the f-strings
- Add type to the parameter `datetime_obj` in the docstring of the internal method `_total_time_unit`
- Add type to every parameter missing it in all docstrings

---

## [v6.3.0] - 2024-09-18

### Changed
- Eliminate need of the old method `time_format_tweaker` in favour of the renewed `datetime_obj_converter` from module `time_formatters`
- Rewrite some lazy imports and fix a typo as a result

### Added
- Add further fractional second precision choice at internal method `_format_arbitrary_time`
- Add support for `datetime.time` object conversion to other datetime-like objects

---

## [v6.0.0] (2024-09-06)

### Added
- Created directories for lambda functions and assertion documentation in Python.
- Enhanced performance by importing frequently used NumPy libraries and utilizing `get_obj_type_str` for type checks.
- Implemented a simple calculator functionality using a dictionary-based switch-case approach, accepting multiple arguments.
- Improved input validation and functionalities in `sort_dictionary_by_keys` and `merge_dictionaries` methods.
  
### Changed
- Restored accidentally removed code during editing.
- Sub-package `arrays_and_lists`:
	* Move out some methods in `array_data_manipulation` and `array_maths` to other modules in this sub-package.
	* Rewrite section headers to align with the nature of methods under them. Clarity and precision gained.
- Renamed directories for improved readability and intuitive understanding.
- Removed unnecessary directories due to renaming or redundancy.

### Removed
- Deleted `webdriver_Firefox-Chrome_settings_check.py` in favour of the more descriptively named `webdriver_Firefox-Chrome_setup_test.py`.
- Eliminated `git` directory as Git does not depend on Python.

---

## [v5.5.5] (2024-08-20)

### Added
- Combined character splitting instructions into single lines for efficiency.
  
### Changed
- Enhanced the `format_table_from_lists` method for better error handling.
- Improved readability by splitting long lines into shorter ones.
- Introduced a new folder for Web Scraping modules.

---

## [v5.4.2] (2024-08-08)

### Added
- Functionality to select column delimiters in all relevant methods.
- New method to underline single or multiple line strings.

### Changed
- Revised the docstring in `format_table_from_lists` to reflect new functionalities.
- Fixed issues in the `format_table_from_lists` method related to multi-row values.

### Removed
- Removed the `Constants` section from general notes.

---

## [v5.2.2] (2024-07-15)

### Added
- Optional argument for setting the index starting number in `format_table_from_list` and `format_table_from_lists`.
- New module for formatting dictionaries or lists into tables.

### Changed
- Clarified overwriting behaviour in `serialize_dict_to_json`.
- Simplified the try-except block structure in `print_format_string`.

### Removed
- Removed a JSON test file.

---

## [v5.0.0] (2024-07-10)

### Added
- Created a subpackage for JSON functionalities.

### Changed
- Polished section comments for clarity.

### Removed
- Removed redundant JSON file utilities, centralizing them in the `json_file_handler` module.

---

## [v4.9.0] (2024-06-29)

### Added
- Various references updated from `pytools` to `pyutils`.
- New warning codes and documentation improvements.

### Changed
- Created a file to track significant changes in the repository.

---

## [v4.0.0] (2024-06-26)

### Added
- Several subpackages for various utility functions and modules.

### Changed
- Relocated methods and optimized imports.

### Removed
- Deleted files that have been relocated.

---

## [v3.0.0] (2024-06-24)

### Added
- Introduced new functionalities for handling regex and optimizing code structure.

### Changed
- Updated imports to absolute and improved error handling.

---

## [v2.7.4] - 2024-06-14

### Changed
- Modify method `datetime_range_operator` to `merge_datetime_dataframes`.
- Update method `get_current_time` to `get_current_datetime`; fix typo when writing to the object `report_file_obj`.
- Optimize the code of the main method `clock_time_average`, as well as the auxiliary methods, and add and refine the docstrings in all of them.
- Refine module and custom module import syntax in method `standardize_calendar`.
- Rename `ofile` variable to `out_file_obj`, which all `.write` instances are referenced from.

### Added
- Add todo for when method `time_format_tweaker` at module `time_formatters` is optimized and incorporated more functionalities to it.
- Add detailed docstring to the method `natural_year` and optimize inner code and comments.

### Fixed
- Fix todo list for main method `clock_time_average` and auxiliaries
- Optimize the whole try-except block and handle specific errors gracefully.

---

## [v2.4.0] - 2024-06-12
### Added
- Add docstrings and polish the main methods `sum_clock_times` and `sum_date_objects`, as well as their auxiliary methods.
- Add methods to sum or subtract dates and/or times (preliminary version).

### Deleted
- Delete to-do list with date and time maths.

---

## [v2.1.0] - 2024-06-11
### Added
- Import the method to return an object type`s string part.
- Add multidimensional indexing functionality for NumPy arrays in `select_array_elements` method.

### Renamed
- Rename the method to return an object type`s string part.

---

## [v2.0.0] - 2024-06-10
### Added
- Add module for climate and environment data manipulation and extraction.
- Add module for date and time management methods.
- Add module initiator file.
- Add module for string management.
- Add directory containing small manuals and web extracts about external Python modules and methods.
- Add module for mathematical operations with sets.

### Removed
- Remove method `json2dict` as dictionaries are semantically handled.
