import pandas as pd

# We use the Pandas library to read the contents of the scraped data
# obtained by scrapy
df = pd.read_csv('scrapyData.csv', encoding='utf-8')

# Now we remove duplicate rows (reviews)
df.drop_duplicates(inplace=True)

# Drop the reviews with 3 stars, since we're doing Positive/Negative
# sentiment analysis.
df = df[df['stars'] != '3 of 5 stars']

def get_class(stars):
	score = int(stars[0])
	if score > 3:
	    return 'Good'
	else:
	    return 'Bad'

# Transform the number of stars into Good and Bad tags.
df['true_category'] = df['stars'].apply(get_class)

df = df[['hotel', 'title', 'content', 'true_category']]

# Print a histogram of sentiment values
print(df['true_category'].value_counts())

# Write the data into a CSV file
df.to_csv('itemsHotel.csv', header=False, index=False, encoding='utf-8')
