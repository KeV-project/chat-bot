import slack_utility
import time

file = open('info.txt', 'w') 
order = 0
order_num = 1

#Пока что бот может работать только по определенному алгоритму:
#Для начала диалога необходимо поздароваться с ботом или сообщить о готовности сделать заказ 

def handle_command(slack_api, command, channel):

	file = open('info.txt', 'a') 
	global order
	global order_num

	if order == 0:
		if command.lower().startswith('hi') or command.lower().startswith('hey') or command.lower().endswith('order') or command.lower().startswith('pizza'):
			slack_api.rtm_send_message(channel, 'Hi, do you want to place an order?')
			order = 1
		else:
			print ('Invalid Command: Not Understood')
			slack_api.rtm_send_message(channel, 'Invalid Command: Not Understood')
	elif order == 1:
		if command.lower().startswith('yes') or command.lower().startswith('sure'):
			slack_api.rtm_send_message(channel, 'I\'m writing down')
			order = 2
		else:
			print ('Invalid Command: Not Understood')
			slack_api.rtm_send_message(channel, 'Invalid Command: Not Understood')
	elif order == 2:
		file.write('Заказ № ' + str(order_num) + ' ' + command + '\n')
		slack_api.rtm_send_message(channel, 'Thank! Your order is accepted')
		order_num = order_num + 1
		order = 0

	

	file.close()


	
	
def main():

	READ_WEBSOCKET_DELAY = 1 
	slack_api = slack_utility.connect()
	if slack_api.rtm_connect():
		print ('SLACK_BOT connected and running')
		while True:
			command, channel = slack_utility.parse_slack_response(slack_api.rtm_read())
			if command and channel:
				handle_command(slack_api, command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print ('Connection failed. Invalid Slack token or bot ID?') 


if __name__ == '__main__':
	main()

file.close()