import requests
from ms_teams import TeamsBot
from config import TEAMS_APP_ID, TEAMS_APP_PASSWORD, JIRA_USER, JIRA_API_TOKEN, JIRA_DOMAIN

# Initialize Teams bot
bot = TeamsBot(app_id=TEAMS_APP_ID, app_password=TEAMS_APP_PASSWORD)

def get_jira_status(jira_id):
    url = f'https://{JIRA_DOMAIN}/rest/api/3/issue/{jira_id}'
    headers = {
        'Authorization': f'Basic {JIRA_USER}:{JIRA_API_TOKEN}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    issue = response.json()

    status = issue['fields']['status']['name']
    comments = [comment['body'] for comment in issue['fields']['comment']['comments']]
    latest_comment = comments[-1] if comments else 'No comments available.'

    return status, latest_comment

@bot.event
async def on_message(message):
    if message.text.lower().startswith('jira'):
        jira_id = message.text.split()[-1]
        status, comment = get_jira_status(jira_id)
        default_message = "Should you need to expedite your support request, please CAST Product Owner at po@abc.com"
        await message.reply(f'Jira ID: {jira_id}\nStatus: {status}\nLatest Comment: {comment}\n\n{default_message}')

bot.start()