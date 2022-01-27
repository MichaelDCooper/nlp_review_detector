import unittest
import requests
from bs4 import BeautifulSoup
from main import fetch_reviews, find_kgb, build_review_bodies, fetch_review_attr

class MainTest(unittest.TestCase):
    def test_fetch_reviews(self):
        reviews = fetch_reviews()
        actual_len = len(reviews)
        expected_len = 50 # 5 pages at 10 results per page
        self.assertEqual(actual_len, expected_len) 

    def test_find_kgb(self):
        # Ideally this step would be mocked 
        reviews = fetch_reviews(2)
        review_len = len(reviews)
        # Doesn't test anything new but is necessary to confirm future test failure
        self.assertEqual(review_len, 10) 

        # Tests initial kgb results
        trunc_reviews = reviews[:2]
        kgb_endorsements = find_kgb(trunc_reviews)
        self.assertEqual(len(kgb_endorsements), 2)

        # Tests negative reviews are filtered before hitting analyzer
        trunc_reviews[0].recommendation = 'No'
        kgb_endorsements = find_kgb(trunc_reviews)
        self.assertEqual(len(kgb_endorsements), 1)

    def test_exceptions(self):
        # Tests that content values match and that scraping was successful 
        with self.assertRaises(ValueError) as exception_context:
            build_review_bodies([],[])
        self.assertEqual(
            str(exception_context.exception),
            'Invalid content or title lists'
        )

        with self.assertRaises(ValueError) as exception_context:
            build_review_bodies(['test'],[])
        self.assertEqual(
            str(exception_context.exception),
            'Invalid content or title lists'
        )

        # Raises when page attr is not found
        with self.assertRaises(ValueError) as exception_context:
            review_url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page1/'
            requested_page = requests.get(review_url)
            page_content = requested_page.content
            soup = BeautifulSoup(page_content, 'html.parser')
            fetch_review_attr(soup, "doesnt_exist", "bad_class", True)
        self.assertEqual(
            str(exception_context.exception),
            'Attribute not found'
        )


