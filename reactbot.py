import os
import time
from slackclient import SlackClient

#get bot's ID from environment variable
BOT_ID = os.environ.get("BOT_ID")

#other variables
AT_BOT = "<@" + BOT_ID + ">"
Ex_Command = "print reactions"
key = "volleyball"

#instantiate Slack and Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def findMessage(channel, key):
	allMessages = slack_client.api_call("channel.history",channel=channel)

	for message in allMessages:
		if "react to" and key in message["text"]:
			return message["ts"]

def handle_command(command, channel):
	""" Receives commands directed at the bot"""

	response = "Please begin your command with the phrase 'print reactions'"
	if command.startswith(Ex_Command):
		response = 'nice'
	slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)



def parse_slack_output(slack_rtm_output):
    """Returns None unless a message is directed at the Bot, 
    based on its ID."""

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']

            #if statement for if output is not directed at bot but holds keywords
    return None, None


def main():

	if __name__ == "__main__":
		READ_WEBSOCKET_DELAY = 1 
		if slack_client.rtm_connect():
			print("ReactBot connected!")
			while True:
				command, channel = parse_slack_output(slack_client.rtm_read())
				if command and channel:
					handle_command(command, channel)
				time.sleep(READ_WEBSOCKET_DELAY)
        
		else:
			print("Connection failed. Invalid Slack token or bot id?")
        id = findMessage(channel)
main()
