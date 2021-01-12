# Advert Analysis Project

## Intro

Prerequisites:
1. Pandas
1. Numpy
1. Seaborn
1. Matplotlib.pyplot
1. Click

Over the course of 30 days, a business owner advertises his business online. The text of every advertisement is assigned to one of 30 possible colours. The ads are distributed evenly by colour, with 100 of each different colour being viewed daily. These numbers add up to 3,000 daily views that are distributed across the 30 colours. The businesses advertising software automatically tracks all daily views. It also records the daily clicks associated with each of the 30 colours. The software stores this data in a csv table, which holds the clicks-per-day and views-per-day for every specified colour.

We are tasked with finding out if there is a text colour that will render a higher number of clicks than the current colour used by the business, blue. We must find out if there is a colour that generated a higher daily click count mean and then compare it to the daily click means of the adverts in blue, determining if the difference in means is statistically significant through the use of statistical hypothesis testing.

## main() Function:
Arguments:
- *file_path* (required):
    - File path for csv file to be fed into **clicks_csv_to_dataframe**, which loads the csv file into a dataframe, *df*.
- *permutations* (default=30,000):
    - Determines the number of permutations used in our permutation tests.
    - Fed into **find_significant_colours**, which is used to determine if there are any colours that produce a higher number of clicks.
- *heatmap*:
    - If we instead set heatmap to True, then the **generate_heatmap** function is initiated, generating a heatmap of the p-value for each colour paired with blue.

### csv_clicks_to_dataframe
- Loads the csv into a dataframe.
- Minimizes the amount of unnecessary information in the new dataframe:
     - Removes columns containing view counts, as the view count for each colour is 100 daily without exception.
- The column listing the different colours is set to act as the row indices for the dataframe.
- The returned dataframe, *df*, is an argument to both the **find_significant_colours** and **generate_heatmap** functions.

### find_significant_colours
- Primary function in **main()**: used to find any colours that perform better than the blue coloured adverts.
- Arguments:
    - *df*: fed in from **clicks_csv_to_dataframe**.
    - *permutations*: fed in from the second argument in the **main()** function.
    - Both of these are fed through the other two functions in this section.

#### permutation_test:
- A statistical significance test used to find the associated p-value of two separate sample means when population mean and variance are unknown.
- Returns the p-value computed from the mean click counts for blue and another colour, specified by the argument *colour_clicks*.

#### superior_click_colour_p_values:
- The function begins by filtering out all of the colours that have inferior daily mean click counts to blue.
- Iterates through the remaining colours, collecting the relevant p-value in relation to the blue advert clicks using the **permutation_test** function.
- Returns a colour to p-value dictionary (*colour_p_value_dict*).

#### Bonferroni correction
- The final process: carried out in the main body of the **find_significant_colours** function.
- A process used to counteract the effects of data dredging:
    - When oversampling leads to a statistically significant p-value being computed that may be false or misleading.
- The standard significance level is 0.05: a computed p-value lower than 0.05 is considered to show statistical significance.
- The Bonferroni correction divides the significance level by the number of permutation tests that have been carried out:
    - Our function determines the new significance level by dividing 0.05 by the number of colours in *colour_p_value_dict* returned by **superior_click_colour_p_values**.
- Iterates through colours in *colour_p_value_dict*: if a colour's p-value is below the new significance level, the colour and associated p-value are added to a dictionary, *significant_colours*, which is then returned.

### generate_heatmap
- Optional function in **main()**.
- Uses the *colour_p_value_dict* returned by **collect_p_values** (described below).
- Sorts the colour and p-value pairs in *colour_p_value_dict* by their p-values.
- Generates a heatmap of the sorted p-values for each of the 30 colours in the csv file.

#### collect_p_values
- Iterates through each different colour in the dataframe (except blue), collecting the relevant p-value in relation to the blue advert clicks using the **permutation_test** function.
- Returns a colour to p-value dictionary (*colour_p_value_dict*), listing each colour in the dataframe along with its associated p-value.

## Results
The *significant_colours* dictionary returned by **find_significant_colours** is a list comprised of any colours that have a higher mean click count than blue as well as a p-value that shows statistical significance. The dictionary contains the colours that we've shown, through statistical means, to improve the performance of the businesses adverts.
When we run our **main()** function, we are returned only one colour, Ultramarine, with a p-value of roughly 0.0025. Our findings would strongly suggest that the business owner should change his advertising text colour to Ultramarine in order to improve the number of clicks his adverts receive.

### P-Value Heatmap

![P-Value Heatmap](images/p_value_heatmap.png)
|:--:|
| *P-Value Heatmap computed with permutations=30000* |

We can see from this heatmap that, although there are a large number of colours with sufficiently low p-values to suggest statistical significance, the large majority of these colours have a lower mean clicks per day than blue.
