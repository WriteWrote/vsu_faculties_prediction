# VSU_gradework_web
website for my VSU graduation work: neuro predicting test

# Система прогнозирования для абитуриента наиболее ему подходящего факультета вуза на основе его цифровых следов в социальной сети

# Greetings!

## What is it about?
This is a project of fourth-grade student of Voronezh State University. It was dedicated to attempt to solve the problem of self-awareness in the aspect of most suiting professional skills and willingness to learn some particular knoledge from the university.

This is the quick but reliable test for young and bold, who want to learn something new about themselves or confirm their own decisions, so they can choose the most suitable for their personal traits faculty of the VSU.

## How does it works?
The key is a modern approach to the old problem. This project is trying to prove the theory that people can leave a tonn of information about their personalities unconsciously, while simply surfing the internet. So it must be possible to analyse the so be said **digital footprints**, which person lefts behind, for example, liking some posts in the Instagram or Facebook or VK (etc, etc, etc...

In this project specially constructed and trained AI-model takes **digital footprints** of the person performing the test and creates a prediction to which faculty should they try to apply. Model can spot some nontrivial patterns, which may result in surprising predictions!

## How you can test yourself?
Simply go to your personal VK-page and copy from the clipboard path to your profile. Paste the link into the box below ant click the 'Test!' button. Also make sure that your personal page is open for everyone (or make it open for a brief period of time for testing), otherwise this test will not work on you.

## Basic idea of using AI
The idea is simple: this program takes your VK-profile and makes a request to VK-servers to collect the list of your open and visible groups. Because VK provides an open API for such requests, program cannot just go and collect everything it wants, so it takes only open and available information. Also it is totally anonimous, because there is absolutely no need for your name/other stuff for the analys.

After receiving the VK-server responce program scrubbes the unique ids of the public groups from your profile and makes a long vector of them. Theт it fits this vector to the model, and model returns a prediction: 21 numbers in percents, which describe mostly the belonging the sample to the specific class.

The final prediction is made by finding the max value in the answer of the AI-model, this value is coming out as the result. However all persentages for all classes also are provided at the result-page, so you can see all the varietes. Sometimes the difference will be so small, that you might actually have two or three possible variants, that are suited for you.

## ToDo:
- consider using NLP model
- consider using tokenized namings of groups for calculating vector similarity
- deploy it to open&free server
- finish the official cover note for the app

## Tasks already done:
- created basic structure of web (HTML+CSS+Jango)
- created api (Py+Flask)
- gathered raw data for training model (parsed VK-profiles)
- clean data and form basic datasets (2 classes: tech and art; and 21 classes: all VSU faculties)
- test mocking model on the data (keras, Sequential)
- connect model to the web
- prepare code to parse single person digital footprints to the form for fitting into the model for prediction
- assemble all together
- finish polishing the website
- try out 2 datasets: for 2 classes and 21
- reconsider AI-model
