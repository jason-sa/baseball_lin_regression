# Predicting MLB salary in year 6 with rookie stats

This repository scrapes MLB rookie stats and salary data from [Baseball Reference](https://www.baseball-reference.com/), and builds linear models to address this questions,

* What will be a player's salary in year 6 given only rookie year performance?

## Repository Structure

* Code
  * [get_player.py](./get_player.py) - Web-scraping script to gather rookie stats and player salary data
  * [basebally.py](./baseball.py) - All functions used to transform the scraped HTML into data frames, and the linear model selection logic.
* Notebooks
  * [Data Loading](./Data&#32;Loading.ipynb) - Notebook utilized to proto-type the web-scraping algorithms needed to get the data.
  * [Scraping to DF](./Scraping&#32;to&#32;DF.ipynb) - Transform the scrapped HTML into feature data frames
  * [First Model](./First&#32;Model.ipynb) - Build different features, train different models, and select best model
* Presentation
  * [Presentation](./presentation/BaseballSalaryPrediction.pdf) -  High-level presentation of the results.
  * [Summary](./Summary.pdf) -  Detaield and more technical summary of the results