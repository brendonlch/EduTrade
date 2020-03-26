import requests
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
#hardcoded data suppose to be for testing

news_finance = {
  "GOOGL": [
    {
      "author": "Jennifer Elias", 
      "description": "Alphabet's self-driving company previously said it temporarily paused its Waymo One rider service in Metro Phoenix while keeping driverless rides and some driver testing.", 
      "event_genre": [
        "Machine Learning"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T21:15:31Z", 
      "sentiment": 0.0, 
      "source": "CNBC", 
      "ticker": "GOOGL", 
      "title": "Alphabet self-driving car company Waymo suspends all driving operations in Phoenix and Detroit, internal memos show", 
      "url": "https://www.cnbc.com/2020/03/20/alphabet-waymo-suspends-driving-operations-in-phoenix-detroit.html"
    }, 
    {
      "author": "Eric Basmajian", 
      "description": "Financial markets remain highly dislocated with extraordinary volatility.The Fed's first priority is to stabilize the Treasury bond market.The Fed has unveiled the entire 2008 crisis playbook, only in bigger size.Cries for MMT and Helicopter Money have grown \u2026", 
      "event_genre": [
        "Market performance"
      ], 
      "event_location": None, 
      "event_organization": [
        "Fed"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T13:23:00Z", 
      "sentiment": -0.51, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Making Sense Of The Fed's Alphabet Soup", 
      "url": "https://seekingalpha.com/article/4333129-making-sense-of-feds-alphabet-soup"
    }, 
    {
      "author": "Maggie Fitzgerald", 
      "description": "The firm said Amazon, Facebook, Alphabet, Wix.com and Chegg have the most potential to outperform in the next year.", 
      "event_genre": [
        "Market performance"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T13:38:00Z", 
      "sentiment": 0.59, 
      "source": "CNBC", 
      "ticker": "GOOGL", 
      "title": "With tech stocks down nearly 30%, Jefferies sorts through winners and losers", 
      "url": "https://www.cnbc.com/2020/03/20/with-tech-stocks-down-nearly-30percent-jefferies-sorts-through-winners-and-losers.html"
    }, 
    {
      "author": "Kris Holt", 
      "description": "Waymo put most of its services on hold earlier this week, except for fully driverless rides in Phoenix and some testing, to slow the spread of COVID-19. Just a few days later, the Alphabet company has opted to suspend all of its services until April...", 
      "event_genre": [
        "Equities", 
        "Machine Learning"
      ], 
      "event_location": [
        "Phoenix"
      ], 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T15:14:00Z", 
      "sentiment": -0.32, 
      "source": "Engadget", 
      "ticker": "GOOGL", 
      "title": "Waymo suspends all services until at least April 7th", 
      "url": "https://www.engadget.com/2020/03/20/waymo-services-suspended-coronavirus-covid-19/"
    }, 
    {
      "author": "", 
      "description": "Waymo has extended the partial suspension of its autonomous vehicle service pilots to include fully driverless vehicle testing, the company confirmed on Friday. While Alphabet-owned Waymo had already stopped operation of the autonomous driving vehicles in its\u2026", 
      "event_genre": [
        "Machine Learning"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T15:40:18Z", 
      "sentiment": -0.23, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Waymo suspends all self-driving services in light of coronavirus pandemic", 
      "url": "https://news.yahoo.com/waymo-suspends-self-driving-services-154018604.html"
    }, 
    {
      "author": "Eric J. Savitz", 
      "description": "Big Tech \u2014 the Growth Play \u2014 Is Now a Defensive Stalwart Cash is now king. And Alphabet, Amazon, Apple, Microsoft, and Facebook have a combined $587 billion in cash on hand\u2014and just $207 billion in debt.", 
      "event_genre": [
        "Equities"
      ], 
      "event_location": None, 
      "event_organization": [
        "Facebook", 
        "Apple", 
        "Microsoft"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T16:58:14Z", 
      "sentiment": 0.8, 
      "source": "Barrons.com", 
      "ticker": "GOOGL", 
      "title": "Technology Trader: Coronavirus Has Created a Rare Opportunity to Buy Dominant Tech Companies on the Cheap", 
      "url": "https://www.barrons.com/articles/coronavirus-creates-buying-opportunity-for-dominant-tech-stocks-51584722749"
    }, 
    {
      "author": "Oleh Kombaiev", 
      "description": "Fundamentally, Alphabet is undervalued. But does it matter now?Alphabet's beta coefficient has declined dramatically.\u00a0And this is a good sign because the company is now less prone to the market volatility.Now is the worst time to predict, but I hardly believe\u2026", 
      "event_genre": [
        "Equities"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T06:00:17Z", 
      "sentiment": -0.14, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet: Path To $1000, But Hardly Much Lower", 
      "url": "https://seekingalpha.com/article/4333183-alphabet-path-to-1000-hardly-much-lower"
    }, 
    {
      "author": "Foo Yun Chee", 
      "description": "Alphabet Inc's YouTube said on Friday it will reduce its streaming quality in the European Union to avoid straining the internet as thousands of Europeans, constrained by the coronavirus outbreak, switch to teleworking and watch videos at home.", 
      "event_genre": [
        "Politics", 
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "European Union"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T07:09:34Z", 
      "sentiment": -0.53, 
      "source": "Reuters", 
      "ticker": "GOOGL", 
      "title": "Exclusive: YouTube to reduce streaming quality in Europe due to coronavirus", 
      "url": "https://ca.reuters.com/article/technologyNews/idCAKBN2170OP-OCATC"
    }, 
    {
      "author": "Samuel Stolton", 
      "description": "Alphabet's YouTube said on Friday (20 March) it will reduce its streaming quality in the European Union to avert internet gridlock as thousands of Europeans, constrained by the coronavirus outbreak, switch to working from home.", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": [
        "Youtube", 
        "European Union"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-20T09:36:17Z", 
      "sentiment": -0.27, 
      "source": "Euractiv.com", 
      "ticker": "GOOGL", 
      "title": "YouTube to reduce streaming quality in Europe due to coronavirus", 
      "url": "http://www.euractiv.com/section/digital/news/youtube-to-reduce-streaming-quality-in-europe-due-to-coronavirus/"
    }, 
    {
      "author": "Reuters", 
      "description": "The United States imposed fresh Iran-related sanctions on Thursday, targeting five firms, the Treasury Department said on its website. The firms include Petro Grand FZE, Alphabet International DMCC, Swissol Trade DMCC, Alam Althrwa General Trading LLC, and Al\u2026", 
      "event_genre": [
        "Politics", 
        "Trade"
      ], 
      "event_location": [
        "States"
      ], 
      "event_organization": [
        "Treasury", 
        "Petro", 
        "Trading Llc"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-19T14:27:16Z", 
      "sentiment": 0.82, 
      "source": "Ynetnews.com", 
      "ticker": "GOOGL", 
      "title": "U.S. issues new Iran-related sanctions", 
      "url": "https://www.ynetnews.com/article/rkoxZZW8L"
    }, 
    {
      "author": "Paresh Dave", 
      "description": "Some app developers say Alphabet Inc's Google is increasingly pressing them to embed code in their own products that will deepen Google's access to data on consumers, giving the company a leg up on rivals.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-19T10:00:00Z", 
      "sentiment": 0.05, 
      "source": "Reuters", 
      "ticker": "GOOGL", 
      "title": "FOCUS-Google critics see its Firebase tools as another squeeze play", 
      "url": "https://www.reuters.com/article/us-google-antitrust-focus-idUSKBN2161GA"
    }, 
    {
      "author": "", 
      "description": "When President Donald Trump finally addressed the nation\u2019s dire shortage of testing capabilities for the coronavirus on March 13, he did what many people do when they seek answers: He turned to Google. But Trump\u2019s announcement that the Alphabet Inc. unit woul\u2026", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google", 
        "Alphabet Inc"
      ], 
      "event_person": [
        "Donald Trump"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-19T10:13:01Z", 
      "sentiment": -0.32, 
      "source": "Bloomberglaw.com", 
      "ticker": "GOOGL", 
      "title": "Big Tech Tries to Help the US Narrow the Virus Testing Gap - Bloomberg Law", 
      "url": "https://news.bloomberglaw.com/health-law-and-business/big-tech-tries-to-help-the-u-s-narrow-the-virus-testing-gap"
    }, 
    {
      "author": "CNA", 
      "description": "Some app developers say Alphabet Inc's  Google is increasingly pressing them to embed code in their own products that will deepen Google's access to data on consumers, giving the company a leg up on rivals.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-19T10:21:21Z", 
      "sentiment": 0.05, 
      "source": "Channelnewsasia.com", 
      "ticker": "GOOGL", 
      "title": "Google critics see its Firebase tools as another squeeze play", 
      "url": "https://www.channelnewsasia.com/news/business/google-critics-see-its-firebase-tools-as-another-squeeze-play-12556714"
    }, 
    {
      "author": "CNA", 
      "description": "BRUSSELS: EU Industry Chief Thierry Breton has called on video streaming platforms such as Netflix and Alphabet unit YouTube to take measures to prevent Internet gridlock caused by people teleworking and streaming at home due to the coronavirus outbreak.The E\u2026", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Netflix", 
        "Brussels Eu Industry"
      ], 
      "event_person": [
        "Thierry Breton"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-19T11:03:32Z", 
      "sentiment": -0.64, 
      "source": "Channelnewsasia.com", 
      "ticker": "GOOGL", 
      "title": "Internet under strain from streaming services during COVID-19 crisis: European Commission", 
      "url": "https://www.channelnewsasia.com/news/world/internet-under-strain-from-streaming-services-during-covid-19-12556850"
    }, 
    {
      "author": "Foo Yun Chee", 
      "description": "EU Industry Chief Thierry Breton has called on video streaming platforms such as Netflix and Alphabet unit YouTube to take measures to prevent internet gridlock caused by people teleworking and streaming at home due to the coronavirus outbreak.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Netflix"
      ], 
      "event_person": [
        "Thierry Breton"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-18T20:33:03Z", 
      "sentiment": 0.38, 
      "source": "Reuters", 
      "ticker": "GOOGL", 
      "title": "UPDATE 1-EU wants streaming platforms to ease internet gridlock amid virus crisis", 
      "url": "https://www.reuters.com/article/us-health-coronavirus-internet-idUSKBN2153RV"
    }, 
    {
      "author": "Techinvestornews.com", 
      "description": "EU Industry Chief Thierry Breton has called on video streaming platforms such as Netflix and Alphabet unit YouTube to take measures to prevent internet gridlock caused by people teleworking and streaming at home due to the coronavirus outbreak.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Netflix"
      ], 
      "event_person": [
        "Thierry Breton"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-18T22:54:00Z", 
      "sentiment": -0.36, 
      "source": "Techinvestornews.com", 
      "ticker": "GOOGL", 
      "title": "EU wants streaming platforms to ease internet gridlock amid virus crisis (Reuters: Internet News)", 
      "url": "https://www.techinvestornews.com/https://www.techinvestornews.com/Tech-News/Latest-Headlines/eu-wants-streaming-platforms-to-ease-internet-gridlock-amid-virus-crisis"
    }, 
    {
      "author": "Jon Fingas", 
      "description": "Alphabet's COVID-19 screening site might serve as a relief to those eager to determine if they need to get tested, but it's also raising some privacy concerns in Congress.  Five Democratic senators have sent letters to Vice President Mike Pence and Alphabet c\u2026", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": [
        "Mike Pence"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-19T00:19:00Z", 
      "sentiment": 0.56, 
      "source": "Engadget", 
      "ticker": "GOOGL", 
      "title": "Senators ask Alphabet how it will protect COVID-19 screening site data", 
      "url": "https://www.engadget.com/2020-03-18-senators-ask-alphabet-about-covid-19-site-privacy.html"
    }, 
    {
      "author": "Marel.", 
      "description": "The coronavirus is causing massive disruption to life and business, and critical industries are facing incredible strain. Alphabet is under pressure along with the markets globally.Alphabet's strong cash flow generation is supporting its strong cash balance, \u2026", 
      "event_genre": [
        "Equities"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-18T13:07:36Z", 
      "sentiment": 0.65, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet: Taking Advantage Of The Sell Off, But With Caution", 
      "url": "https://seekingalpha.com/article/4332705-alphabet-taking-advantage-of-sell-off-caution"
    }, 
    {
      "author": "Yoel Minkoff", 
      "description": "<ul><li>The U.S. government is in active talks with Facebook (NASDAQ:<a href='https://seekingalpha.com/symbol/FB' title='Facebook, Inc.'>FB</a>), Google (<a href='https://seekingalpha.com/symbol/GOOG' title='Alphabet Inc.'>GOOG</a>, <a href='https://seekingal\u2026", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Facebook Nasdaq"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-18T09:02:54Z", 
      "sentiment": 0.08, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Harnessing location data to combat coronavirus", 
      "url": "https://seekingalpha.com/news/3552783-harnessing-location-data-to-combat-coronavirus"
    }, 
    {
      "author": "Matthew Finnegan, Matthew Finnegan", 
      "description": "An online screening and testing \u201ctriage\u201d tool for COVID-19 was launched this week by Verily Life Sciences, a healthcare technology company owned by Mountain View, Calif.-based Alphabet \u2014 though with a substantially reduced scope than initially suggested by Pr\u2026", 
      "event_genre": [
        "Pharmaceutical"
      ], 
      "event_location": None, 
      "event_organization": [
        "Verily Life Sciences"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T21:05:00Z", 
      "sentiment": 0.49, 
      "source": "Computerworld.com", 
      "ticker": "GOOGL", 
      "title": "What is Verily Life Sciences and how can it help assess COVID-19 cases?", 
      "url": "https://www.computerworld.com/article/3532798/what-is-verily-life-sciences-and-how-can-it-help-assess-covid-19-cases.html"
    }, 
    {
      "author": "Shoshana Wodinsky", 
      "description": "By now, you\u2019ve probably heard about Verily, the strangely named Alphabet subsidiary that\u2019s in charge of the \u201ccoronavirus testing website\u201d endorsed by Donald Trump. Now that the company has launched the first round of its proposed coronavirus program in the Ba\u2026", 
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
      "published": "2020-03-17T22:28:00Z", 
      "sentiment": 0.08, 
      "source": "Gizmodo.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet Still Needs to Answer a Big Question About Its Covid-19 Site", 
      "url": "https://gizmodo.com/alphabet-still-needs-to-answer-a-big-question-about-its-1842359741"
    }, 
    {
      "author": "Michael Kramer, Contributor, Michael Kramer, Contributor https://www.forbes.com/sites/kramermichael/", 
      "description": "The sharp decline in the stock market could hurt Alphabet's first quarter results.", 
      "event_genre": [
        "Analyst Estimates", 
        "Earnings"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-18T01:51:24Z", 
      "sentiment": -0.73, 
      "source": "Forbes.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet\u2019s First Quarter Results May Disappoint On Steep Stock Market Sell-Off", 
      "url": "https://www.forbes.com/sites/kramermichael/2020/03/17/alphabets-first-quarter-results-may-disappoint-on-steep-stock-market-sell-off/"
    }, 
    {
      "author": "Noah Manskar", 
      "description": "The Google sister company offering coronavirus tests ran out of appointments within a day of launching a website to help patients schedule them. Verily, a health-focused subsidiary of Google\u2019s parent company, Alphabet, opened the site Monday to screen people \u2026", 
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
      "published": "2020-03-17T12:21:46Z", 
      "sentiment": 0.4, 
      "source": "Nypost.com", 
      "ticker": "GOOGL", 
      "title": "Google\u2019s Project Baseline coronavirus tests are fully booked", 
      "url": "https://nypost.com/2020/03/17/googles-project-baseline-coronavirus-tests-are-fully-booked/"
    }, 
    {
      "author": "Carmen Reinicke", 
      "description": "Four technology giants - Microsoft,Apple,Google-parent Alphabet, and Amazon- have shed more than $US1 trillion in market value since all-time highs in February as markets have been roiled by coronavirus, CNBC reported. More \u00bb", 
      "event_genre": [
        "Politics", 
        "Analyst Estimates"
      ], 
      "event_location": None, 
      "event_organization": [
        "Apple", 
        "Microsoft", 
        "Cnbc"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T13:24:03Z", 
      "sentiment": 0.2, 
      "source": "Businessinsider.com.au", 
      "ticker": "GOOGL", 
      "title": "4 tech giants President Trump calls 'MAGA' stocks have lost $1 trillion in the coronavirus-induced market rout", 
      "url": "https://www.businessinsider.com.au/tech-giants-maga-stocks-lost-trillion-value-coronavirus-market-selloff-2020-3"
    }, 
    {
      "author": "CNBC US Source", 
      "description": "Cisco CEO Chuck Robbins organized a call with nearly 60 Silicon Valley CEOs and executives, including Facebook, Apple, Alphabet and others, to explore ways to use their money and resources to help fight coronavirus. He joins CNBC's \"Squawk on the Street\" to d\u2026", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": [
        "Facebook", 
        "Cisco", 
        "Cnbc Squawk"
      ], 
      "event_person": [
        "Chuck Robbins"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T13:34:12Z", 
      "sentiment": 0.42, 
      "source": "CNBC", 
      "ticker": "GOOGL", 
      "title": "Cisco CEO Chuck Robbins on how the private sector can help during the coronavirus crisis", 
      "url": "https://www.cnbc.com/video/2020/03/17/cisco-ceo-chuck-robbins-on-how-the-private-sector-can-help-during-the-coronavirus-crisis.html"
    }, 
    {
      "author": "Daisuke Wakabayashi and Natasha Singer", 
      "description": "Within a few hours of launching, Alphabet Inc.'s Verily said it could not schedule any more appointments at the time because it had reached capacity.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T14:20:43Z", 
      "sentiment": 0.1, 
      "source": "Bizjournals.com", 
      "ticker": "GOOGL", 
      "title": "Coronavirus testing website goes live and quickly hits capacity", 
      "url": "https://www.bizjournals.com/bizjournals/news/2020/03/17/coronavirus-testing-website-goes-live-and-quickly.html?ana=RSS&s=article_search&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+bizj_national+%28Bizjournals+National+Feed%29"
    }, 
    {
      "author": "", 
      "description": "DUBLIN--(BUSINESS WIRE)--The \"The US Library Expenditure Market: Size, Trends and Forecasts (2020-2024)\" report has been added to ResearchAndMarkets.com's offering. This report provides an in-depth analysis of the US library expenditure market by value, by co\u2026", 
      "event_genre": [
        "Analyst Estimates"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T16:26:20Z", 
      "sentiment": 0.34, 
      "source": "Businesswire.com", 
      "ticker": "GOOGL", 
      "title": "Insights into the US Library Expenditure Market (2020 to 2024) - Featuring Clarivate Analytics, RELX Group (Elsevier), Alphabet (Google) and Cambridge Information Group (ProQuest) - ResearchAndMarkets.com", 
      "url": "https://www.businesswire.com/news/home/20200317005616/en/Insights-Library-Expenditure-Market-2020-2024--"
    }, 
    {
      "author": "Keris Lahiff", 
      "description": "The megacap tech club is on the rebound, but Piper Sandler's Craig Johnson says a bigger pullback is the time to jump in.", 
      "event_genre": [
        "Analyst Estimates", 
        "Equities"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": [
        "Craig Johnson", 
        "Piper Sandler"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T16:34:27Z", 
      "sentiment": 0.09, 
      "source": "CNBC", 
      "ticker": "GOOGL", 
      "title": "This is when to buy Microsoft, Apple, Amazon and Alphabet stock: Piper Sandler technical analyst", 
      "url": "https://www.cnbc.com/2020/03/17/microsoft-apple-amazon-and-alphabet-stock-are-buys-at-these-levels.html"
    }, 
    {
      "author": "Jason Aycock", 
      "description": "<ul>   <li>Google Fiber (<a href='https://seekingalpha.com/symbol/GOOG' title='Alphabet Inc.'>GOOG</a> <font color=\"green\">+2%</font>, <a href='https://seekingalpha.com/symbol/GOOGL' title='Alphabet Inc.'>GOOGL</a> <font color=\"green\">+2.8%</font>) has <a hre\u2026", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T16:39:56Z", 
      "sentiment": 0.0, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Google Fiber shuts retail, sales calls", 
      "url": "https://seekingalpha.com/news/3552595-google-fiber-shuts-retail-sales-calls"
    }, 
    {
      "author": "Reuters", 
      "description": "SAN FRANCISCO \u2013 Alphabet Inc\u2019s YouTube, Facebook and Twitter warned on Monday that more videos and other content could be erroneously removed for policy violations, as the companies empty offices and rely on automated takedown software during the coronavirus \u2026", 
      "event_genre": [
        "Media"
      ], 
      "event_location": [
        "Francisco"
      ], 
      "event_organization": [
        "Facebook", 
        "Twitter"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T17:11:00Z", 
      "sentiment": -0.87, 
      "source": "Nypost.com", 
      "ticker": "GOOGL", 
      "title": "Social media giants warn of AI moderation errors as coronavirus empties offices", 
      "url": "https://nypost.com/2020/03/17/social-media-giants-warn-of-ai-moderation-errors-as-coronavirus-empties-offices/"
    }, 
    {
      "author": "Neer Varshney", 
      "description": "The so-called \"Make American Great Again\" stocks touted by President Donald Trump last month lost more than $1 trillion in market capitalization on Monday.What Happened Microsoft Corporation, Apple Inc., Google parent company Alphabet Inc. (NASDAQ: GOOGL) (NA\u2026", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google", 
        "Nasdaq", 
        "Apple Inc", 
        "Alphabet Inc", 
        "Microsoft Corporation"
      ], 
      "event_person": [
        "Donald Trump"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T05:42:22Z", 
      "sentiment": 0.32, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Trump's MAGA Stocks Lose $1T Market Value In A Single Day", 
      "url": "https://finance.yahoo.com/news/trumps-maga-stocks-lose-1t-054222221.html"
    }, 
    {
      "author": "Reuters", 
      "description": "In the Dec. 20 letter, O'Toole also wrote that Alphabet also would disclose the growth of Google Cloud revenues \"although we do not believe it is currently a required disclosure.\"", 
      "event_genre": [
        "Investment"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T06:05:00Z", 
      "sentiment": 0.48, 
      "source": "Business-standard.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet shared YouTube revenue after US SEC demanded 'qualitative' data", 
      "url": "https://www.business-standard.com/article/international/alphabet-shared-youtube-revenue-after-us-sec-demanded-qualitative-data-120031601704_1.html"
    }, 
    {
      "author": "Louis Stevens", 
      "description": "This article explains why Alphabet should aggressively execute a leveraged recapitalization.\n        Just as Apple has successfully done, Alphabet should achieve a cash neutral position, especially as interest rates continue to plummet.\n        Alphabet's cur\u2026", 
      "event_genre": [
        "Investment", 
        "Equities"
      ], 
      "event_location": None, 
      "event_organization": [
        "Apple"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T23:14:56Z", 
      "sentiment": 0.15, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet's Cash Hoard Is Destroying Shareholder Value", 
      "url": "https://seekingalpha.com/article/4332326-alphabets-cash-hoard-is-destroying-shareholder-value"
    }, 
    {
      "author": "", 
      "description": "YouTube could see a jump in videos erroneously taken down for content policy violations as the company relies more on automated software during the coronavirus pandemic, Alphabet Inc's Google warned on Monday. Google said in a blog post that to reduce the nee\u2026", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-17T01:00:38Z", 
      "sentiment": -0.82, 
      "source": "Japantoday.com", 
      "ticker": "GOOGL", 
      "title": "Vanishing YouTube videos: Google expects AI errors as coronavirus empties offices", 
      "url": "https://japantoday.com/category/tech/update-1-vanishing-youtube-videos-google-expects-ai-errors-as-coronavirus-empties-offices"
    }, 
    {
      "author": "Darrell Etherington", 
      "description": "Alphabet -owned health technology company Verily has launched the COVID-19 screening site that was first misrepresented by President Trump as a broadly focused coronavirus web-based screening and testing utility developed by Google. After a flurry of blog pos\u2026", 
      "event_genre": [
        "Product Release", 
        "Pharmaceutical"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T12:33:53Z", 
      "sentiment": 0.3, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet's Verily launches its California COVID-19 test screening site in a limited pilot", 
      "url": "https://finance.yahoo.com/news/alphabets-verily-launches-california-covid-123353150.html"
    }, 
    {
      "author": "Darrell Etherington", 
      "description": "Alphabet -owned health technology company Verily has launched the COVID-19 screening site that was first misrepresented by President Trump as a broadly focused coronavirus web-based screening and testing utility developed by Google. After a flurry of blog pos\u2026", 
      "event_genre": [
        "Product Release", 
        "Pharmaceutical"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T12:33:53Z", 
      "sentiment": 0.3, 
      "source": "TechCrunch", 
      "ticker": "GOOGL", 
      "title": "Alphabet\u2019s Verily launches its California COVID-19 test screening site in a limited pilot", 
      "url": "http://techcrunch.com/2020/03/16/alphabets-verily-launches-its-california-covid-19-test-screening-site-in-a-limited-pilot/"
    }, 
    {
      "author": "J. Jennings Moss", 
      "description": "Verily, Alphabet Inc.'s life science research offshoot, late Sunday launched a screening website to help users determine if they need to get a test for COVID-19 and to provide information about where they can go to get tested for the coronavirus. For now, the\u2026", 
      "event_genre": [
        "Pharmaceutical"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T14:23:22Z", 
      "sentiment": 0.49, 
      "source": "Bizjournals.com", 
      "ticker": "GOOGL", 
      "title": "Verily launches coronavirus screening website as Alphabet CEO pledges cooperation", 
      "url": "https://www.bizjournals.com/sanjose/news/2020/03/16/verily-launches-coronavirus-screening-website-as.html?ana=RSS&s=article_search&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+industry_7+%28Industry+Technology%29"
    }, 
    {
      "author": "Todd Haselton", 
      "description": "Alphabet's website, built by Verily, says it's no longer taking reservations for coronavirus COVID-19 screenings in two California counties. It launched on Sunday evening.", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": [
        "California"
      ], 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T15:36:00Z", 
      "sentiment": -0.18, 
      "source": "CNBC", 
      "ticker": "GOOGL", 
      "title": "The Alphabet coronavirus screening website that Trump talked about is not taking appointments now", 
      "url": "https://www.cnbc.com/2020/03/16/alphabet-verily-coronavirus-screening-website-is-overloaded.html"
    }, 
    {
      "author": "Mark Bergen", 
      "description": "(Bloomberg) -- A website to screen people for coronavirus tests run by Google parent Alphabet Inc. reached capacity and stopped accepting appointments on its first full day of operation.Verily, a health-care unit of Alphabet, opened the website Sunday evening\u2026", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google", 
        "Bloomberg"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T16:33:02Z", 
      "sentiment": 0.27, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Google-Backed Coronavirus Testing Website Books Up on First Day", 
      "url": "https://finance.yahoo.com/news/google-backed-coronavirus-testing-website-163302954.html"
    }, 
    {
      "author": "Anthony Ha", 
      "description": "Alphabet  launches a site for COVID-19 test screening, the stock market continues to fall and Microsoft Teams goes down.  Alphabet-owned health technology company Verily  has launched the COVID-19 screening site that was first described by President Trump as \u2026", 
      "event_genre": [
        "Politics", 
        "Equities"
      ], 
      "event_location": None, 
      "event_organization": [
        "Microsoft"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T16:35:00Z", 
      "sentiment": 0.13, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Daily Crunch: Alphabet's Verily launches COVID-19 screening site - Yahoo Philippines News", 
      "url": "https://ph.news.yahoo.com/daily-crunch-alphabets-verily-launches-163517267.html"
    }, 
    {
      "author": "Anthony Ha", 
      "description": "Alphabet launches a site for COVID-19 test screening, the stock market continues to fall and Microsoft Teams goes down. Here\u2019s your Daily Crunch for March 16, 2020. 1. Alphabet\u2019s Verily launches its California COVID-19 test screening site in a limited pilot A\u2026", 
      "event_genre": [
        "Product Release"
      ], 
      "event_location": [
        "California"
      ], 
      "event_organization": [
        "Microsoft"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T16:35:17Z", 
      "sentiment": -0.23, 
      "source": "TechCrunch", 
      "ticker": "GOOGL", 
      "title": "Daily Crunch: Alphabet\u2019s Verily launches COVID-19 screening site", 
      "url": "http://techcrunch.com/2020/03/16/daily-crunch-alphabets-verily-launches-covid-19-screening-site/"
    }, 
    {
      "author": "Anthony Ha", 
      "description": "Alphabet launches a site for COVID-19 test screening, the stock market continues to fall and Microsoft Teams goes down. Alphabet-owned health technology company Verily has launched the COVID-19 screening site that was first described by President Trump as a b\u2026", 
      "event_genre": [
        "Politics"
      ], 
      "event_location": None, 
      "event_organization": [
        "Microsoft"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T16:35:17Z", 
      "sentiment": 0.13, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Daily Crunch: Alphabet's Verily launches COVID-19 screening site", 
      "url": "https://finance.yahoo.com/news/daily-crunch-alphabets-verily-launches-163517267.html"
    }, 
    {
      "author": "CNA", 
      "description": "Alphabet Inc  began disclosing revenue for its YouTube video service this year after U.S. securities regulators asked the Google parent to give more \"quantitative and qualitative\" data on the business, according to filings released Monday.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Youtube"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T16:45:39Z", 
      "sentiment": 0.56, 
      "source": "Channelnewsasia.com", 
      "ticker": "GOOGL", 
      "title": "Google parent Alphabet shared YouTube revenue after US SEC request", 
      "url": "https://www.channelnewsasia.com/news/business/google-parent-alphabet-shared-youtube-revenue-after-us-sec-request-12544292"
    }, 
    {
      "author": "Paresh Dave", 
      "description": "Alphabet Inc began disclosing revenue for its YouTube video service this year after U.S. securities regulators asked the Google parent to give more \"quantitative and qualitative\" data on the business, according to filings released Monday.", 
      "event_genre": [
        "Media"
      ], 
      "event_location": None, 
      "event_organization": [
        "Youtube"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T17:00:38Z", 
      "sentiment": 0.56, 
      "source": "Reuters", 
      "ticker": "GOOGL", 
      "title": "Google parent Alphabet shared YouTube revenue after U.S. SEC request", 
      "url": "https://in.reuters.com/article/alphabet-sec-idINKBN2132YY"
    }, 
    {
      "author": "Reuters", 
      "description": "Alphabet's chief accounting officer said the company would also disclose the growth of Google Cloud revenues \"although we do not believe it is currently a required disclosure.\"", 
      "event_genre": [
        "Earnings", 
        "Corporate Leadership"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T17:29:19Z", 
      "sentiment": 0.66, 
      "source": "CNBC", 
      "ticker": "GOOGL", 
      "title": "Google parent Alphabet began sharing YouTube revenue after SEC request", 
      "url": "https://www.cnbc.com/2020/03/16/google-parent-alphabet-began-sharing-youtube-revenue-after-sec-request.html"
    }, 
    {
      "author": "Richard Nieva", 
      "description": "California Governor Gavin Newsom said he believes the partnership with Google's sister company can be a \"national model\" for coronavirus screening.", 
      "event_genre": [
        "Partnership"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google"
      ], 
      "event_person": [
        "Gavin Newsom"
      ], 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T04:39:00Z", 
      "sentiment": 0.0, 
      "source": "Cnet.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet's Verily launches coronavirus testing website for SF Bay Area - CNET", 
      "url": "https://www.cnet.com/news/alphabets-verily-launches-coronavirus-testing-website-for-sf-bay-area/"
    }, 
    {
      "author": "Stephanie Mlot", 
      "description": "COVID-19 (via Johns Hopkins Medicine) Alphabet Inc.\u2019s research organization Verily launched a website to provide information about coronavirus screening in the San Francisco Bay Area. Starting today, Californians can take an online COVID-19 screener survey, h\u2026", 
      "event_genre": [
        "Product Release", 
        "Pharmaceutical"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-16T11:12:33Z", 
      "sentiment": 0.13, 
      "source": "Geek.com", 
      "ticker": "GOOGL", 
      "title": "Verily Launches COVID-19 Screening Site for San Francisco Residents", 
      "url": "https://www.geek.com/tech/verily-launches-covid-19-screening-site-for-san-francisco-residents-1820258/"
    }, 
    {
      "author": "Gerrit De Vynck", 
      "description": "(Bloomberg) -- Alphabet Inc.\u2019s Google will launch a website on Monday focused on providing up-to-date information about coronavirus education and prevention.The site is a separate project from the testing and triage website being built by Google sister compan\u2026", 
      "event_genre": [
        "Product Release"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google", 
        "Bloomberg"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-15T20:42:37Z", 
      "sentiment": 0.38, 
      "source": "Yahoo.com", 
      "ticker": "GOOGL", 
      "title": "Google CEO Says Nationwide Virus Info Site to Launch Monday", 
      "url": "https://finance.yahoo.com/news/google-ceo-says-nationwide-virus-204237016.html"
    }, 
    {
      "author": "Stone Fox Capital", 
      "description": "Alphabet has dipped $400 on COVID-19 fears.The company has an EV down to only $670 billion due to $115 billion in net cash.A slash in travel ad revenues will cut $1-2 billion in quarterly revenues.The stock only trades at an EV of 12.2x '21 EPS targets. A $1,\u2026", 
      "event_genre": [
        "Earnings"
      ], 
      "event_location": None, 
      "event_organization": None, 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-15T23:21:06Z", 
      "sentiment": -0.49, 
      "source": "Seekingalpha.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet: Sticking With $1,700 Target", 
      "url": "https://seekingalpha.com/article/4332088-alphabet-sticking-1700-target"
    }, 
    {
      "author": "Mike Wheatley", 
      "description": "Google LLC said Friday its sister company Verily Life Sciences LLC is helping the federal government to build a new online tool to help some Americans get tested for the coronavirus. Verily, which is owned by Google\u2019s parent company Alphabet Inc., said the to\u2026", 
      "event_genre": [
        "Politics", 
        "Partnership"
      ], 
      "event_location": None, 
      "event_organization": [
        "Google", 
        "Alphabet Inc", 
        "Sciences"
      ], 
      "event_person": None, 
      "event_sector": [
        "Technology"
      ], 
      "published": "2020-03-15T23:52:49Z", 
      "sentiment": 0.73, 
      "source": "Siliconangle.com", 
      "ticker": "GOOGL", 
      "title": "Alphabet Inc.\u2019s Verily life sciences unit is helping to build a coronavirus testing website", 
      "url": "https://siliconangle.com/2020/03/15/alphabet-inc-s-verily-life-sciences-unit-helping-build-coronavirus-testing-website/"
    }
  ]
}

# class NewsObj(db.Model):
#       __tablename__ = 'news'

#       id = db.Column(db.Integer, primary_key=True)
#       title = db.Column(db.String(248), Noneable=False)
#       author = db.Column(db.String(248), Noneable=False)
#       description = db.Column(db.String(2048), Noneable=False)
#       published = db.Column(db.String(1000), Noneable=False)
#       ticker = db.Column(db.String(100), Noneable=False)
#       url = db.Column(db.String(2048), Noneable=False)

#       def __init__(self, id, title, author, description, published, ticker, url): #Initialise the objects
#        self.id = id
#        self.title = title
#        self.author = author
#        self.description = description
#        self.published = published
#        self.ticker = ticker
#        self.url = url

#       def json(self): 
#         return {"id": self.id, "title": self.title, "author": self.author, "description": self.description, "published": self.published, "ticker": self.ticker,"url": self.url}


@app.route("/")
def get_news_by_tickers():
  # url = ('https://api.unibit.ai/v2/company/news/?'
  #      'tickers=GOOGL&'
  #      'dataType=json&'
  #      'accessKey=RdOZz1C5684sM5OlIF-5BVpcKQ80tMZI')

  # news = requests.get(url) 
  # news_finance = news.json()

  new_data = news_finance
  count = 0
  new_dict = {}
  news_objects = {}
  obj_of_news = {}

  return new_data

  # for data1 in new_data['GOOGL']:
  #   count += 1
  #   new_dict[count] = data1
  #   for i in range (1 , len(new_dict) + 1):
  #       y = NewsObj(i, new_dict[i]['title'], new_dict[i]['author'], new_dict[i]['description'], new_dict[i]['published'], new_dict[i]['ticker'], new_dict[i]['url'])
  #       news_objects[i] = y.json()
  # try:
  #   for i in range (1, len(news_objects) + 1):
  #     #return news_objects
  #     # return(news_objects)
  #     individual_news = news_objects[i]
  #     obj_news = NewsObj(**individual_news)   
  #     db.session.add(obj_news)
  #     db.session.commit()
  # except:
  #   return jsonify({"message": "An error occurred adding news"}), 500
  # return jsonify({"message": "Successfully added"}), 201
  
app.run(port=6002, debug=True)
