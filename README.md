# NoIT project

This repository contains a machine learning testing application. 
It allows its user to upload a classification dataset in .csv format and 
train different algorithms to predict a chosen target variable. After training
the user receives a report where he can see metric values of each of the algorithms chosen.

It is a part of my masters work in Belarusian State University.

### Description

------------

 - Alg folder contains implementation of the metric algorithms, based on the measure of precedence, testing process and report making process.
 - EDA folder contains EDA operations including duplicates and null values handling, data encoding etc.
 - Media folder contains application icon.
 - UI folder contains widgets and other graphics objects used to build the application.

### Running the code

------------

 - You must have Python 3.9+ installed
 - Clone the repository
 - (Optional) Set up a virtual environment
 - Install poetry with: *pip install poetry*
 - Install all the dependencies with: *poetry install*
 - Run the code with: *python -OO main.py*