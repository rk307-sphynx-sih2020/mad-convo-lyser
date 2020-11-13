# mad-convo-lyser
Chat analyser mobile application using KivyMD

final_mad.py -> Application code
helpers.py -> Text fields using stringbuilder to receive input
mail.py -> Code to send an email for the report portal and implicit grooming detection

In order to run this application the following files will be required-
1. Input conversation text file
2. LIWC dictionary with additional words if required
3. Email body must be stored in a text file (message.txt and message1.txt)
4. The recepients of the email must be stored in a text file (contacts.txt)

A support vector machine (SVM) has been used as a classifier in this application. 
So an SVM must be trained and the pkl file should be loaded into the code.
