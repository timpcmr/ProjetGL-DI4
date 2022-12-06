import XMLgenerator.picture_metadata as meta
import XMLgenerator.xmlwriter as xgen
import os
from xml.dom import minidom

def test_picture_metadata():
    
    # Variables exemples
    d1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001_22', 'Code' : '001'}
    d2 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '002'}
    d3 = {'Date' : '08/11/2022', 'Heure' : '10:50'}
    
    # Vérification de la robustesse de la fonction de lecture CSV
    assert meta.picture_metadata("Footage/1.csv") == d1
    assert meta.picture_metadata("Footage/2.csv") == d2
    assert meta.picture_metadata("Footage/3.csv") == d3

def test_xmlwriter():
    
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
    assert dico1_1 == d1_1
    assert dico1_2 == d1_2
    
    assert dico2_1 == {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001_22', 'Code' : 'UNDEFINED'}
    assert dico2_2 == {'hornetlength' : '11', 'abdomenshape' : 'Rond', 'cast' : 'Male', 'wingsspacing' : 'UNDEFINED'}
    
    # Suppression des fichiers XML (Désactivation)
    os.remove("Results/1.xml")
    os.remove("Results/2.xml")
    os.rmdir("Results")