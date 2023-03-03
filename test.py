import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
def heatmap(a):
    final_data=[]
    for i in a:
        data = []
        for j in a:
            data.append(round(j/i,2))
        final_data.append(data)
    return final_data

st.title('Visualisation pour le recrutement')


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(io=uploaded_file)
    df = df.fillna(0)

    with st.container():
        st.header("Nuage de point")
        st.sidebar.title("Variable pour le nuage de point")
        choice_x = st.sidebar.selectbox("Axe des X",df.select_dtypes(["float","int"]).columns)
        choice_y = st.sidebar.selectbox("Axe des Y",df.select_dtypes(["float","int"]).columns)
        aver_x = df[choice_x].mean()
        aver_y = df[choice_y].mean()
        plot = px.scatter(data_frame = df, x = choice_x, y = choice_y, color = 'Market value' ,text = "Player", hover_name = "Player")
        plot.update_traces(marker_size=10)
        plot.add_vline(x=aver_x, line_width=1, line_dash="dash")
        plot.add_hline(y=aver_y,line_width=1, line_dash="dash")
        st.plotly_chart(plot)



        st.header("Bar chart")
        st.sidebar.title("Variable pour le chart bar")
        choice_chart = st.sidebar.multiselect("Choose variables",df.select_dtypes(["float","int"]).columns)
        test = []
        if len(choice_chart) >0:
            for i in choice_chart:
                test.append(go.Bar(name=i, x=df["Player"], y=df[i]))

            fig = go.Figure(data= test
            )
            # Change the bar mode
            fig.update_layout(barmode='group')
            st.plotly_chart(fig)

        st.header("Heatmap")
        st.caption('La couleur de chaque case indique le niveau de performance du joueur en x par rapport au joueur en y. Si les statistiques du joueur en x sont supérieur à celle du joueur en y, la case sera colorée en bleu foncé. Inversément Si le joueur en y a de meilleur statistique que le joueur en x, la case sera colorée en bleu clair. La valeure indiquée est un simple ratio entre la statistique du joueur x et celle du joueur y')
        st.sidebar.title("Cararctéristique de comparaison pour HeatMap")
        choice_heatmap = st.sidebar.selectbox("Choisir une variable",df.select_dtypes(["float","int"]).columns)
        data = heatmap(df[choice_heatmap] )
        fig2 = px.imshow(data, x =df["Player"], y =df["Player"], text_auto = True)
        st.plotly_chart(fig2)

        st.sidebar.title("Radar")
        radar_file = st.sidebar.file_uploader("Choose a radar file")
        if radar_file is not None:
            st.header("Radar")
            st.image(radar_file)
