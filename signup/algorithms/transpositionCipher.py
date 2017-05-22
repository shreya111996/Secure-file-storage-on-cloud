def encrypt(message, key):
	index = 0
	count = 0
	cipher = []

	for letter in message:
		cipher.append(message[index])
		index += key

		if index > len(message) - 1:
			count += 1
			index = count
			
	return ''.join(cipher)

def decrypt(cipher, key):
	message = [''] * len(cipher)
	index = 0
	count = 0

	for letter in cipher:
		message[index] = letter
		index += key
		if index > len(cipher) - 1:
			count += 1
			index = count

	return ''.join(message)