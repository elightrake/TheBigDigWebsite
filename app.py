from flask import Flask, render_template, request
import pandas as pd # type: ignore

app = Flask(__name__)

# Load the data
people_df = pd.read_csv('Matching - People.csv')
matches_df = pd.read_csv('Matching - Matches.csv')

# Set the default number of matches to display
num_matches = 1

def format_link(link):
    """Ensure the link starts with 'https://www.'."""
    if not link.startswith('https://'):
        link = 'https://www.' + link
    return link

def get_match_details(email):
    """Return match details based on email from the people_df."""
    match = people_df[people_df['Email'] == email].iloc[0]
    
    # Format links (instagram, website, and others)
    instagram = format_link(match['Instagram']) if not pd.isna(match['Instagram']) else None
    website = format_link(match['Website']) if not pd.isna(match['Website']) else None
    links = [format_link(match[col]) for col in ['Link1', 'Link2', 'Link3', 'Link4'] if not pd.isna(match[col])]

    details = {
        'name': match['Name'],
        'pronouns': match['Pronouns'],
        'roles': match['Roles'],
        'email': match['Email'],
        'instagram': instagram,
        'website': website,
        'links': links
    }
    return details

@app.route('/')
def index():
    return render_template('index.html', num_matches=num_matches)

@app.route('/result', methods=['POST'])
def result():
    email = request.form['email']
    if email not in matches_df['Email'].values:
        # If the email is invalid, return an error message
        return render_template('index.html', error="Invalid email. Please try again.", num_matches=num_matches)
    
    # Get top matches for the user
    matches = []
    for i in range(1, num_matches + 1):
        top_match_column = f'TopMatch{i}'
        if top_match_column in matches_df.columns:
            top_match_email = matches_df[matches_df['Email'] == email][top_match_column].values[0]
            matches.append(get_match_details(top_match_email))

    return render_template('result.html', matches=matches, num_matches=num_matches)

if __name__ == '__main__':
    app.run(debug=True)
