import requests

def forward_email(data):
	try:
		requests.post(
			"https://api.mailgun.net/v3/{domain-name}/messages",
			auth=("api", "{mail-gun-api-key}"),
			data={"from": "{email-from}",
				"to": ["{}".format(data['email'])],
				"subject": "Registration Activation Link",
				"text": "Click the following link or copy paste on web browser to activate the account : <a href='{}'></a>".format(data['link_url'])})
	except Exception as e:
		print(str(e))
    
	
    