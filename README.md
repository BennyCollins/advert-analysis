# Advert Analysis Project

## Intro

Prerequisites:
1. Pandas
1. Numpy
1. Seaborn
1. Matplotlib.pyplot
1. Click

Over the course of 30 days, a business owner advertises his business online. The text of every ad is assigned to one of 30 possible colours. The advertisements are distributed evenly by colour, with 100 of each different colour being viewed daily. These numbers add up to 3,000 daily views that are distributed across the 30 colours. The businesses advertising software automatically tracks all daily views. It also records the daily clicks associated with each of the 30 colours. The software stores this data in a table, which holds the clicks-per-day and views-per-day for every specified colour.

We are tasked with finding out if there is a text colour that will render a higher number of clicks than the current colour used by the business, blue. We must find out if there is a colour that generated a higher click count mean and then determine if this difference in means is statistically significant through the use of statistical hypothesis testing.

## main() Function:

### csv_clicks_to_dataframe

The first argument for the **main()** function is the required argument *file_path*. This is fed into our function **clicks_csv_to_dataframe**, which is used to load the csv file containing click counts into a dataframe. This function also minimizes the amount of unnecessary information in the new dataframe by removing the columns containing the view counts, as the view count for each colour is 100 daily without exception. Finally the column listing the different colours is set to act as the row indices for the dataframe. The returned dataframe, *df*, is an argument to both the **bonferroni_correction** and **generate_heatmap** functions, and is fed through all of the functions that are called within these two.

### bonferroni_correction

A permutation test is a statistical significance test that is utilised to find the associated p-value of two separate sample means when population mean and variance are unknown. Our function **permutation_test** returns the p-value computed from the mean click counts for blue and another colour specified by the argument *colour_clicks*.

The functions **collect_p_values** and **superior_click_colour_p_values** both do essentially the same thing. They iterate through each different colour in the dataframe (except blue), collecting its relevant p-value in relation to the blue advert clicks using the **permutation_test** function. They return a colour to p-value dictionary (*colour_p_value_dict*), which lists each colour in the dataframe along with its associated p-value. The only difference between **collect_p_values** and **superior_click_colour_p_values** is that the latter begins by filtering out all of the colours that have inferior mean click counts to blue.

Finally, the primary function used in **main()** is **bonferroni_correction**. The first argument for this function is *df*, as mentioned earlier. The second argument for **bonferroni_correction** is *permutations*, which is fed in from the second argument in the **main()** function (*permutations*, default = 30,000). *permutations*, like *df*, is fed through the previous two functions described above, where *permutations* determines the number of permutations used in **permutation_test**.

Bonferroni correction is a process used to counteract the effects of data dredging, where oversampling leads to a statistically significant p-value being computed that may be false or misleading. The standard significance level is 0.05, meaning a computed p-value lower than 0.05 is considered to show statistical significance. The Bonferroni correction divides this significance level by the number of different permutation tests that have been run. We use our **superior_click_colour_p_values** function to obtain our *colour_p_value_dict* in order to minimize the number of permutation tests we are running, decreasing the effects of data dredging.

Our **bonferroni_correction** function then determines our new significance level by dividing 0.05 by the number of colours in *colour_p_value_dict*, which is equal to the number of permutation tests we have run. **bonferroni_correction** iterates through the colours in *colour_p_value_dict* and if a p-value is below the new significance level *(0.05/5 = 0.01)*, then the colour and associated p-value are added to a dictionary, *significant_colours*, which is then returned. This dictionary is a list comprised of any colours that have a higher mean click count than blue as well as a p-value that shows statistical significance. When we run the Bonferroni part of our **main()** function, we are returned only one colour, Ultramarine, with a p-value of roughly 0.0025. Our findings would strongly suggest that the business owner should change his advertising text colour to Ultramarine in order to improve the number of clicks his adverts receive.

### generate_heatmap

The final argument in the **main()** function is *heatmap* (default = False). If we instead set heatmap to True, then **main()** will initiate the **generate_heatmap** function. This function uses the *colour_p_value_dict* returned by the **collect_p_values** function described earlier. **generate_heatmap** sorts the colour and p-value pairs by their p-values and then generates a heatmap of p-values for each colour.

## P-Value Heatmap

![P-Value Heatmap](images/p_value_heatmap.png)
|:--:|
| *P-Value Heatmap computed with permutations=30000* |
# advert-analysis
