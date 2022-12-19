import XMLgenerator.picture_metadata as meta
import XMLgenerator.xmlwriter as xgen
import os
from xml.dom import minidom

def test_picture_metadata():
    """Teste la bonne lecture du fichier CSV donné en entrée
    On teste ici la robestesse de la fonction de lecture de CSV en alterrant les données présentes dans le fichier.
    """
    
    # Variables exemples
    d1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001_22', 'Code' : '001'}
    d2 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '002'}
    d3 = {'Date' : '08/11/2022', 'Heure' : '10:50'}
    
    # Vérification de la robustesse de la fonction de lecture CSV
    assert meta.picture_metadata("Footage/1.csv") == d1 # Fichier complet (Format optimal)
    assert meta.picture_metadata("Footage/2.csv") == d2 # Fichier incomplet (Colonne manquante)
    assert meta.picture_metadata("Footage/3.csv") == d3 # Fichier incomplet (Colonne indiquée mais vide)

def test_xmlwriter():
    """Teste la bonne écriture des résultats dans le fichier XML
    On teste ici la robustesse de la fonction d'écriture de XML en alterrant les données présentes dans le fichier.
    Pour vérifier la bonne écriture, on lit ensuite le fichier XML généré et on compare les données lues avec celles attendues.
    """
    
    #Variables exemples
    d1_1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001_22', 'Code' : '001'}
    d1_2 = {'hornetlength' : '11', 'abdomenshape' : 'Rond', 'cast' : 'Male', 'wingsspacing' : '12'}
    
    d2_1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001_22'}
    d2_2 = {'hornetlength' : '11', 'abdomenshape' : 'Rond', 'cast' : 'Male'}
    
    # Ecriture des fichiers XML (Activation)
    xgen.xmlwriter(d1_2, d1_1, "Footage/1.png")
    xgen.xmlwriter(d2_2, d2_1, "Footage/2.png")
    
    # Lecture des fichiers XML
    doc1 = minidom.parse("Results/1.xml")
    doc2 = minidom.parse("Results/2.xml")
    
    dico1_1 = {}
    dico1_2 = {}
    dico2_1 = {}
    dico2_2 = {}
    
    
    dico1_1['Date'] = doc1.getElementsByTagName('date')[0].firstChild.nodeValue
    dico1_1['Heure'] = doc1.getElementsByTagName('time')[0].firstChild.data
    dico1_1['Reference'] = doc1.getElementsByTagName('trapreference')[0].firstChild.data
    dico1_1['Code'] = doc1.getElementsByTagName('trapcode')[0].firstChild.data
    
    dico2_1['Date'] = doc2.getElementsByTagName('date')[0].firstChild.data
    dico2_1['Heure'] = doc2.getElementsByTagName('time')[0].firstChild.data
    dico2_1['Reference'] = doc2.getElementsByTagName('trapreference')[0].firstChild.data
    dico2_1['Code'] = doc2.getElementsByTagName('trapcode')[0].firstChild.data
    
    dico1_2['hornetlength'] = doc1.getElementsByTagName('hornetlength')[0].firstChild.data
    dico1_2['abdomenshape'] = doc1.getElementsByTagName('abdomenshape')[0].firstChild.data
    dico1_2['cast'] = doc1.getElementsByTagName('cast')[0].firstChild.data
    dico1_2['wingsspacing'] = doc1.getElementsByTagName('wingsspacing')[0].firstChild.data
    
    dico2_2['hornetlength'] = doc2.getElementsByTagName('hornetlength')[0].firstChild.data
    dico2_2['abdomenshape'] = doc2.getElementsByTagName('abdomenshape')[0].firstChild.data
    dico2_2['cast'] = doc2.getElementsByTagName('cast')[0].firstChild.data
    dico2_2['wingsspacing'] = doc2.getElementsByTagName('wingsspacing')[0].firstChild.data
    
    # Vérification des fichiers XML
    
    # Ici on s'attend à retrouver toutes les données écrites car tous les champs sont spécifiés
    assert dico1_1 == d1_1
    assert dico1_2 == d1_2
    
    # Ici on s'attend à retrouver toutes les données écrites sauf les champs "Code" et "wingsspacing" qui doivent être remplacés par 'UNDEFINDED' car ils ne sont pas spécifiés.
    assert dico2_1 == {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001_22', 'Code' : 'UNDEFINED'}
    assert dico2_2 == {'hornetlength' : '11', 'abdomenshape' : 'Rond', 'cast' : 'Male', 'wingsspacing' : 'UNDEFINED'}
    
    # Suppression des fichiers XML (Désactivation)
    os.remove("Results/1.xml")
    os.remove("Results/2.xml")
    os.rmdir("Results")