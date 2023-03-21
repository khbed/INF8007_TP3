from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    pdq_df = pd.read_csv('data/pdq.csv', sep=";")
    interventions_df = pd.read_csv('data/interventions.tsv', sep="\t")

    nombre_interventions = interventions_df.groupby('PDQ')['PDQ'].size()
    pdq_df['NB_INTERVENTIONS'] = pdq_df['PDQ'].map(nombre_interventions)

    interventions_df.sort_values(by=['DATE_INCIDENT'], inplace=True, ascending=False)

    max_date = interventions_df.iloc[0]['DATE_INCIDENT']
    min_date = interventions_df.iloc[-1]['DATE_INCIDENT']

    # On va chercher la vaeur de modify_no_intervention
    modify_no_intervention = request.args.get('modify_no_intervention')
    # Si modify_no_intervention a une valeur non nulle on l'imprime sur la console
    if modify_no_intervention != None:
        print(modify_no_intervention)

    # On va chercher la vaeur de remove_no_intervention
    remove_no_intervention = request.args.get('remove_no_intervention')
    # Si remove_no_intervention a une valeur non nulle on l'imprime sur la console
    if remove_no_intervention != None:
        print(remove_no_intervention)

    return render_template('Base_TP3.html', pdq_df=pdq_df, nombre_interventions=nombre_interventions.to_dict(), min_date=min_date, max_date=max_date)


if __name__ == "__main__":
    app.run(host='localhost', port=5555, debug=False)
