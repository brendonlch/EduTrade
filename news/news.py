import requests
import json
from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
#FOR DEBUGGING - eprint()
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#hardcoded data
data = {
  "meta_data": {
    "api_name": "stock_news_v2", 
    "credit_cost": 5000, 
    "end_date": "yesterday", 
    "end_minute": "23:59:59", 
    "num_total_data_points": 50, 
    "start_date": "yesterday", 
    "start_minute": "00:00:00"
  }, 
  "result_data": {
    "GOOGL": [
      {
        "author": "newsfeedback@fool.com (Billy Duberstein)", 
        "description": "Alphabet has been a long-term winner. So why is 2020 looking like an especially good buying opportunity?", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-07T17:27:00Z", 
        "sentiment": 0.96, 
        "source": "Fool.com", 
        "ticker": "GOOGL", 
        "title": "This Stock Could Be 2020's Best Profit Opportunity", 
        "url": "https://www.fool.com/investing/2020/03/07/this-stock-could-be-2020s-best-profit-opportunity.aspx"
      }, 
      {
        "author": "Jennifer Elias", 
        "description": "Emails from Alphabet CEO Sundar Pichai, CFO Ruth Porat, and marketing chief Lorraine Twohill show how \"every\" Google office is affected by the COVID-19 outbreak in some way.", 
        "event_genre": [
          "Politics", 
          "Corporate Leadership"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": [
          "Sundar Pichai", 
          "Ruth Porat", 
          "Lorraine Twohill"
        ], 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-06T15:37:34Z", 
        "sentiment": -0.15, 
        "source": "CNBC", 
        "ticker": "GOOGL", 
        "title": "Google internal emails reveal how execs are prepping employees for coronavirus response", 
        "url": "https://www.cnbc.com/2020/03/06/coronavirus-google-execs-react-to-outbreak-with-internal-emails.html"
      }, 
      {
        "author": "newsfeedback@fool.com (Danny Vena)", 
        "description": "Alphabet is using the time-honored venture capital model to reduce its potential losses.", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-06T15:44:43Z", 
        "sentiment": -0.4, 
        "source": "Fool.com", 
        "ticker": "GOOGL", 
        "title": "Google's Moonshot Projects Just Got a Lot Less Risky", 
        "url": "https://www.fool.com/investing/2020/03/06/google-moonshot-projects-just-got-lot-less-risky.aspx"
      }, 
      {
        "author": "CNA", 
        "description": "Social media giant Facebook Inc and Alphabet Inc's  Google on Thursday recommended their San Francisco Bay area employees to work from home to minimize the risk of spreading Covid-19.", 
        "event_genre": [
          "Media"
        ], 
        "event_location": None, 
        "event_organization": [
          "Facebook"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-06T06:30:29Z", 
        "sentiment": -0.08, 
        "source": "Channelnewsasia.com", 
        "ticker": "GOOGL", 
        "title": "Facebook, Google ask San Francisco staff to work from home amid coronavirus", 
        "url": "https://www.channelnewsasia.com/news/business/facebook--google-ask-san-francisco-staff-to-work-from-home-amid-coronavirus-12509094"
      }, 
      {
        "author": "CNA", 
        "description": "Social media giant Facebook Inc and Alphabet Inc's  Google on Thursday recommended their San Francisco Bay area employees to work from home to minimize the risk of spreading Covid-19.", 
        "event_genre": [
          "Media"
        ], 
        "event_location": None, 
        "event_organization": [
          "Facebook"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-06T07:46:06Z", 
        "sentiment": -0.08, 
        "source": "Channelnewsasia.com", 
        "ticker": "GOOGL", 
        "title": "Facebook, Google ask San Francisco staff to work from home as coronavirus spreads", 
        "url": "https://www.channelnewsasia.com/news/business/facebook--google-ask-san-francisco-staff-to-work-from-home-as-coronavirus-spreads-12509094"
      }, 
      {
        "author": "John Vincent", 
        "description": "Generation Investment Management\u2019s 13F portfolio value increased 7.5% from $14.54B to $15.64B this quarter.They added Baxter International and increased Twilio while decreasing Analog Devices and Deere.The top three positions are Alphabet, Charles Schwab, and\u2026", 
        "event_genre": [
          "Investment", 
          "Equities"
        ], 
        "event_location": None, 
        "event_organization": [
          "Baxter"
        ], 
        "event_person": [
          "Charles Schwab"
        ], 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-06T08:19:29Z", 
        "sentiment": 0.75, 
        "source": "Seekingalpha.com", 
        "ticker": "GOOGL", 
        "title": "Tracking Al Gore's Generation Investment Management Portfolio - Q4 2019 Update", 
        "url": "https://seekingalpha.com/article/4330204-tracking-al-gores-generation-investment-management-portfolio-q4-2019-update"
      }, 
      {
        "author": "Stone Fox Capital", 
        "description": "Yext returns back to beating consensus targets.The stock trades at a lower P/S multiple than Alphabet despite targeted growth rates of nearly double the search giant.Yext should return to a multiple of 6x FY22 sales estimates of $485 million, or $25.", 
        "event_genre": [
          "Equities"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-05T23:20:38Z", 
        "sentiment": -0.75, 
        "source": "Seekingalpha.com", 
        "ticker": "GOOGL", 
        "title": "Yext: Deep Value", 
        "url": "https://seekingalpha.com/article/4330128-yext-deep-value"
      }, 
      {
        "author": "ASB Capital", 
        "description": "Google is one of the world's most profitable companies.Existing business segments are hugely profitable and the company has more cash than it needs for moonshot investments.With years of excess cash built up and plenty of money coming in to re-invest, look fo\u2026", 
        "event_genre": [
          "Investment", 
          "Equities"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-05T16:14:26Z", 
        "sentiment": 0.78, 
        "source": "Seekingalpha.com", 
        "ticker": "GOOGL", 
        "title": "Search For A Dividend At Alphabet If You're Feeling Lucky", 
        "url": "https://seekingalpha.com/article/4329886-search-for-dividend-alphabet-feeling-lucky"
      }, 
      {
        "author": "CNA", 
        "description": "AT&T Inc  has partnered with Alphabet Inc's  Google Cloud to use 5G edge computing technologies to help clients improve speed and increase security by running applications closer to end users.", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": [
          "T Inc"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-05T17:35:44Z", 
        "sentiment": 0.85, 
        "source": "Channelnewsasia.com", 
        "ticker": "GOOGL", 
        "title": "AT&T partners with Google Cloud for 5G edge computing", 
        "url": "https://www.channelnewsasia.com/news/business/at-t-partners-with-google-cloud-for-5g-edge-computing-12507048"
      }, 
      {
        "author": "Brandy Betz", 
        "description": "<ul><li>Google (<a href='https://seekingalpha.com/symbol/GOOG' title='Alphabet Inc.'>GOOG</a> <font color='green'>+2.8%</font>)(<a href='https://seekingalpha.com/symbol/GOOGL' title='Alphabet Inc.'>GOOGL</a> <font color='green'>+2.7%</font>)\u00a0Cloud <a href=\"ht\u2026", 
        "event_genre": [
          "Product Release"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T20:28:22Z", 
        "sentiment": 0.0, 
        "source": "Seekingalpha.com", 
        "ticker": "GOOGL", 
        "title": "Google Cloud announces four new regions", 
        "url": "https://seekingalpha.com/news/3548696-google-cloud-announces-four-new-regions"
      }, 
      {
        "author": "Jennifer Elias", 
        "description": "Waymo was Google's self-driving car division until 2016, when it became an independent company under Google-parent Alphabet. Overall, the group has spent more than a decade working on self-driving technology, and is just starting to commercialize the technolo\u2026", 
        "event_genre": [
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T20:47:55Z", 
        "sentiment": 0.0, 
        "source": "CNBC", 
        "ticker": "GOOGL", 
        "title": "Alphabet's Waymo shows new Jaguar cars on the heels of investment round", 
        "url": "https://www.cnbc.com/2020/03/04/alphabet-waymo-shows-new-jaguar-cars-on-the-heels-of-investment-round.html"
      }, 
      {
        "author": "Paresh Dave", 
        "description": "The former head of Uber Technologies Inc's self-driving technology unit must pay $179 million to Alphabet Inc's Google to end a legal battle over his split from the company, according to a court order on Wednesday.", 
        "event_genre": [
          "Politics", 
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": [
          "Uber Technologies"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T22:05:48Z", 
        "sentiment": -0.36, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "Ex-Uber self-driving head owes $179 mln to Google in contract dispute", 
        "url": "https://www.reuters.com/article/us-waymo-uber-idUSKBN20R37A"
      }, 
      {
        "author": "By Paresh Dave", 
        "description": "The former head of Uber Technologies Inc's self-driving technology unit must pay $179 million to Google to end a legal battle over his split from the Alphabet Inc unit, according to a court order on Wednesday. Anthony Levandowski, who had been a key engineer \u2026", 
        "event_genre": [
          "Politics", 
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google", 
          "Alphabet Inc", 
          "Uber Technologies"
        ], 
        "event_person": [
          "Anthony Levandowski"
        ], 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T22:11:26Z", 
        "sentiment": -0.36, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Ex-Uber self-driving head owes $179 million to Google in contract dispute", 
        "url": "https://finance.yahoo.com/news/ex-uber-self-driving-head-221126795.html"
      }, 
      {
        "author": "Paresh Dave", 
        "description": "The former head of Uber Technologies Inc's self-driving technology unit must pay $179 million (139.39 million pounds) to Google to end a legal battle over his split from the Alphabet Inc unit, according to a court order on Wednesday.", 
        "event_genre": [
          "Politics", 
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google", 
          "Alphabet Inc", 
          "Uber Technologies"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-05T00:00:57Z", 
        "sentiment": -0.59, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "Ex-Uber self-driving head declares bankruptcy after $179 million loss to Google", 
        "url": "https://uk.reuters.com/article/uk-waymo-uber-idUKKBN20R37E"
      }, 
      {
        "author": "Joel Rosenblatt", 
        "description": "(Bloomberg) -- The self-driving star engineer whose move from Google to Uber triggered one of Silicon Valley\u2019s ugliest trade secret fights filed for bankruptcy on the same day a judge ordered him to pay $179 million over his defection from the Alphabet Inc. u\u2026", 
        "event_genre": [
          "Politics"
        ], 
        "event_location": None, 
        "event_organization": [
          "Alphabet", 
          "Google", 
          "Bloomberg"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-05T00:20:21Z", 
        "sentiment": -0.85, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Ex-Uber Engineer Seeks Bankruptcy After Google Tightens Its Grip", 
        "url": "https://finance.yahoo.com/news/ex-uber-engineer-seeks-bankruptcy-002021038.html"
      }, 
      {
        "author": "Reuters", 
        "description": "The former head of Uber's self-driving technology unit, Anthony Levandowski, filed for bankruptcy protection on Wednesday, shortly after a court confirmed that he must pay $179 million to Google to end a legal battle over his split from the Alphabet unit.", 
        "event_genre": [
          "Politics"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": [
          "Anthony Levandowski"
        ], 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-05T00:35:26Z", 
        "sentiment": -0.59, 
        "source": "CNBC", 
        "ticker": "GOOGL", 
        "title": "Ex-Uber self-driving head Levandowski declares bankruptcy after $179 million loss to Google", 
        "url": "https://www.cnbc.com/2020/03/04/ex-uber-self-driving-head-anthony-levandowski-declares-bankruptcy.html"
      }, 
      {
        "author": "newsfeedback@fool.com (Evan Niu, CFA)", 
        "description": "The tech holding company is increasingly turning to outside investors.", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T13:30:00Z", 
        "sentiment": 0.0, 
        "source": "Fool.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet's Waymo Raises $2.25 Billion", 
        "url": "https://www.fool.com/investing/2020/03/04/alphabets-waymo-raises-225-billion.aspx"
      }, 
      {
        "author": "Eric Feng", 
        "description": "How do we have four trillion-dollar companies growing at startup rates? Because they aren't like other companies.", 
        "event_genre": [
          "Valuation "
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T17:24:45Z", 
        "sentiment": 0.07, 
        "source": "Medium.com", 
        "ticker": "GOOGL", 
        "title": "The Cost-Cutting Shortcut That Helped Apple, Amazon, Alphabet And Microsoft Became $1 Trillion Companies", 
        "url": "https://marker.medium.com/how-microsoft-apple-amazon-and-alphabet-have-created-trillion-dollar-companies-by-lowering-one-34a29c6169a1"
      }, 
      {
        "author": "newsfeedback@fool.com (Danny Vena)", 
        "description": "The Google parent is seeking outside funding for some of its vaunted \"other bets.\"", 
        "event_genre": [
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T21:41:45Z", 
        "sentiment": 0.0, 
        "source": "Fool.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet's Self-Driving Car Segment Waymo Just Raised Billions From Outside Investors", 
        "url": "https://www.fool.com/investing/2020/03/03/alphabet-self-driving-car-waymo-raised-billions.aspx"
      }, 
      {
        "author": "Brandy Betz", 
        "description": "<ul><li>Alphabet (<a href='https://seekingalpha.com/symbol/GOOG' title='Alphabet Inc.'>GOOG</a>,<a href='https://seekingalpha.com/symbol/GOOGL' title='Alphabet Inc.'>GOOGL</a>) <a href=\"https://www.reuters.com/article/us-health-coronavirus-google/google-cance\u2026", 
        "event_genre": [
          "Media"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T22:07:39Z", 
        "sentiment": -0.23, 
        "source": "Seekingalpha.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet cancels Google I/O event", 
        "url": "https://seekingalpha.com/news/3548374-alphabet-cancels-google-i-o-event"
      }, 
      {
        "author": "", 
        "description": "Coronavirus is probably the 1 concern in investors' minds right now. It should be. We estimate that COVID-19 will kill around 5 million people worldwide and there is a 3.3% probability that Donald Trump will die from the new coronavirus (see the details). So,\u2026", 
        "event_genre": [
          "Politics"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": [
          "Donald Trump"
        ], 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-04T01:18:29Z", 
        "sentiment": -0.86, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Hedge Funds Have Never Been This Bullish On Alphabet Inc (GOOGL)", 
        "url": "https://news.yahoo.com/hedge-funds-never-bullish-alphabet-011829943.html"
      }, 
      {
        "author": "Irina Slav", 
        "description": "Waymo, the self-driving car developer of Alphabet, has raised $2.25 billion in funding from external investors, led by tech investment firms including Silver Lake, Alphabet itself, Andreesen Horowitz, and AutoNation. Google began working on a self-driving car\u2026", 
        "event_genre": [
          "Partnership", 
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google", 
          "Silver"
        ], 
        "event_person": [
          "Andreesen Horowitz"
        ], 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T15:30:00Z", 
        "sentiment": 0.0, 
        "source": "Oilprice.com", 
        "ticker": "GOOGL", 
        "title": "Google\u2019s Self-Driving Car Unit Raises $2.25 Billion", 
        "url": "https://oilprice.com/Latest-Energy-News/World-News/Googles-Self-Driving-Car-Unit-Raises-225-Billion.html"
      }, 
      {
        "author": "Reuters, Reuters", 
        "description": "Waymo, the self-driving unit of Alphabet, said it had raised US$2.25 billion in its first external investment round and expects to add more outside investors.The company also disclosed its self-driving trucking business will be called Waymo Via.Founded 11 yea\u2026", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T04:47:54Z", 
        "sentiment": 0.0, 
        "source": "Scmp.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet\u2019s self driving unit Waymo raises US$2.25 billion in first outside funding round", 
        "url": "https://www.scmp.com/tech/start-ups/article/3064721/alphabets-self-driving-unit-waymo-raises-us225-billion-first-outside"
      }, 
      {
        "author": "Reuters Editorial", 
        "description": "Abu Dhabi state fund Mubadala Investment Co was part of a consortium that invested $2.25 billion in Waymo, the self-driving technology company owned by Alphabet Inc, it said on Tuesday.", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": [
          "Abu Dhabi"
        ], 
        "event_organization": [
          "Alphabet Inc", 
          "Waymo", 
          "Mubadala Investment"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T05:21:50Z", 
        "sentiment": 0.0, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "UAE's Mubadala among investors in self-driving firm Waymo", 
        "url": "https://www.reuters.com/article/mubadala-waymo-idUSB2N2A002L"
      }, 
      {
        "author": "Yoel Minkoff", 
        "description": "<ul><li>Highlighting the costs of developing self-driving vehicles, Alphabet's (<a href='https://seekingalpha.com/symbol/GOOG' title='Alphabet Inc.'>GOOG</a>, <a href='https://seekingalpha.com/symbol/GOOGL' title='Alphabet Inc.'>GOOGL</a>) Waymo has raised $2\u2026", 
        "event_genre": [
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T08:00:08Z", 
        "sentiment": 0.0, 
        "source": "Seekingalpha.com", 
        "ticker": "GOOGL", 
        "title": "Waymo raises $2.25B from first outside investors", 
        "url": "https://seekingalpha.com/news/3547862-waymo-raises-2_25b-from-first-outside-investors"
      }, 
      {
        "author": "Reuters Editorial", 
        "description": "Waymo, the self-driving unit of Alphabet Inc, on Monday said it plans to raise $2.25 billion in its first external investment round.", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:14:56Z", 
        "sentiment": 0.0, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "Waymo raises $2.25 bln in external investment round", 
        "url": "https://www.reuters.com/article/waymo-financing-idUSL4N2AV4U8"
      }, 
      {
        "author": "Jennifer Elias", 
        "description": "Silicon Valley firms like Silver Lake invested in Waymo's massive round.", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:18:49Z", 
        "sentiment": 0.36, 
        "source": "CNBC", 
        "ticker": "GOOGL", 
        "title": "Alphabet's self-driving car company Waymo raises a whopping $2.25 billion in first external funding round", 
        "url": "https://www.cnbc.com/2020/03/02/waymo-raises-2point25-billion-in-first-external-funding-round.html"
      }, 
      {
        "author": "Reuters Editorial", 
        "description": "Waymo, the self-driving unit of Alphabet Inc , said on Monday it has raised $2.25 billion in its first external investment round.", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:35:27Z", 
        "sentiment": 0.0, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "Waymo raises $2.25 billion from outside investors, parent Alphabet", 
        "url": "https://ca.reuters.com/article/technologyNews/idCAKBN20P36D-OCATC"
      }, 
      {
        "author": "insider@insider.com (Matthew DeBord)", 
        "description": "Alphabet's self-driving car startup Waymo just raised a whopping $2.25 billion from outside investors \u2014 a first for the company.", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:42:58Z", 
        "sentiment": 0.0, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Waymo just announced a massive $2.25 billion funding round \u2014 the self-driving car company's first-ever raise from outside investors", 
        "url": "https://news.yahoo.com/waymo-just-announced-massive-2-214258667.html"
      }, 
      {
        "author": "Alan Ohnsman, Forbes Staff, Alan Ohnsman, Forbes Staff https://www.forbes.com/sites/alanohnsman/", 
        "description": "The move comes as the company accelerates R&D and expands its robotaxi and robotruck fleets.", 
        "event_genre": [
          "Financing"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:50:28Z", 
        "sentiment": 0.1, 
        "source": "Forbes.com", 
        "ticker": "GOOGL", 
        "title": "Waymo Raises $2.25 Billion In First Funding Round With Non-Alphabet Backers, Including Silver Lake And Andreesen Horowitz", 
        "url": "https://www.forbes.com/sites/alanohnsman/2020/03/02/waymo-raises-225-billion-in-first-funding-round-with-non-alphabet-backers-including-silver-lake-and-andreesen-horowitz/"
      }, 
      {
        "author": "Jason D. Rowley", 
        "description": "The autonomous driving company, previously incubated as an \"other bets\" project under the umbrella of Alphabet, says it has raised a staggering $2.25 billion in financing from investors.", 
        "event_genre": [
          "Financing"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:51:08Z", 
        "sentiment": 0.0, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet\u2019s Autonomous Vehicle Bet Waymo Raises $2.25 Billion In First Outside Funding Round", 
        "url": "https://finance.yahoo.com/news/alphabet-autonomous-vehicle-bet-waymo-215108340.html"
      }, 
      {
        "author": "Kirsten Korosec", 
        "description": "Waymo, the former Google self-driving car project that is now a business under Alphabet, said Monday it raised $2.25 billion in a fundraising round led by Silver Lake, Canada Pension Plan Investment Board, and Mubadala Investment Company. This is the company'\u2026", 
        "event_genre": [
          "Partnership", 
          "Investment"
        ], 
        "event_location": [
          "Silver Lake"
        ], 
        "event_organization": [
          "Google", 
          "Mubadala Investment Company", 
          "Plan Investment Board"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T21:58:12Z", 
        "sentiment": 0.0, 
        "source": "TechCrunch", 
        "ticker": "GOOGL", 
        "title": "Waymo brings in $2.25 billion from outside investors, Alphabet", 
        "url": "https://techcrunch.com/2020/03/02/waymo-brings-in-2-25-billion-from-outside-investors-alphabet/"
      }, 
      {
        "author": "Reuters Editorial", 
        "description": "Waymo, the self-driving unit of Alphabet Inc, said on Monday it has raised $2.25 billion in its first external investment round.", 
        "event_genre": [
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T22:03:29Z", 
        "sentiment": 0.0, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "CORRECTED-UPDATE 1-Waymo raises $2.25 billion from outside investors, parent Alphabet", 
        "url": "https://www.reuters.com/article/waymo-financing-idUSL4N2AV4VF"
      }, 
      {
        "author": "AFP", 
        "description": "Waymo said Monday it had raised $2.25 billion in its first external funding round to help the former Google car unit accelerate its deployment of autonomous cars and trucks. Born in a Google lab devoted to big-vision new technology, Waymo became a subsidiary \u2026", 
        "event_genre": [
          "Partnership", 
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T22:12:00Z", 
        "sentiment": 0.66, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet's Waymo raises $2.25 bn to rev up autonomous projects", 
        "url": "https://news.yahoo.com/alphabets-waymo-raises-2-25-bn-rev-autonomous-221200012.html"
      }, 
      {
        "author": "Reuters Editorial", 
        "description": "Alphabet Inc's Google has asked around 8,000 staff at its European headquarters in Dublin to work from home on Tuesday as a precaution after a staff-member reported flu-like symptoms.", 
        "event_genre": [
          "Politics"
        ], 
        "event_location": [
          "Dublin"
        ], 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T22:27:05Z", 
        "sentiment": 0.0, 
        "source": "Reuters", 
        "ticker": "GOOGL", 
        "title": "Google asks Dublin staff to work from home as coronavirus precaution", 
        "url": "https://www.reuters.com/article/us-health-coronavirus-google-idUSKBN20P39D"
      }, 
      {
        "author": "Cromwell Schubarth", 
        "description": "Waymo, the self-driving unit of Alphabet Inc., on Monday said it has raised $2.25 billion in funding, mostly from outside investors. It is the first external investment for the Mountain View-based autonomous vehicle technology business, which grew out of Goog\u2026", 
        "event_genre": [
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T22:37:09Z", 
        "sentiment": 0.0, 
        "source": "Bizjournals.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet's Waymo scores $2.25B in first outside funding", 
        "url": "https://www.bizjournals.com/sanfrancisco/news/2020/03/02/alphabet-waymo-outside-funding-goog.html?ana=RSS&s=article_search&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+bizj_national+%28Bizjournals+National+Feed%29"
      }, 
      {
        "author": "Mark Bergen and Ira Boudway", 
        "description": "(Bloomberg) -- Waymo raised $2.25 billion from a slate of private equity investors, venture capitalists and automotive companies, the first time Alphabet Inc.\u2019s autonomous vehicle unit has taken outside funds.Silver Lake Management LLC, a private equity firm,\u2026", 
        "event_genre": [
          "M&A", 
          "Investment"
        ], 
        "event_location": None, 
        "event_organization": [
          "Bloomberg", 
          "Management"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T23:54:22Z", 
        "sentiment": 0.0, 
        "source": "Yahoo.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet\u2019s Waymo Raises $2.25 Billion For Driverless Cars", 
        "url": "https://finance.yahoo.com/news/alphabet-waymo-raises-2-25-235422073.html"
      }, 
      {
        "author": "Jon Fingas", 
        "description": "Believe it or not, Waymo hasn't really leaned on outside help to fulfill its self-driving car ambitions -- Alphabet (and earlier, Google) has shouldered much of the load. Now, however, it's expanding its sources of cash. Waymo has announced its first external\u2026", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T23:59:00Z", 
        "sentiment": 0.68, 
        "source": "Engadget", 
        "ticker": "GOOGL", 
        "title": "Waymo's first outside investment round includes car industry heavyweights", 
        "url": "https://www.engadget.com/2020/03/02/waymo-first-external-investment/"
      }, 
      {
        "author": "Matt McFarland, CNN Business", 
        "description": "Waymo, the self-driving arm of Google's parent company Alphabet, announced Monday that it has raised $2.25 billion in its first external round of funding. And, it said, it expects to raise even more money as it looks to scale and expand its business.", 
        "event_genre": [
          "Partnership", 
          "Financing"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T00:06:28Z", 
        "sentiment": 0.32, 
        "source": "CNN", 
        "ticker": "GOOGL", 
        "title": "Self-driving car company Waymo raises $2.25 billion in first external round of funding", 
        "url": "https://www.cnn.com/2020/03/02/tech/waymo-investment-round-funding/index.html"
      }, 
      {
        "author": "Duncan Riley", 
        "description": "Waymo LLC, the self-driving car division of Alphabet Inc. has raised $2.25 billion in its first external fundraising round to further develop its self -driving technology. The round, which came just shy of a year after it was rumored that Alphabet was looking\u2026", 
        "event_genre": [
          "Partnership", 
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": [
          "Alphabet Inc", 
          "Waymo"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T01:23:56Z", 
        "sentiment": -0.25, 
        "source": "Siliconangle.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet\u2019s Waymo self-driving car division raises $2.25B in its first external fundraising", 
        "url": "https://siliconangle.com/2020/03/02/alphabets-waymo-self-driving-car-division-raises-2-25b-first-external-fundraising/"
      }, 
      {
        "author": "Nick Lavars", 
        "description": "It covers almost three quarters of the Earth, but we know only a fraction of what lies beneath the ocean\u2019s surface. Google\u2019s parent company Alphabet has today launched a new initiative called Tidal aimed at changing that, with an overarching objective to use \u2026", 
        "event_genre": [
          "Product Release"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T02:47:08Z", 
        "sentiment": -0.21, 
        "source": "Newatlas.com", 
        "ticker": "GOOGL", 
        "title": "Alphabet launches Tidal, a moonshot to save the world's oceans", 
        "url": "https://newatlas.com/environment/alphabet-tidal-moonshot-save-oceans/"
      }, 
      {
        "author": "Cromwell Schubarth", 
        "description": "Waymo, the self-driving unit of Alphabet Inc. that is continuing to expand its Arizona operations, has raised $2.25 billion in funding, mostly from outside investors. It is the first external investment for the Mountain View-based autonomous vehicle technolog\u2026", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": [
          "Arizona"
        ], 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-03T03:10:10Z", 
        "sentiment": 0.32, 
        "source": "Bizjournals.com", 
        "ticker": "GOOGL", 
        "title": "Waymo, continuing Arizona expansion, scores $2.25B in outside funding", 
        "url": "https://www.bizjournals.com/phoenix/news/2020/03/02/waymo-continuing-arizona-expansion-scores-2-25b-in.html?ana=RSS&s=article_search&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+bizj_phoenix+%28Phoenix+Business+Journal%29"
      }, 
      {
        "author": "By James Pero For Dailymail.com", 
        "description": "A blog post describes project Tidal, which is a part of Alphabet's 'X' division that develops 'moonshot' projects. Tidal is creating a computer vision system that uses AI to monitor fish health.", 
        "event_genre": [
          "Partnership", 
          "Machine Learning"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T17:02:29Z", 
        "sentiment": 0.49, 
        "source": "Dailymail.co.uk", 
        "ticker": "GOOGL", 
        "title": "Alphabet unveils AI camera system that monitors fish populations with the goal of feeding humanity", 
        "url": "https://www.dailymail.co.uk/sciencetech/article-8066017/Alphabet-unveils-AI-camera-monitors-fish-populations-goal-feeding-humanity.html"
      }, 
      {
        "author": "Maria Deutscher", 
        "description": "Google LLC parent Alphabet Inc. is getting into fish farming. Alphabet\u2019s X division, which oversees the company\u2019s emerging research projects, today unveiled a new initiative that aims to harness artificial intelligence to develop more environmentally friendly\u2026", 
        "event_genre": [
          "Product Release"
        ], 
        "event_location": None, 
        "event_organization": [
          "Google"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T17:56:30Z", 
        "sentiment": 0.69, 
        "source": "Siliconangle.com", 
        "ticker": "GOOGL", 
        "title": "Underwater AI: Alphabet\u2019s X lab launches new moonshot to protect the ocean", 
        "url": "https://siliconangle.com/2020/03/02/underwater-ai-alphabets-x-lab-launches-new-moonshot-protect-ocean/"
      }, 
      {
        "author": "Dan Wu and Greg Lindsay", 
        "description": "There\u2019s a way to incorporate tech into a city that creates more equity and connection, not just opportunities to monetize data. Welcome to the city of the future, designed by Sidewalk Labs, an Alphabet subsidiary. Read Full Story", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": None, 
        "event_organization": [
          "Sidewalk Labs"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T06:00:47Z", 
        "sentiment": 0.68, 
        "source": "Fastcompany.com", 
        "ticker": "GOOGL", 
        "title": "How to design a smart city that\u2019s built on empowerment\u2014not corporate surveillance", 
        "url": "https://www.fastcompany.com/90469838/how-to-design-a-smart-city-thats-built-on-empowerment-not-corporate-surveillance?partner=feedburner&utm_source=feedburner&utm_medium=feed&utm_campaign=feedburner+fastcompany&utm_content=feedburner"
      }, 
      {
        "author": "Nick Summers", 
        "description": "Alphabet's moonshot factory is turning its attention back toward the ocean. But whereas Project Foghorn looked to turn seawater into a carbon-neutral fuel, the newly-announced Tidal has a broader mission to protect the sea and its aquatic inhabitants. \"This i\u2026", 
        "event_genre": [
          "Commodities"
        ], 
        "event_location": None, 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-03-02T10:01:00Z", 
        "sentiment": 0.64, 
        "source": "Engadget", 
        "ticker": "GOOGL", 
        "title": "Alphabet's next moonshot: protect the ocean", 
        "url": "https://www.engadget.com/2020/03/02/tidal-alphabet-x-moonshot-ocean-fish-farming/"
      }, 
      {
        "author": "By Henry Martin For Mailonline", 
        "description": "An employee of Alphabet Inc's  Google, who had been in the Zurich office, has tested positive  for coronavirus, the company said. The number of cases in Switzerland has risen to 15.", 
        "event_genre": [
          "Media"
        ], 
        "event_location": [
          "Switzerland", 
          "Zurich"
        ], 
        "event_organization": None, 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-02-28T20:32:33Z", 
        "sentiment": 0.82, 
        "source": "Dailymail.co.uk", 
        "ticker": "GOOGL", 
        "title": "Google employee who was at Zurich office tests positive for coronavirus", 
        "url": "https://www.dailymail.co.uk/news/article-8057501/Google-employee-Zurich-office-tests-positive-coronavirus.html"
      }, 
      {
        "author": "Andrew Bary", 
        "description": "The Dow Had Its Worst Week Since 2008. Where to Find Cash-Rich Stocks in the Coronavirus Selloff. After a pummeling selloff, investors should consider strong industry leaders like Verizon, Berkshire, JPMorgan, and Alphabet", 
        "event_genre": [
          "Equities"
        ], 
        "event_location": None, 
        "event_organization": [
          "Verizon", 
          "Jpmorgan"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-02-29T00:27:00Z", 
        "sentiment": -0.53, 
        "source": "Barrons.com", 
        "ticker": "GOOGL", 
        "title": "Features - Main: The Dow Had Its Worst Week Since 2008. Where to Find Cash-Rich Stocks in the Coronavirus Selloff.", 
        "url": "https://www.barrons.com/articles/cash-rich-stocks-to-buy-amid-the-coronavirus-selloff-51582936062"
      }, 
      {
        "author": "", 
        "description": "LONDON--(BUSINESS WIRE)---- $LIVN--LivaNova PLC announced a research collaboration with Verily, an Alphabet company, to capture measures of depression within its RECOVER clinical study.", 
        "event_genre": [
          "Pharmaceutical"
        ], 
        "event_location": None, 
        "event_organization": [
          "Livnlivanova"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-02-26T21:53:50Z", 
        "sentiment": -0.08, 
        "source": "Businesswire.com", 
        "ticker": "GOOGL", 
        "title": "LivaNova Enters Research Collaboration with Verily to Gain New Insights into Vagus Nerve Stimulation Impact on Difficult-to-Treat Depression", 
        "url": "https://www.businesswire.com/news/home/20200226005968/en/LivaNova-Enters-Research-Collaboration-Verily-Gain-New"
      }, 
      {
        "author": "CNA", 
        "description": "Alphabet Inc's  Waymo and General Motors Co's  Cruise are leading a backlash against a California reporting requirement on self-driving vehicle test data that the companies claim is not relevant or accurate in measuring performance or progress.", 
        "event_genre": [
          "Partnership"
        ], 
        "event_location": [
          "California"
        ], 
        "event_organization": [
          "General Motors Co"
        ], 
        "event_person": None, 
        "event_sector": [
          "Technology"
        ], 
        "published": "2020-02-26T22:25:29Z", 
        "sentiment": 0.42, 
        "source": "Channelnewsasia.com", 
        "ticker": "GOOGL", 
        "title": "Waymo joins backlash against California self-driving data requirement", 
        "url": "https://www.channelnewsasia.com/news/business/waymo-joins-backlash-against-california-self-driving-data-requirement-12474166"
      }
    ]
  }
}

class NewsObj(db.Model):
      __tablename__ = 'news'

      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(248), nullable=False)
      author = db.Column(db.String(248), nullable=False)
      description = db.Column(db.String(2048), nullable=False)
      published = db.Column(db.String(1000), nullable=False)
      ticker = db.Column(db.String(100), nullable=False)
      url = db.Column(db.String(2048), nullable=False)

      def __init__(self, id, title, author, description, published, ticker, url): #Initialise the objects
       self.id = id
       self.title = title
       self.author = author
       self.description = description
       self.published = published
       self.ticker = ticker
       self.url = url

      def json(self): 
        return {"id": self.id, "title": self.title, "author": self.author, "description": self.description, "published": self.published, "ticker": self.ticker,"url": self.url}


@app.route("/")
def get_news_by_tickers():
  new_data = data['result_data']
  count = 0
  new_dict = {}
  news_objects = {}
  obj_of_news = {}

  for data1 in new_data['GOOGL']:
    count += 1
    new_dict[count] = data1
    for i in range (1 , len(new_dict) + 1):
      # if new_dict[i]['author'] == "":
      #   x = NewsObj(i, new_dict[i]['title'],"No author", new_dict[i]['description'], new_dict[i]['published'], new_dict[i]['ticker'], new_dict[i]['url'])
      #   news_objects[i] = x.json()
      # else:
        y = NewsObj(i, new_dict[i]['title'], new_dict[i]['author'], new_dict[i]['description'], new_dict[i]['published'], new_dict[i]['ticker'], new_dict[i]['url'])
        news_objects[i] = y.json()
  # return news_objects
  try:
    for i in range (1, len(news_objects) + 1):
      #return news_objects
      # return(news_objects)
      bird = news_objects[i]
      obj = NewsObj(**bird)
      # return obj     
      db.session.add(obj)
      db.session.commit()
  except:
    return "FAIL"
  return "Success"
  
app.run(port=6002, debug=True)
