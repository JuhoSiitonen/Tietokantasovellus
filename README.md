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

Admin user can delete restaurants, dishes, users and reviews and add restaurants, dishes and new admins.


INFO for VÄLIPALAUTUS 3:

You can test the app on page https://zwolt.fly.dev 
You can create a user by clicking "Rekisteröidy" and then entering your chosen credentials.
You can order food by clicking "Ravintolat lähelläsi", then choosing a restaurant and then choosing preferred dishes. This is followed by a confirmation screen where you can confirm your order by clicking "Vahvista tilaus". Then you can return to the frontpage or leave a review of the restaurant. 
From the front page you can view your orders and reviews. You can modify your review by selecting it. You can also view best restaurants by review and also you can logout from the frontpage. Admin tools can be accessed from the frontpage, the app checks admin rights and showcases an extra button for admin tools if admin is logged in. 

Admin user is: Admin 
Password: Admin


Missing features and issues:

-Only elementary html check for user input, except in registering

-Only a preliminary CSS style added

-Many dishes can be ordered, but only one of each, needs to be changed

-Prices are only integer type at the moment, same with stars, affects restaurant review average

-HTML used in a very very basic way

-Separation of concerns in modules routes, restaurants and users to make them more understandable

-Restaurant admin user would be good, at the moment only one kind of admin which controls everything

-Confirmation page usage of hidden inputs

- Adding dishes with same name in same restaurant, some changes to DB needs to be done to fix this, especially problematic with deleting items


