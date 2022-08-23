from performance_pkg import graphing_functions as gf
import sys
path_to_csv = sys.argv[1]
path_to_save = sys.argv[2]
df = gf.load_and_clean(path_to_csv)
for i in df.columns:
    gf.plot_all(df[i], df, path_to_save)