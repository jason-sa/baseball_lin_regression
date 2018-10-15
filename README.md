# Predicting MLB salary in year 6 with rookie stats

This repository scrapes MLB rookie stats and salary data from [Baseball Reference](https://www.baseball-reference.com/), and builds linear models to address this questions,

* What will be a player's salary in year 6 given only rookie year performance?

## Repository Structure

* Code
  * [get_player.py](./get_player.py) - Web-scraping script to gather rookie stats and player salary data
  * [basebally.py](./baseball.py) - All functions used to transform the scraped HTML into data frames, and the linear model selection logic.
* Notebooks
  * [Data Loading](./Data\ Loading.ipynb) - Notebook utilized to proto-type the web-scraping algorithms needed to get the data.
  * [Scrapping to DF] - Transform the scrapped HTML into feature data frames
  * [First Model] - Build different features, train different models, and select best model
* Presentation
  * [Presentation] -  High-level presentation of the results.
  * [Sumamry] -  Detaield and more technical summary of the results