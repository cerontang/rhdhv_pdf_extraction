import re
import PyPDF2
import numpy as np
import pandas as pd
import os

#PURPOSE OF SCRIPT: CHECK EXTRACTION VALIDITY AND ACCURACY BY RANDOMISING THE SPELLING OF KEY EXTRACTION VALUES

reportLocation = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\06-Grouting works\02 - Verification\01 Copy of all verification BHs\Pier 3'
reportList = os.listdir(reportLocation)

#print(len(reportList))

for i in reportList:
    SPTornot = 1
    x = 0
    reportPath = reportLocation+'\\'+i
    text = ""
    with open(reportPath, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        totalPages = reader.numPages
        for pageNumber in range(totalPages):
            page = reader.getPage(pageNumber)
            text = text + page.extractText()
        textList = text.split()
        for j in textList:
            if j == 'SPT1':
                break
            else:
                x = x + 1
            if x == len(textList)-1:
                SPTornot = 0
                break

    random_matchedWord_list_From = []
    exact_matchedWord_list_From = []

    random_matchedWord_list_Grout = []
    exact_matchedWord_list_Grout = []

    if SPTornot == 1:
        ###TESTING "From" SPELLING#####################################################################################
        for word in textList:
            testWord = re.search(r"^[F][a-hj-z][a-z][m]", word)
            if testWord != None:
                matchedWord = testWord.group(0)
                random_matchedWord_list_From.append(matchedWord)
        for word in textList:
            exacttestWord = "From"
            if exacttestWord == word:
                exact_matchedWord_list_From.append(word)
        ###TESTING "Grout" SPELLING####################################################################################
        for word in textList:
            testWord = re.search(r"^[g][a-z][a-z][a-z][t]", word)
            if testWord != None:
                matchedWord = testWord.group(0)
                random_matchedWord_list_Grout.append(matchedWord)
        for word in textList:
            exacttestWord = "grout"
            if exacttestWord == word:
                exact_matchedWord_list_Grout.append(word)
        ###############################################################################################################
        testResult = "OK"
        if len(random_matchedWord_list_From) != len(exact_matchedWord_list_From) or len(random_matchedWord_list_Grout) != len(exact_matchedWord_list_Grout):
            testResult = "NOT OK, PLEASE CHECK"

        print(i, " ", len(random_matchedWord_list_From), " ", len(exact_matchedWord_list_From), " ", len(random_matchedWord_list_Grout), " ", len(exact_matchedWord_list_Grout), testResult)




    # print(i, " ", SPTornot)
    # print(textList)