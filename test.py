import streamlit as st
import pandas as pd

df1 = pd.DataFrame({
    'Column 1': [1, 2, 3],
    'Column 2': [4, 5, 6]
})

df2 = pd.DataFrame({
    'Column A': ['A', 'B', 'C'],
    'Column B': ['D', 'E', 'F']
})

def style_dataframe(df):
    return df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [
                ('background-color', '#4CAF50'),
                ('color', 'white'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '16px')
            ]
        },
        {
            'selector': 'td, th',
            'props': [
                ('border', '2px solid #4CAF50')
            ]
        }]
    )

def display_dataframe(df):
    styled_df = style_dataframe(df)
    st.write(styled_df.to_html(), unsafe_allow_html=True)

# Display DataFrames
st.header("DataFrame 1")
display_dataframe(df1)

st.header("DataFrame 2")
display_dataframe(df2)
