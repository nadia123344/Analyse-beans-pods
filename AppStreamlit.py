import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import read_csv



st.set_page_config(
    page_title="Analyse Beans & Pods",
    page_icon="☕",
    layout="wide"
)



produits = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']


@st.cache_data
def charger_donnees():
    df = pd.read_csv('BeansDataSet.csv')
    return df

try:
    donnees = charger_donnees()
except:
    st.error("Erreur lors du chargement des données")


menu = st.sidebar.title("Analyse Beans & Pods")
page = st.sidebar.selectbox(
    "Navigation",
    ["Accueil", "Analyse des Ventes", "Analyse Régionale", "Analyse des Canaux", "Visualisations"]
)


if page == "Accueil":
    st.title("📊 Tableau de bord Beans & Pods")
    st.write("Bienvenue dans l'analyse des données de Beans & Pods")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total des ventes", f"{donnees[produits].sum().sum():,.0f}")
    with col2:
        st.metric("Nombre de transactions", len(donnees))

elif page == "Analyse des Ventes":
    st.title("📈 Analyse des Ventes")
    
    ventes_totales = donnees[produits].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ventes_totales.plot(kind='bar')
    plt.title('Ventes par produit')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Analyse Régionale":
    st.title("🗺️ Analyse Régionale")
    
    region = st.selectbox("Sélectionner une région", donnees['Region'].unique())
    donnees_region = donnees[donnees['Region'] == region]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    donnees_region[produits].mean().plot(kind='bar')
    plt.title(f'Moyenne des ventes - {region}')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Analyse des Canaux":
    st.title("🏪 Analyse des Canaux de Distribution")
    
    
    ventes_canal = donnees.groupby('Channel')[produits].sum()
  

    st.subheader("Détails des ventes par canal")
    st.write(ventes_canal)
    
   
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ventes_canal.plot(kind='bar', ax=ax1)
    plt.title('Ventes par Canal de Distribution')
    plt.xlabel('Canal')
    plt.ylabel('Ventes')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig1)
    
    
    st.subheader("Distribution des ventes par produit et canal")

    fig2, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel() 


    for idx, produit in enumerate(produits):
        axes[idx].hist(donnees[donnees['Channel'] == 'Store'][produit], 
                      bins=30, alpha=0.5, label='Magasin', color='blue')
        axes[idx].hist(donnees[donnees['Channel'] == 'Online'][produit], 
                      bins=30, alpha=0.5, label='En ligne', color='orange')
        axes[idx].set_title(f'Distribution des ventes - {produit}')
        axes[idx].set_xlabel('Ventes')
        axes[idx].set_ylabel('Fréquence')
        axes[idx].legend()
    
    plt.tight_layout()
    st.pyplot(fig2)
   
    total_ventes = ventes_canal.sum().sum()
    pourcentage_canal = (ventes_canal.sum(axis=1) / total_ventes * 100).round(2)
 

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Ventes en magasin (%)", f"{pourcentage_canal['Store']}%")
    with col2:
        st.metric("Ventes en ligne (%)", f"{pourcentage_canal['Online']}%")



elif page == "Visualisations":
    st.title("📊 Visualisations Avancées")
    
    
    try:
        filename = 'BeansDataSet.csv'
        data = read_csv(filename)
        st.write("Aperçu des données :")
        st.write(data.head())
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
    
   
    st.subheader("Densité des ventes par produit")
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for idx, colonne in enumerate(produits):
        data[colonne].plot(kind='density', ax=axes[idx])
        axes[idx].set_title(f'Densité - {colonne}')
    
    plt.tight_layout()
    st.pyplot(fig)
    
   
    st.subheader("Matrice de corrélation")
    correlation = donnees[produits].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
    st.pyplot(fig)
    
  
    st.subheader("Distribution des ventes par produit")
    fig, ax = plt.subplots(figsize=(12, 6))
    donnees[produits].boxplot()
    plt.xticks(rotation=45)
    st.pyplot(fig)



st.markdown("---")
st.markdown("Développé par Nadia jebbor - Analyse des données de vente")