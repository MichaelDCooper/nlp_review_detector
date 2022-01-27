import requests 
from bs4 import BeautifulSoup
from flair.models import TextClassifier
from flair.data import Sentence

class Review(object):
    def __init__(self, review_content, review_author, review_recommendation):
        self.content = review_content                                                           
        self.author = review_author
        self.recommendation = review_recommendation
        self.sentiment = 0

# Finds a given review attribute such as a User or Recommendation
# then removes both html formatting and (if necessary) any special characters
def fetch_review_attr(soup, html_attr, class_desc, bypass_formatting = False):
    attrs_with_formatting = find_and_unwrap(soup, html_attr, class_desc)
    if bypass_formatting:
        return attrs_with_formatting
    return remove_special_formatting(attrs_with_formatting)

def find_and_unwrap(soup, html_attr, class_desc):
    initial_results = soup.find_all(html_attr, class_=class_desc)
    initial_results_len = len(initial_results)
    if initial_results_len == 0:
        raise ValueError('Attribute not found')

    final_results = []
    for i in range(len(initial_results)):
        final_results.append(initial_results[i].contents[0])
    return final_results

def remove_special_formatting(attr_list):
    final_results = []
    for attr in attr_list:
        tmp = attr
        # Removes 'by' from author
        if attr[0:3] == 'by ':
            tmp = attr[3:]
        # Removes special characters (\n\r) from recommendation
        tmp = ''.join(c for c in tmp if c.isalnum())
        final_results.append(tmp)
    return final_results

def build_review_bodies(title_list, content_list):
    review_bodies = []
    title_list_len = len(title_list)
    content_list_len = len(content_list)

    if title_list_len == 0 or content_list_len == 0 or content_list_len != title_list_len:
        raise ValueError('Invalid content or title lists')

    for i in range(title_list_len):
        review_bodies.append(f'{title_list[i]} {content_list[i]}')
    return review_bodies

# Scrapes dealer rater website, parses incoming data, and returns a list of reviews
def fetch_reviews(pages = 6): 
    review_list = []
    for i in range(1, pages):
        review_url = f'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page{i}/'
        requested_page = requests.get(review_url)
        page_content = requested_page.content
        soup = BeautifulSoup(page_content, 'html.parser')

        review_title_list = fetch_review_attr(soup, "span", "review-title bolder font-18 italic", True)
        review_content_list = fetch_review_attr(soup, "span", "review-whole display-none", True)
        review_body_list = build_review_bodies(review_title_list, review_content_list)

        review_author_list = fetch_review_attr(soup, "span", "italic font-16 bolder notranslate")
        review_recommendation_list = fetch_review_attr(soup, "div", "td small-text boldest")

        for i in range(len(review_body_list)):
            content = review_body_list[i]
            author = review_author_list[i]
            recommendation = review_recommendation_list[i]
            review_list.append(Review(content, author, recommendation))

    return review_list

# This function implements the sorting functionality that determines how positive a review is
def find_kgb(reviews):
    # Removing all reviews where the user would not recommend the dealership
    recommended_reviews = []
    for review in reviews:
        if review.recommendation == 'Yes':
            recommended_reviews.append(review)

    for review in recommended_reviews:
        classifier = TextClassifier.load('en-sentiment')
        target = Sentence(review.content)
        classifier.predict(target)
        score_str = str(target.labels[0])
        score_filter = filter(str.isdigit, score_str)
        score = int("".join(score_filter)) * .01
        review.sentiment = score
    recommended_reviews.sort(key=lambda r: r.sentiment, reverse=True)
    return recommended_reviews

def print_reviews(reviews, count):
    for i in range(count):
        review = reviews[i]
        print(f'Review Content: {review.content} \n Review Author: {review.author} \n Positivity Score: {review.sentiment}\n\n')

def main():
    review_list = fetch_reviews()
    kgb_endorsements = find_kgb(review_list)
    print_reviews(kgb_endorsements, 3)

if __name__ == "__main__":
    main()
