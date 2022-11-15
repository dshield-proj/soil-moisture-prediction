# soil-moisture-prediction

## 1. Download HDF5 files from SMAP
Use the python code to download the SMAP L4 data in HDF5 format for the required dates. For more information visit [SMAP L4](https://nsidc.org/data/spl4smgp/versions/6)

## 2. Pre-process files
The Deep learning model uses images as it's inputs. So convert the HDF5 file to JPEG image using the Pre-processing code. This is done for two features Soil Moisture and Precipitation.

## 3. Train the model
Use the tranining code to train a ConvLSTM model

## 4. Predictions
Use the prediction code to predict for the required date. Note that for validation purposes all the dates , including the date to be predicted, data must be loaded.

## 5. Post process the predicted CSV file
Finally post-process the global predicted CSV file to include the estimated bias for selected Ground Points.

## Questions?
Contact: Archana Kannan

Email: kannana@usc.edu
