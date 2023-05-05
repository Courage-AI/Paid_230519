import streamlit as st
import pandas as pd
import sys
import pandas as pd
import numpy as np
import matplotlib as plt
import os
import openai

def app():
    df_univ = pd.read_csv('univ.csv')
    df_ques = pd.read_csv('ques.csv')
    univ=df_univ['univ_list'].tolist()

    st.title('Courage AI powered by GPT')
    st.subheader('Select a university')
    openai.api_key=st.text_input('Open AI API key')
    univ = st.selectbox('List of university', univ)


    if univ == '-- select the university--':
        st.write('')
    else:
        year = st.selectbox('Year of exam',[2022])
        ques_num_list = df_ques[df_ques.univ == univ]['ques_num'].tolist()
        ques_num = st.selectbox('Number of essay questions',ques_num_list)
        st.subheader("")
        st.write("Collaborate with your SNS Account (under construction)")
        st.image('sns_icon.png')

    start_style = """
        <style>
            div.stButton > button:first-child {
                width: 100%;
                box-sizing: border-box;
                padding: 1rem;
                font-size: 2.0rem;
            }
        </style>
    """

    start_input = st.checkbox('Start writing essay')
    # ボタンのスタイルを適用
    st.markdown(start_style, unsafe_allow_html=True)

    if start_input:
        df_ques_univ = df_ques[df_ques.univ == univ]
        question = df_ques_univ[df_ques_univ.ques_num == ques_num]['question'].tolist()[0]
        num_words = df_ques_univ[df_ques_univ.ques_num == ques_num]['num_words'].tolist()[0]
        input1 = df_ques_univ[df_ques_univ.ques_num == ques_num]['input1'].tolist()[0]
        input2 = df_ques_univ[df_ques_univ.ques_num == ques_num]['input2'].tolist()[0]
        input3 = df_ques_univ[df_ques_univ.ques_num == ques_num]['input3'].tolist()[0]

        st.subheader('University: ' + univ +', '+ str(year) + ', Question #' + str(ques_num))
        with st.container():
            st.markdown(f"<p style='background-color:#eaf4f4; padding: 10px'>{question}</p>", unsafe_allow_html=True)

        st.subheader('Please input three things about yourself')
        input1_answer = st.text_input("1: " + input1,max_chars=1000)
        input2_answer = st.text_input("2: " + input2,max_chars=1000)
        input3_answer = st.text_input("3: " + input3,max_chars=1000)

        start_style = """
            <style>
                div.stButton > button:first-child {
                    width: 100%;
                    box-sizing: border-box;
                    padding: 1rem;
                    font-size: 2.0rem;
                }
            </style>
        """

        start_essay = st.checkbox('Generate essay')
        # Apply the style of the button
        st.markdown(start_style, unsafe_allow_html=True)

        if start_essay:
            prompt = "Following 3 questions & answers are the information about a student who is going to apply to " + univ + ".\n" + "1: " + input1 + ": " + input1_answer + "\n" + "2: "+ input2 + ": " + input2_answer + "\n" + "3: " + input3 + ": " + input3_answer + "\n" + "Considering the information, please create essay Within " + str(num_words) + " words, to the following question \n" + question
            
            response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,#インプットする文章
                                        temperature=0.5,#0-2の値を取り出力する単語のランダム性を指定。2が完全ランダム
                                        max_tokens=512,#生成する文章の最大単語数
                                        top_p=1,#Temperatureと相対するパラメータ
                                        frequency_penalty=0,#-2から2の値をとり、既に出てきた単語をもう1度使うかどうか指定
                                        presence_penalty=0,#-2から2の値をとり、出てきた回数が多いほどペナルティを大きくする
                                        stop=["###"] )#どんな単語が出てきたら文章を打ち切るかを決める
            
            answer = response["choices"][0]['text']

            st.subheader('Example of essay')
            with st.container():
                st.markdown(f"<p style='background-color:#f4e3e3; padding: 10px'>{answer}</p>", unsafe_allow_html=True)

            button_style = """
                <style>
                    div.stButton > button:first-child {
                        width: 100%;
                        box-sizing: border-box;
                        padding: 1rem;
                        font-size: 2.0rem;
                    }
                </style>
            """

            rewrite = st.button('Rewrite this essay')
            st.markdown(button_style, unsafe_allow_html=True)

            if rewrite:
                answer = "rewrite"

            signup = st.button('Sign-up for next essay')
            st.markdown(button_style, unsafe_allow_html=True)


