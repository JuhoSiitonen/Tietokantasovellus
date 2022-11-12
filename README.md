# Tietokantasovellus
Database application in the spirit of Wolt. The application is named ZWOLT.

User can log in to the application using a username and password.
User can order food from restaurant and receive invoice for the order.
Invoices/receipts are kept in database and user can access them. 
User can give feedback to restaurant in form of stars and a textual review.
These reviews can be accessed by other users also. 
Only one review for a restaurant by user. The reviews can be modified afterwards.
Upon ordering user can leave a textual preference for the delivery or food. 

This is made by having at least 5 postgreSQL databases. Users, restaurants, dishes, receipts and reviews. 
Database information deletion is done by a visibility column which has a boolean value. 


Admin user can delete restaurants, dishes, users and modify all but user data and receipts. 


*** Functionality yet uncertain: Time estimate from restaurant address to customer address. Google maps API connection required. Or Maify or other API for distance matrix.

INFO for VÄLIPALAUTUS 2:


