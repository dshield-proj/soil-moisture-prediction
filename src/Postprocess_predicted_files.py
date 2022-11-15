"""
Create final targetValue CSVs from raw CSV predictions
@author: Archana Kannan (kannana@usc.edu)
"""

# Imports
import pandas as pd
import numpy as np
import datetime

delta = datetime.timedelta(hours=3)  # DELTA T. For SMAP L4 DELTA=3hours


def create_intermediate_file_from_raw_pred(start, end, path_raw, path_intermediate, path_grid):
    """
    Function to extract required GP data from the predictions and store along with grid information
    @param start: start datetime
    @param end: end datetime
    @param path_raw: Path to predicted CSVs
    @param path_intermediate: Path to store intermediate files
    @param path_grid: Path to grid file
    @return: NA
    """
    while start <= end:
        d = start.strftime("%Y%m%d%H%M%S")

        df_pred = pd.read_csv(path_raw + d + ".csv")  # Read raw pred files from the ConvLSTM predictor

        # df_GP consists of lat, long, corresponding row, columns and GP index for the D-SHIELD chosen GPs
        df_GP = pd.read_csv(path_grid + "added_global_with_row_col.csv")

        # Add essential information for generating final targetValue CSV file
        df = pd.DataFrame()
        df['gpi'] = df_GP['GP']
        df['row'] = df_GP['row']
        df['col'] = df_GP['col']

        df['lat[deg]'] = df_GP['lat(y)']
        df['long[deg]'] = df_GP['long(x)']
        df['IGBPClass'] = df_GP['IGBP']

        df['Biome ID'] = df['IGBPClass']

        # Combining 16 classes to get five biome types
        df.loc[df["Biome ID"] == 1, "Biome ID"] = "B1"
        df.loc[df["Biome ID"] == 2, "Biome ID"] = "B1"
        df.loc[df["Biome ID"] == 3, "Biome ID"] = "B1"
        df.loc[df["Biome ID"] == 4, "Biome ID"] = "B1"
        df.loc[df["Biome ID"] == 5, "Biome ID"] = "B1"

        df.loc[df["Biome ID"] == 6, "Biome ID"] = "B2"
        df.loc[df["Biome ID"] == 7, "Biome ID"] = "B2"

        df.loc[df["Biome ID"] == 8, "Biome ID"] = "B3"
        df.loc[df["Biome ID"] == 9, "Biome ID"] = "B3"
        df.loc[df["Biome ID"] == 10, "Biome ID"] = "B3"

        df.loc[df["Biome ID"] == 12, "Biome ID"] = "B4"
        df.loc[df["Biome ID"] == 14, "Biome ID"] = "B4"

        df.loc[df["Biome ID"] == 16, "Biome ID"] = "B5"

        # Add the predicted SM as a column
        # df['SM_pred [m^3m^-3]'] = df_pred['y_pred']
        df['SM_pred [m^3m^-3]'] = df_pred['SMAP_sm']

        # Add uncertainty (variance/standard deviation) as columns
        df['Variance'] = df_pred['Var']
        df['Standard deviation'] = df_pred['Std_dev']

        df['gpi'].replace('', np.nan, inplace=True)
        df['IGBPClass'].replace('', np.nan, inplace=True)

        df.dropna(subset=['gpi'], inplace=True)
        df.dropna(subset=['IGBPClass'], inplace=True)

        df['gpi'] = df['gpi'].astype('int')
        df['IGBPClass'] = df['IGBPClass'].astype('int')

        df_grid = df[['gpi', 'lat[deg]', 'long[deg]', 'row', 'col', 'IGBPClass', 'Biome ID']]

        df = df.drop(columns=['IGBPClass'])  # Removing the no longer used IGBP class information

        # Saving intermediate prediction files and grid.csv file containing supplementary information about the final targetValue files
        df.to_csv(path_intermediate + d + ".csv", index=False)
        df_grid.to_csv(path_grid + "grid.csv", index=False)

        start += delta


