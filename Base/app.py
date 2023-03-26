from flask import Flask, render_template, request, redirect
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    pdq_df = pd.read_csv('data/pdq.csv', sep=";")
    interventions_df = pd.read_csv('data/interventions.tsv', sep="\t")
    categorie_df = pd.read_csv('data/catégoriesInterventions.csv', sep=";")
    quart_df = pd.read_csv('data/quarts_travail.csv', sep=";")

    print(categorie_df['LIBELLÉ'])

    time = datetime.now().time()

    time_str = quart_df['HEURE_FIN'][0]
    time_fin_journee = datetime.strptime(time_str, '%H:%M:%S').time()
    time_str = quart_df['HEURE_DEBUT'][0]
    time_debut_journee = datetime.strptime(time_str, '%H:%M:%S').time()

    time_str = quart_df['HEURE_FIN'][1]
    time_fin_soir = datetime.strptime(time_str, '%H:%M:%S').time()
    time_str = quart_df['HEURE_DEBUT'][1]
    time_debut_soir = datetime.strptime(time_str, '%H:%M:%S').time()

    if(time < time_fin_journee and time > time_debut_journee):
        time_index = 1
    elif (time < time_fin_soir and time > time_debut_soir):
        time_index = 2
    else :
        time_index = 3

    nombre_interventions = interventions_df.groupby('PDQ')['PDQ'].size()
    pdq_df['NB_INTERVENTIONS'] = pdq_df['PDQ'].map(nombre_interventions)

    interventions_df.sort_values(by=['DATE_INCIDENT'], inplace=True, ascending=False)

    max_date = interventions_df.iloc[0]['DATE_INCIDENT']
    min_date = interventions_df.iloc[-1]['DATE_INCIDENT']

    # On va chercher la vaeur de modify_no_intervention
    interventions_df.sort_values(by=['ID_INTERVENTION'], inplace=True, ascending=True)
    modify_no_intervention = request.args.get('modify_no_intervention')
    noModifyInvalid=-1
    affichageModify=False
    lineToModify=interventions_df.iloc[0]
    # Si modify_no_intervention a une valeur non nulle on l'imprime sur la console
    if modify_no_intervention != None:
        if (interventions_df['ID_INTERVENTION'].astype(str) == str(modify_no_intervention)).any():
            noModifyInvalid = 0
            lineToModify=interventions_df.iloc[int(modify_no_intervention)]
        else:
            noModifyInvalid = 1

    modify_date_incident = request.args.get('modify_date_incident')
    modify_cat_intervention = request.args.get('modify_cat_intervention')
    modify_pdq_nb = request.args.get('modify_pdq_nb')
    modify_quart = request.args.get('modify_quart')
    modifEffectuee = False
    if ((modify_no_intervention != None) and  (modify_date_incident != None) and  (modify_cat_intervention != None) and  (modify_pdq_nb != None) and (modify_quart != None)):
        #Ouvrir le fichier des tâches en lecture, récupérer l'ensemble des lignes et fermer le fichier
        interventions_file = open(file='data/interventions.tsv', mode='r', encoding='UTF-8')
        lignes = interventions_file.readlines()
        interventions_file.close()
        #Écraser le fichier des tâches, réecrire l'ensemble des lignes incluant celle modifiée
        interventions_file = open(file='data/interventions.tsv', mode='w', encoding='UTF-8')
        for ligne in lignes:
            contenu = ligne.strip().split("\t")
            if contenu[0] == str(modify_no_intervention):
                ligne = contenu[0] + "\t" + modify_date_incident + "\t" + modify_cat_intervention + "\t" + modify_pdq_nb + "\t" + modify_quart + '\n'
            interventions_file.write(ligne)
        interventions_file.close()
        modifEffectuee=True

    # On va chercher la vaeur de remove_no_intervention
    remove_no_intervention = request.args.get('remove_no_intervention')
    # Si remove_no_intervention a une valeur non nulle on l'imprime sur la console
    if remove_no_intervention != None:
        print(remove_no_intervention)
    print(affichageModify)

    return render_template('Base_TP3.html', pdq_df=pdq_df, nombre_interventions=nombre_interventions.to_dict(), min_date=min_date, max_date=max_date, 
    modify_no_intervention=modify_no_intervention, noModifyInvalid=noModifyInvalid, 
    toModify={'pdq' : lineToModify['PDQ'], 'date' : lineToModify['DATE_INCIDENT'], 'cat': lineToModify['CATÉGORIE'], 'quart' : lineToModify['QUART_TRAVAIL']},
    categorie_df=categorie_df, quart_df=quart_df, time_index = time_index)


if __name__ == "__main__":
    app.run(host='localhost', port=5555, debug=False)
