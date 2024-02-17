import base64

try:
    from pycaret.clustering import *
except ImportError as e:
    print("Error importing pycaret:", e)
import pandas as pd
import streamlit as st


# Function to create models and return evaluation metrics
def create_model_and_df(mod_name,df):
    km1_models = []
    df_km1 = pd.DataFrame(columns=['Number_of_Clusters', 'Silhouette', 'Calinski_Harabasz', 'Davies_Bouldin'])
    for i in range(3, 7):  # considering clusters from 3 to 6
        model = create_model(mod_name, num_clusters=i)
        km1_models.append(model)
        metrics = pull()
        metrics['Number_of_Clusters'] = f'k={i}'
        df_km1 = pd.concat([df_km1, metrics], ignore_index=True)
    df_km1 = df_km1[['Number_of_Clusters', 'Silhouette', 'Calinski-Harabasz', 'Davies-Bouldin']]

    return df_km1

# Function to rearrange DataFrame for better visualization
def rearrange_df(df):
    df = df.set_index('Number_of_Clusters').transpose()
    return df



def selecting_mondel(mod_name,df):
    setup(df, verbose=False)
    df_kmean_1 = create_model_and_df(mod_name,df)
    df_kmean_1 = rearrange_df(df_kmean_1)

    # with normalization
    setup(df, normalize=True, normalize_method='zscore', verbose=False)
    df_kmean_norm = create_model_and_df(mod_name,df)
    df_kmean_norm = rearrange_df(df_kmean_norm)

    # with transformation
    setup(df, transformation=True, transformation_method='yeo-johnson', verbose=False)
    df_kmean_trans = create_model_and_df(mod_name,df)
    df_kmean_trans = rearrange_df(df_kmean_trans)

    # with PCA
    setup(df, pca=True, pca_method='linear', verbose=False)
    df_kmean_pca = create_model_and_df(mod_name,df)
    df_kmean_pca = rearrange_df(df_kmean_pca)

    # with normalization + transformation
    setup(df, transformation=True, transformation_method='yeo-johnson', normalize=True, normalize_method='zscore',
          verbose=False)
    df_kmean_NT = create_model_and_df(mod_name,df)
    df_kmean_NT = rearrange_df(df_kmean_NT)

    # using nromalization + transformation + pca
    setup(df, pca=True, pca_method='linear', transformation=True, transformation_method='yeo-johnson', normalize=True,
          normalize_method='zscore', verbose=False)
    df_kmean_all = create_model_and_df(mod_name,df)
    df_kmean_all = rearrange_df(df_kmean_all)

    return df_kmean_1, df_kmean_norm, df_kmean_trans, df_kmean_pca, df_kmean_NT, df_kmean_all


def merge(merged_df,df1, df2, df3,df4 ,df5, df6):
    merged_df = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
    return merged_df;



def disp_tabel(table, model):
    df_html = table.to_html(index=True, justify='center')
    st.header(model)
    st.subheader(
        "no preprocessing    normalization     transformation      PCA      N+T     N+T+PCA")

    st.write(df_html, unsafe_allow_html=True)
    # st.write(df.style.set_properties(**{'text-align': 'center'}).format("{:.4f}"), height=400)

    # Download as Excel
    excel_buffer = pd.ExcelWriter(f'{model}.xlsx', engine='xlsxwriter')
    table.to_excel(excel_buffer, index=False)
    excel_buffer.save()
    excel_buffer.close()

    with open('data.xlsx', 'rb') as f:
        excel_data = f.read()
    b64_excel = base64.b64encode(excel_data).decode()
    href_excel = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="data.xlsx">Download Excel</a>'
    st.markdown(href_excel, unsafe_allow_html=True)

    st.download_button(
        label="Download CSV",
        data=table.to_csv().encode(),
        file_name=f'{model}.csv',
        mime='text/csv'
    )

def main():
    # Read CSV file
    st.title("CSV File Processor")

    # File uploader widget to upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    #
    # if uploaded_file is not None:
    #     # Process the uploaded CSV file
    #     df = pd.read_csv(uploaded_file)
    #     mod1_df = []
    #     df_kmean_1, df_kmean_norm, df_kmean_trans, df_kmean_pca, df_kmean_NT, df_kmean_all = selecting_mondel('kmeans', df)
    #     mod1_df = merge(mod1_df, df_kmean_1, df_kmean_norm, df_kmean_trans, df_kmean_pca, df_kmean_NT, df_kmean_all)
    #
    #     # Display the DataFrame
    #     st.subheader("comparison DataFrame:")
    #     st.write(mod1_df)

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        mod1_df = []
        mod2_df = []
        mod3_df = []
        df_kmean_1, df_kmean_norm, df_kmean_trans, df_kmean_pca, df_kmean_NT, df_kmean_all = selecting_mondel('kmeans', df)
        mod1_df = merge(mod1_df, df_kmean_1, df_kmean_norm, df_kmean_trans, df_kmean_pca, df_kmean_NT, df_kmean_all)

        df_hcul_1, df_hcul_norm, df_hcul_trans, df_hcul_pca, df_hcul_NT, df_hcul_all = selecting_mondel('hclust', df)
        mod2_df = merge(mod2_df, df_hcul_1, df_hcul_norm, df_hcul_trans, df_hcul_pca, df_hcul_NT, df_hcul_all)

        df_mod3_1, df_mod3_norm, df_mod3_trans, df_mod3_pca, df_mod3_NT, df_mod3_all = selecting_mondel('meanshift', df)
        mod3_df = merge(mod3_df, df_mod3_1, df_mod3_norm, df_mod3_trans, df_mod3_pca, df_mod3_NT, df_mod3_all)

        print(mod1_df)



        st.subheader("Uploaded DataFrame:")
        disp_tabel(mod1_df, "K-means")
        disp_tabel(mod2_df, "Hierarchical clustering")
        disp_tabel(mod3_df, "Mean shit clustering")


if __name__ == '__main__':
    main()