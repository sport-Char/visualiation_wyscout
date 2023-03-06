import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
def heatmap(a):
    final_data=[]
    for i in a:
        data = []
        for j in a:
            if i ==0:
                data.append(np.nan)
                continue
            data.append(round(j/i,2))
        final_data.append(data)
    return final_data
def getValue(df,player, caract, name):
    value = []
    max =[]
    df_new = df.select_dtypes(["float","int"])
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_new), columns=df_new.columns)
    df_scaled[name] = df[name]

    player_row_norm = df_scaled.loc[df_scaled[name] == player]
    df=df.loc[df_scaled[name] == player]
    for i in caract:
        max.append(df[i].values[0])
        value.append(player_row_norm[i].values[0])
    return value, max


st.title('Visualisation pour le recrutement')


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(io=uploaded_file)
    df = df.fillna(0)
    name  = df.columns[0]
    first_column = df.iloc[:, 0]
    with st.container():
        st.header("Nuage de point")
        st.sidebar.title("Variable pour le nuage de point")
        choice_x = st.sidebar.selectbox("Axe des X",df.select_dtypes(["float","int"]).columns)
        choice_y = st.sidebar.selectbox("Axe des Y",df.select_dtypes(["float","int"]).columns)
        aver_x = df[choice_x].mean()
        aver_y = df[choice_y].mean()
        plot = px.scatter(data_frame = df, x = choice_x, y = choice_y, color = 'Market value' ,text = first_column, hover_name = first_column)
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
                test.append(go.Bar(name=i, x=first_column, y=df[i]))

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
        fig2 = px.imshow(data, x =first_column, y =first_column, text_auto = True)
        st.plotly_chart(fig2)
        
        st.header("Comparaison")
        st.sidebar.title("Comp")
        choice_player = st.sidebar.multiselect("Choisir joueur",first_column)
        choice_caract = st.sidebar.multiselect("Choisir caractéristique",df.select_dtypes(["float","int"]).columns)
        categories = choice_caract
        if len(choice_player)>=1 and len(choice_caract)>=3:
            fig3 = go.Figure()
            for i in choice_player:
                value, max = getValue(df, i, categories, name)
                fig3.add_trace(go.Scatterpolar(
                    r=value,
                    theta=categories,
                    fill='toself',
                    name=i,
                    hovertext = max
                ))
            fig3.update_layout(
                polar=dict(
                radialaxis=dict(
                visible=True
            ),
            ),
                showlegend=True
            )
            st.plotly_chart(fig3)
        
        
        st.sidebar.title("Radar")
        radar_file = st.sidebar.file_uploader("Choose a radar file")
        if radar_file is not None:
            st.header("Radar")
            st.image(radar_file)