def create_target_value_file_from_intermediate_file(start, path_intermediate, path_final):
    """
    Function to create the final target value CSV for plannar.
    @param start: start datetime
    @param path_intermediate: Path to intermediate files
    @param path_final: Path to store the target value CSVs
    @return:NA
    """
    d = start.strftime("%Y%m%d")

    df_1 = pd.read_csv(path_intermediate + d + "013000.csv")
    df_2 = pd.read_csv(path_intermediate + d + "043000.csv")
    df_3 = pd.read_csv(path_intermediate + d + "073000.csv")
    df_4 = pd.read_csv(path_intermediate + d + "103000.csv")
    df_5 = pd.read_csv(path_intermediate + d + "133000.csv")
    df_6 = pd.read_csv(path_intermediate + d + "163000.csv")
    df_7 = pd.read_csv(path_intermediate + d + "193000.csv")
    df_8 = pd.read_csv(path_intermediate + d + "223000.csv")

    # Time 1
    df_1["Bias_sq"] = df_1["Biome ID"]
    df_1.loc[df_1["Biome ID"] == "B1", "Bias_sq"] = 0.0334 ** 2
    df_1.loc[df_1["Biome ID"] == "B2", "Bias_sq"] = 0.0172 ** 2
    df_1.loc[df_1["Biome ID"] == "B3", "Bias_sq"] = 0.0821 ** 2
    df_1.loc[df_1["Biome ID"] == "B4", "Bias_sq"] = 0.0522 ** 2
    df_1.loc[df_1["Biome ID"] == "B5", "Bias_sq"] = 0.0671 ** 2
    df_1["V1"] = df_1["Variance"] + df_1["Bias_sq"]
    df_1["V1"] = df_1["V1"]

    df1_dict = {"Grid index": df_1['gpi'],
                "V1": df_1["V1"]}
    pd.DataFrame(df1_dict).to_csv(path_final + "targetVal_" + d + "T013000Z.csv", index=False)
    print("Time 1")
    print(np.max(df_1["V1"]))
    print(np.mean(df_1["V1"]))

    # Time 2
    df_2["Bias_sq"] = df_2["Biome ID"]
    df_2.loc[df_2["Biome ID"] == "B1", "Bias_sq"] = 0.0672 ** 2
    df_2.loc[df_2["Biome ID"] == "B2", "Bias_sq"] = 0.0717 ** 2
    df_2.loc[df_2["Biome ID"] == "B3", "Bias_sq"] = 0.1495 ** 2
    df_2.loc[df_2["Biome ID"] == "B4", "Bias_sq"] = 0.1243 ** 2
    df_2.loc[df_2["Biome ID"] == "B5", "Bias_sq"] = 0.1354 ** 2
    df_2["V1"] = df_2["Variance"] + df_2["Bias_sq"]
    df_2["V1"] = df_2["V1"]

    df2_dict = {"Grid index": df_2['gpi'],
                "V1": df_2["V1"]}
    pd.DataFrame(df2_dict).to_csv(path_final + "targetVal_" + d + "T043000Z.csv", index=False)
    print("Time 2")
    print(np.max(df_2["V1"]))
    print(np.mean(df_2["V1"]))

    # Time 3
    df_3["Bias_sq"] = df_3["Biome ID"]
    df_3.loc[df_3["Biome ID"] == "B1", "Bias_sq"] = 0.0785 ** 2
    df_3.loc[df_3["Biome ID"] == "B2", "Bias_sq"] = 0.1278 ** 2
    df_3.loc[df_3["Biome ID"] == "B3", "Bias_sq"] = 0.2287 ** 2
    df_3.loc[df_3["Biome ID"] == "B4", "Bias_sq"] = 0.1919 ** 2
    df_3.loc[df_3["Biome ID"] == "B5", "Bias_sq"] = 0.2067 ** 2
    df_3["V1"] = df_3["Variance"] + df_3["Bias_sq"]
    df_3["V1"] = df_3["V1"]

    df3_dict = {"Grid index": df_3['gpi'],
                "V1": df_3["V1"]}
    pd.DataFrame(df3_dict).to_csv(path_final + "targetVal_" + d + "T073000Z.csv", index=False)
    print("Time 3")
    print(np.max(df_3["V1"]))
    print(np.mean(df_3["V1"]))

    # Time 4
    df_4["Bias_sq"] = df_4["Biome ID"]
    df_4.loc[df_4["Biome ID"] == "B1", "Bias_sq"] = 0.0904 ** 2
    df_4.loc[df_4["Biome ID"] == "B2", "Bias_sq"] = 0.1323 ** 2
    df_4.loc[df_4["Biome ID"] == "B3", "Bias_sq"] = 0.2861 ** 2
    df_4.loc[df_4["Biome ID"] == "B4", "Bias_sq"] = 0.2418 ** 2
    df_4.loc[df_4["Biome ID"] == "B5", "Bias_sq"] = 0.2640 ** 2
    df_4["V1"] = df_4["Variance"] + df_4["Bias_sq"]
    df_4["V1"] = df_4["V1"]

    df4_dict = {"Grid index": df_4['gpi'],
                "V1": df_4["V1"]}
    pd.DataFrame(df4_dict).to_csv(path_final + "targetVal_" + d + "T103000Z.csv", index=False)
    print("Time 4")
    print(np.max(df_4["V1"]))
    print(np.mean(df_4["V1"]))

    # Time 5
    df_5["Bias_sq"] = df_5["Biome ID"]
    df_5.loc[df_5["Biome ID"] == "B1", "Bias_sq"] = 0.1129 ** 2
    df_5.loc[df_5["Biome ID"] == "B2", "Bias_sq"] = 0.1451 ** 2
    df_5.loc[df_5["Biome ID"] == "B3", "Bias_sq"] = 0.3436 ** 2
    df_5.loc[df_5["Biome ID"] == "B4", "Bias_sq"] = 0.3071 ** 2
    df_5.loc[df_5["Biome ID"] == "B5", "Bias_sq"] = 0.3287 ** 2
    df_5["V1"] = df_5["Variance"] + df_5["Bias_sq"]
    df_5["V1"] = df_5["V1"]

    df5_dict = {"Grid index": df_5['gpi'],
                "V1": df_5["V1"]}
    pd.DataFrame(df5_dict).to_csv(path_final + "targetVal_" + d + "T133000Z.csv", index=False)
    print("Time 5")
    print(np.max(df_5["V1"]))
    print(np.mean(df_5["V1"]))

    # Time 6
    df_6["Bias_sq"] = df_6["Biome ID"]
    df_6.loc[df_6["Biome ID"] == "B1", "Bias_sq"] = 0.1388 ** 2
    df_6.loc[df_6["Biome ID"] == "B2", "Bias_sq"] = 0.1608 ** 2
    df_6.loc[df_6["Biome ID"] == "B3", "Bias_sq"] = 0.4206 ** 2
    df_6.loc[df_6["Biome ID"] == "B4", "Bias_sq"] = 0.3684 ** 2
    df_6.loc[df_6["Biome ID"] == "B5", "Bias_sq"] = 0.3928 ** 2
    df_6["V1"] = df_6["Variance"] + df_6["Bias_sq"]
    df_6["V1"] = df_6["V1"]

    df6_dict = {"Grid index": df_6['gpi'],
                "V1": df_6["V1"]}
    pd.DataFrame(df6_dict).to_csv(path_final + "targetVal_" + d + "T163000Z.csv", index=False)
    print("Time 6")
    print(np.max(df_6["V1"]))
    print(np.mean(df_6["V1"]))

    # Time 7
    df_7["Bias_sq"] = df_7["Biome ID"]
    df_7.loc[df_7["Biome ID"] == "B1", "Bias_sq"] = 0.1734 ** 2
    df_7.loc[df_7["Biome ID"] == "B2", "Bias_sq"] = 0.1458 ** 2
    df_7.loc[df_7["Biome ID"] == "B3", "Bias_sq"] = 0.4880 ** 2
    df_7.loc[df_7["Biome ID"] == "B4", "Bias_sq"] = 0.4261 ** 2
    df_7.loc[df_7["Biome ID"] == "B5", "Bias_sq"] = 0.4435 ** 2
    df_7["V1"] = df_7["Variance"] + df_7["Bias_sq"]
    df_7["V1"] = df_7["V1"]

    df7_dict = {"Grid index": df_7['gpi'],
                "V1": df_7["V1"]}
    pd.DataFrame(df7_dict).to_csv(path_final + "targetVal_" + d + "T193000Z.csv", index=False)
    print("Time 7")
    print(np.max(df_7["V1"]))
    print(np.mean(df_7["V1"]))

    # Time 8
    df_8["Bias_sq"] = df_8["Biome ID"]
    df_8.loc[df_8["Biome ID"] == "B1", "Bias_sq"] = 0.2076 ** 2
    df_8.loc[df_8["Biome ID"] == "B2", "Bias_sq"] = 0.1433 ** 2
    df_8.loc[df_8["Biome ID"] == "B3", "Bias_sq"] = 0.5408 ** 2
    df_8.loc[df_8["Biome ID"] == "B4", "Bias_sq"] = 0.4746 ** 2
    df_8.loc[df_8["Biome ID"] == "B5", "Bias_sq"] = 0.4981 ** 2
    df_8["V1"] = df_8["Variance"] + df_8["Bias_sq"]
    df_8["V1"] = df_8["V1"]

    df8_dict = {"Grid index": df_8['gpi'],
                "V1": df_8["V1"]}
    pd.DataFrame(df8_dict).to_csv(path_final + "targetVal_" + d + "T223000Z.csv", index=False)
    print("Time 8")
    print(np.max(df_8["V1"]))
    print(np.mean(df_8["V1"]))


