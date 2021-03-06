# NLP Review Detector

## Description
This application is an NLP powered Python script that scrapes the internet and detects 'overly positive' reviews that may have been written by bots.

It does so by: 
1. Using `Beautiful Soup` to scrape a website, currently set to `www.dealerrater.com`
2. Parses the site for reviews using Python's native `html.parser`
3. Uses [Flair Nlp](https://github.com/flairNLP/flair) to detect how positive a review is based on the content of the review. Since the goal is to determine being overly positive, and not to detect other ways the review may have suspicious origin, the strategy used is based on the premise that any bot farm would check their messages for sentiment before sending them out, and therefore, could be detected by checking sentiment programmatically.   
5. After determing which reviews are most likely to be fake, the program outputs the 3 worst offenders to the console

## Usage
The following Python pacakages are necessary for running the scrip. I recommend using `pip` to download them 
1. [requests](https://docs.python-requests.org/en/latest/)                                                                           
2. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)                                                             
3. [Flair Nlp](https://github.com/flairNLP/flair) 

After the packages have been installed you can run: 
`python3 main.py` to run the application 
and 
`python -m unittest test.py` to run the test suite

#### Note: Due to flairs runtime, the application can take up to 5 minutes to complete on first run

## Output
### Main Output:
![Main Output](https://github.com/MichaelDCooper/nlp_review_detector/blob/main/img/review_detector_main.png?raw=true)

### Test Output: 
![Test Output](https://github.com/MichaelDCooper/nlp_review_detector/blob/main/img/review_detector_test.png?raw=true)

