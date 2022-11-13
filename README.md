# ZWOLT
Database application in the spirit of Wolt. The application is named ZWOLT.

User can log in to the application using a username and password.
User can order food from restaurant and receive invoice/receipt for the order.
Invoices/receipts are kept in database and user can access them. 
User can give feedback to restaurant in form of stars and a textual review.
These reviews can be seen by other users also. The reviews can be modified afterwards.
Upon ordering user can leave a textual preference for the delivery or food. 

This is made by having at least 6 postgreSQL databases. Users, restaurants, dishes, receipts, receiptdishes and reviews. Receiptdishes table made to keep data in databases more atomic. 
Database information deletion is done by a visibility column which has a boolean value. 

Admin user can delete restaurants, dishes, users and modify all but user data and receipts. 


*** Functionality yet uncertain: Time estimate from restaurant address to customer address. Google maps API connection required. Or Maify or other API for distance matrix.

INFO for VÄLIPALAUTUS 2:

You can test the app on page https://zwolt.fly.dev 
You can create a user by clicking "Rekisteröidy" and then entering your chosen credentials.
You can order food by clicking "Ravintolat lähelläsi", then choosing a restaurant and then choosing preferred dishes. This is followed by a confirmation screen where you can confirm your order by clicking "Vahvista tilaus". Then you can return to the frontpage or leave a review of the restaurant. 
From the front page you can view your orders and reviews. You can modify your review by selecting it. You can also view best restaurants by review and also you can logout from the frontpage. 

Missing features and issues:

-Admin mode for inserting restaurants and dishes and making a user an admin. Admin will also be able to delete users, restaurants, dishes and reviews.  

-At the moment no check for user rights except session user_id

-Making a review through the frontpage

-Restaurant and dish descriptions and Find functions for them

-CSRF vulnerability not yet patched

-Too many functions and pages, idea is to make pages more dynamic and use same functions more if possible, also improve use of SQL not to find just single bits of data by a function

-No check for user input (length mainly as there is yet no input which requires integers)

-PRG model not really applied, many POST methods in a row..

-Only a preliminary CSS style added, in future CSS containers and different color scheme and many links changed to buttons.

-Many dishes can be ordered, but only one of each, needs to be changed

-Prices are only integer type at the moment

-Distance matrix from Google maps or mapify or else if enough time to implement

-Deleting users own reviews, not yet implemented

-Using stars to order reviews not yet implemented

-HTML used in a very very basic way

-Separation of concerns in modules restaurants and users to make them more understandable

-Link to frontpage or back one page from Confirmation page (issue with post method)

