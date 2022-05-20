# [Expense Tracker](https://gastocontrol.herokuapp.com)

A solution for controlling all your expenses no matter the currency.

# Table of Contents  
1. [Introduction](#Introduction)
2. [How to use](#How to use)
3. [Technical stack](#Technical-stack)
4. [ToDos](#ToDos)

# Introduction
My family and I are moving to a new country in a different continent, so we needed a place to store all our expenses. The problem was that we have to spend money in different currencies and didn't wnat to spend a lot of time looking for the current value of each currency, so I decided to build a solution that would fit our needs and make my parents life easier. I built this web app in spanish since we came from Argentina and my parents don't speak any other language.

# How to use
The app is really easy to use, you basically create your user and then start to add your purchases. After creating your user, you will receive an email with your user and password since the change/forgot password functionality has not been added yet.

You will also get a monthly email containing a PDF with the resume of all your spendings of that month. If you haven't add anything, you will not receive an email. If you wish, you can also download a partial resume of all the purchases that you have added so far.

You can add a title and description, then you can choose the original currency of the purchase and the one you want to be converted to. 

The app works with Euro (EUR), Bitcoin (BTC), Swiss Franc (CHF), British Pound Sterling (GBP) and Argentine Peso (ARS). Once you save it, you will see your purchase with the converted value to the chosen currency. You can add, edit or delete any item added.

# Technical stack

For building this web app, I used the following technologies:

### Python and Django
Since my whole carreer I've been using Python, I decided to use it for developing this idea. I ended up using Django since it was a more suitable solution than Flask and FastAPI for this idea since it has a lot of out of box features and reduces time to build the website.

### Pre-commit
I used pre-commit, Black and Flake8 in order to improve my code's quality.

### Heroku
I chose Heroku because I already had experience using it and this was not going to be a really big idea that would need to scale a lot.

### PostgreSQL
Since Heroku has a PostgreSQL addon and I have experience using this database, I decided to take advantage of its simplicity. The website is not so big so its not going to need to scale a lot and the structure for the table is really simple.
Another reason was that relational databases are easier to implement in Django than NoSQL ones.

### SendGrid
Heroku has a SendGrid addon and they have a really good documentation, so I picked up this solution for the emailing.

### exchangerate.host
I decided to use [exchangerate.host](https://exchangerate.host) for the currency conversion. It is a free to use API, and is really easy to use and well documented.

# ToDos
- Add change/forgot my password feature
- Add more languages
- Write integration tests
- Improve UX
- Add dark mode