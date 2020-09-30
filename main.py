import json
import requests
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from wordcloud import WordCloud
import matplotlib.pyplot as plt


def part1():
    st.header("Part A - The Stories API")
    st.write("This app uses the Top Stories API to display the most common used in the top current articles based on a specific top selected by the user. The Data is displayed as line chart and wordcloud.")

    st.subheader("I - Topic Selection")


    option = st.text_input("Please enter your Name")
    option_selection = st.selectbox(
        "Select a Top you Like",
        ["","arts", "automobiles","books","business","fashion","food","health","home","insider","magazine","movies","nyregion","obituaries","opinion","politics","realestate","science","sports","sundayreview","technology","theater","t-magazine","travel","upshot","us","world"]
    )

    if option and option_selection:
        st.write("Hello " + option + " you selected " + option_selection + "!")
        api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
        api_key = api_key_dict["my_key"]

        url = "https://api.nytimes.com/svc/topstories/v2/" + option_selection + ".json?api-key=" + api_key

        response = requests.get(url).json()
        main_functions.save_to_file(response, "JSON_Files/response.json")

        results = main_functions.read_from_file("JSON_Files/response.json")
        str1 = ""

        for i in results["results"]:
            str1 = str1 + i["abstract"]

        words = word_tokenize(str1)

        words_on_punc = []

        for w in words:
            if w.isalpha():
                words_on_punc.append(w.lower())

        stopwordsA = stopwords.words("english")

        clean_words = []

        for w in words_on_punc:
            if w not in stopwordsA:
                clean_words.append(w)

        fdish = FreqDist(clean_words)

        st.subheader("II - Frequency Distribution")
        if st.checkbox("Click here to generate frequency distribution"):
            most_common = pd.DataFrame(fdish.most_common(10))
            df = pd.DataFrame({"words": most_common[0], "count": most_common[1]})

            fig = px.line(df, x="words", y="count", title="")
            st.plotly_chart(fig)

        st.subheader("III - Wordcloud")
        if st.checkbox("Click here to generate wordcloud"):
            wordcloud = WordCloud().generate(str1)
            plt.figure(figsize=(12, 12))
            plt.imshow(wordcloud)
            plt.axis('off')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

def part2():
    st.header("Part B - Most Polular Articles")
    st.write("Select if you want to see the most shared, emailed or viewed articles.")

    popular_selection = st.selectbox(
        "Select your preferred set of articles ",
        ["","emailed", "shared", "viewed"]
    )

    popular_time_selection = st.selectbox(
        "Select the period of time (last days)",
        ["","1", "7", "30"]
    )

    if popular_selection and popular_time_selection:
        api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
        api_key = api_key_dict["my_key"]

        urlB = "https://api.nytimes.com/svc/mostpopular/v2/"+ popular_selection + "/" + popular_time_selection + ".json?api-key=" + api_key


        responseB = requests.get(urlB).json()
        main_functions.save_to_file(responseB, "JSON_Files/Popular_response.json")

        resultsB = main_functions.read_from_file("JSON_Files/Popular_response.json")

        str2 = ""

        for i in resultsB["results"]:
            str2 = str2 + i["abstract"]

        wordsB = word_tokenize(str2)

        wordsB_on_punc = []

        for w in wordsB:
            if w.isalpha():
                wordsB_on_punc.append(w.lower())

        stopwordsB = stopwords.words("english")

        clean_wordsB = []

        for w in wordsB_on_punc:
            if w not in stopwordsB:
                clean_wordsB.append(w)

        fdish2 = FreqDist(clean_wordsB)


        wordcloudB = WordCloud().generate(str2)
        plt.figure(figsize=(12, 12))
        plt.imshow(wordcloudB)
        plt.axis('off')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

if __name__ == '__main__':
    st.title("COP 4813 - Web Application Programming")

    st.title("Project 1")

    project_option = st.sidebar.selectbox("Choose a project", ("Part 1", "Part 2"))
    if project_option == "Part 1":
        part1()
    elif project_option == "Part 2":
        part2()