def main():
    """
    Main function to post process predictions for plannar
    @return: NA
    """
    # The raw pred consists of SM, uncertainties for all the 9kmx9km SMAP grid
    path_raw = '/Users/archanakannan/Desktop/Archana/USC/Codes/pythonProject/DSHIELD/Final_run_loop_closing/raw_predictions/run001_pred_no_ass/'
    path_intermediate = "/Users/archanakannan/Desktop/Archana/USC/Codes/pythonProject/DSHIELD/Final_run_loop_closing/intermediate_files/run001_pred_no_ass/"
    path_final = "/Users/archanakannan/Desktop/Archana/USC/Codes/pythonProject/DSHIELD/Final_run_loop_closing/pred_csv/run001_no_ass/"

    # Read the modified covgrid.csv file
    path_grid = "/Users/archanakannan/Desktop/Archana/USC/Codes/pythonProject/DSHIELD/Final_run_loop_closing/"

    start = datetime.datetime(2020,10,5,1,30,0) # START DATETIME
    end = datetime.datetime(2020,10,5,22,30,0) # END DATETIME

    create_intermediate_file_from_raw_pred(start, end, path_raw, path_intermediate, path_grid)
    create_target_value_file_from_intermediate_file(start, path_intermediate, path_final)


if __name__ == "__main__":
    main()
