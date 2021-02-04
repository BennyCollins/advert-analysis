#! /usr/bin/env python

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import click


def clicks_csv_to_dataframe(csv_file_path):
    df = pd.read_csv(csv_file_path)
    view_columns = [column for column in df.columns if 'View' in column]
    df.drop(columns=view_columns, inplace=True)
    df.set_index('Color', inplace=True)
    return df


def permutation_test(df, colour_clicks, permutations):
    num_extreme_values = 0
    blue_clicks = df.Blue.values
    extreme_mean_diff = abs(blue_clicks.mean() - colour_clicks.mean())
    total_ad_clicks = np.hstack([blue_clicks, colour_clicks])
    for _ in range(permutations):
        np.random.shuffle(total_ad_clicks)
        random_ad_clicks_1 = total_ad_clicks[:20]
        random_ad_clicks_2 = total_ad_clicks[20:]
        shuffled_mean_diff = abs(random_ad_clicks_1.mean() - random_ad_clicks_2.mean())
        if shuffled_mean_diff >= extreme_mean_diff:
            num_extreme_values += 1
    p_value = num_extreme_values / permutations
    return p_value


def collect_p_values(df, permutations):
    colour_p_value_dict = {}
    df_transposed = df.T
    df_not_blue = df_transposed.drop(columns='Blue')
    for colour, values in df_not_blue.items():
        colour_clicks = np.array(values)
        p_value = permutation_test(df_transposed, colour_clicks, permutations)
        colour_p_value_dict[colour] = p_value
    return colour_p_value_dict


def generate_heatmap(df, permutations):
    colour_p_value_dict = collect_p_values(df, permutations)
    sorted_colours, sorted_p_values = zip(*sorted(colour_p_value_dict.items(), key=lambda x: x[1]))
    plt.figure(figsize=(10, 10))
    sns.heatmap([[p_value] for p_value in sorted_p_values], cmap='YlGnBu', annot=True, xticklabels=['p-value'], yticklabels=sorted_colours)


def superior_click_colour_p_values(df, permutations):
    colour_p_value_dict = {}
    df_transposed = df.T
    blue_clicks = df.T.Blue.values
    superior_colours = df[df.T.mean().values > blue_clicks.mean()]
    for colour, values in superior_colours.T.items():
        colour_clicks = np.array(values)
        p_value = permutation_test(df_transposed, colour_clicks, permutations)
        colour_p_value_dict[colour] = p_value
    return colour_p_value_dict


def find_significant_colours(df, permutations):
    significant_colours = {}
    colour_p_value_dict = superior_click_colour_p_values(df, permutations)
    significance_level = 0.05 / len(colour_p_value_dict)
    superior_colours, p_values = zip(*colour_p_value_dict.items())
    for colour in superior_colours:
        if colour_p_value_dict[colour] < significance_level:
            significant_colours[colour] = colour_p_value_dict[colour]
    return significant_colours


@click.command()
@click.option("--file_path", required=True , help="CSV file path")
@click.option("--permutations", default=30000, help="Number of permutations")
@click.option("--heatmap", is_flag=True, help="Generate heatmap?")
def main(file_path, permutations, heatmap):
    df = clicks_csv_to_dataframe(file_path)
    significant_colours = find_significant_colours(df, permutations)
    if heatmap:
        generate_heatmap(df, permutations)
        if permutations > 30000:
            plt.savefig("colours_p_value_heatmap.png")
        plt.show()
    print(significant_colours)


if __name__ == "__main__":
    main()
