import main as prog
from xml.dom import minidom

def test_picture_metadata():
    d1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001-22', 'Code' : '001'}
    d2 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '002'}
    d3 = {'Date' : '08/11/2022', 'Heure' : '10:50'}
    
    assert prog.picture_metadata("Footage/1.csv") == d1
    assert prog.picture_metadata("Footage/2.csv") == d2
    assert prog.picture_metadata("Footage/3.csv") == d3

def test_xmlwriter():
    #Variables exemples
    
    d1_1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001-22', 'Code' : '001'}
    d1_2 = {'hornetlength' : '11', 'abdomenshape' : 'Rond', 'cast' : 'Male', 'wingsspacing' : '12'}
    
    d2_1 = {'Date' : '08/11/2022', 'Heure' : '10:50', 'Reference' : '001-22'}
    d2_2 = {'hornetlength' : '11', 'abdomenshape' : 'Rond', 'cast' : 'Male'}
    
    # Ecriture des fichiers XML
    
    prog.xmlwriter(d1_1, d1_2, "Footage/1.png")
    prog.xmlwriter(d2_1, d2_2, "Footage/2.png")
    
    # Lecture des fichiers XML
    
    doc1 = minidom.parse("Results/1.xml")
    doc2 = minidom.parse("Results/2.xml")
    
    dico1 = {}
    dico2 = {}