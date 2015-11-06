from flask import Flask, render_template, redirect, url_for
from app.pyGlialo import extract_winner, get_meetup_json, save_winners_list

app = Flask(__name__)

meetup_json = get_meetup_json()

list_of_winners = []


@app.route('/')
def spread_the_goodies():
    winner_json = extract_winner(meetup_json)
    winner = {'name': winner_json['name'], 'member_id': winner_json['member_id']}
    return render_template('index.html', winner=winner, winners=list_of_winners, lead_text='Rolling for the goodies')


@app.route('/save/<name>/')
def save_winner(name):
    if name not in list_of_winners:
        list_of_winners.append(name)
    return redirect(url_for('spread_the_goodies'))


@app.route('/pass')
def pass_extraction():
    list_of_winners.append('empty_slot')
    return redirect(url_for('spread_the_goodies'))


@app.route('/finalize')
def finalize_the_goodies():
    save_winners_list(list_of_winners)
    return render_template('finalize.html', winners=list_of_winners)


if __name__ == '__main__':
    app.run(debug=True)