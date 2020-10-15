
# this is csug cycle1's ipv4 address
# ADDR = 128.151.69.85

# ADDR = 192.168.0.192
ADDR = 127.0.0.1
PORT = 12345

server:
	@printf 'Issuing the following command: $ '
	python3 rps.py Simon server $(PORT)


client:
	@printf 'Issuing the following command: $ '
	python3 rps.py Clinton client $(ADDR):$(PORT)
