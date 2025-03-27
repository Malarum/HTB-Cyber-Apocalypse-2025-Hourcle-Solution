from pwn import *
import string

# Target server details
ip_addr = "94.237.63.241" #Enter your server ip here
port = 32219 #enter your port here

# Charset for brute-force attack
s = connect(ip_addr, port)

def get_encrypted_data(username):
    """Connects to the server and retrieves the encrypted hex data for a given username."""
      # Establish connection
    s.sendline(b'1')  # Send option to provide username
    s.sendline(username.encode())  # Send username
    
    # Read until encrypted data
    s.recvuntil(b'[+] Speak thy name, so it may be sealed in the archives :: [+] Thy credentials have been sealed in the encrypted scrolls: ')
    encrypted_hex = s.recvline().strip().decode()
    
    return bytes.fromhex(encrypted_hex)  # Convert hex to raw bytes

def brute_force():
    multiplyer = 47
    known_chars = ""
    charset = string.ascii_letters + string.digits
    while len(known_chars) < 20:
        for char in charset:
            test_username = 'B' * multiplyer
            test_password = known_chars + char
            new_username = test_username + test_password
            decrypt = get_encrypted_data(new_username)


            print(f'[+] Current brute force: {new_username} | Your current password is: {known_chars}')
            decrypt2 = get_encrypted_data(test_username)
            #print(f'Trying {char} for username: {test_username}')
            #if len(known_chars) <= 16:
            if decrypt[28:48] == decrypt2[28:48]:
                known_chars += char
                multiplyer -= 1
                print(f'[+] found a match {char} | current password {known_chars} | current username {new_username}')

    return(known_chars)


def main():
    recovered_password = brute_force()
    print(f'[+] Password recovered!: {recovered_password}')
    s.sendline(b'2')
    s.sendline(recovered_password.encode())
    s.recvuntil(b'[+] Whisper the sacred incantation to enter the Forbidden Sanctum :: [+] The gates open before you, Keeper of Secrets! ')
    flag = s.recvline().strip().decode()
    print(f'[+] Congratualtions on capturing the flag! {flag}')

main()

