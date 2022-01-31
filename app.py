import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



    user_list = df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")


    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("BOBBY'S CHAT ANALYSER")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages ")
            st.title(num_messages)
        with col2:
            st.header("Total Words ")
            st.title(words)
        with col3:
            st.header("Total Media Messages ")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links shared ")
            st.title(num_links)

      #  if selected_user == "Overall":
           # st.title("Most busy user")
          #  x, new_df = helper.most_busy_user(df)
         #   fig, ax = plt.subplots()
        #    col1, col2 = st.columns(2)
       # with col1:
          #  ax.bar(x.index, x.values, color = 'red')
         #   plt.xticks(rotation = "vertical")
        #    st.pyplot(fig)
      #  with col2:
           # st.dataframe(new_df)

        timeline = helper.monthly_timeline(selected_user, df)
        st.title("Monthly timeline")
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color = "green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("weekly Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.weekly_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy months")
            busy_month = helper.monthly_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()

        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)









        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


    st.title("WordCloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)


    most_common_df = helper.most_comman_word(selected_user, df)

    fig, ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)


    emoji_df  = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")


    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(10), labels = emoji_df[0].head(10), autopct = "%0.2f")
        st.pyplot(fig)












