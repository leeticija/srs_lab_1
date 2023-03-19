from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import sqlite3
import sys
import os
import base64
from Crypto.Hash import SHA256

def get_connection(file):
  try:
    connection = sqlite3.connect(file, check_same_thread=False)
    return connection
  except sqlite3.Error as error:
    print("An error occurred while connecting to database.")

# stvaranje baze
def initialize_database():
  os.remove('database.db')
  with open('database.db', 'w') as fp:
    pass
  connection = get_connection('database.db')
  try:
    query = """CREATE TABLE passwords(address VARCHAR, password VARCHAR, salt VARCHAR);
               CREATE TABLE master_password(master_password VARCHAR, salt VARCHAR);"""
    cursor = connection.cursor()
    cursor.executescript(query)
    cursor.close()
  except sqlite3.Error as error:
    print(error)

def get_password_by_address(address, master_pass):
  address_sha = SHA256.new(data=bytes(address.strip(), 'utf-8')).digest()
  connection = get_connection('database.db')
  cur = connection.cursor()
  cur.execute("""SELECT * FROM passwords WHERE address = '{a}';""".\
    format(a=base64.b64encode(address_sha).decode('ascii')))
  fetched = cur.fetchall()
  cur.close()
  connection.commit()
  connection.close()

  decoded_salt = base64.b64decode(fetched[0][2])
  key = PBKDF2(master_pass.strip(), decoded_salt, 32, count=1000, hmac_hash_module=SHA512)
  decoded = base64.b64decode(fetched[0][1])
  cipher2 = AES.new(key, AES.MODE_GCM, nonce=decoded[:16])
  decrypted = cipher2.decrypt(decoded[16:]).decode('utf-8')

  if base64.b64decode(decrypted[:44]) != address_sha:
    print("Master password incorrect or integrity check failed.")
  
  return base64.b64decode(decrypted[47:]).decode('utf-8')

# on database initialization masterpassword should be saved.
def save_master_password(master_password):
  # generate random salt for kdf:
  salt = get_random_bytes(16)
  key = PBKDF2(sys.argv[2].strip(), salt, 32, count=1000, hmac_hash_module=SHA512)
  # hash master password before encryption:
  hashed_password_to_encrypt = SHA256.new(data=bytes(sys.argv[2], 'utf-8')).digest()
  # prepare aes object before encryption:  
  cipher = AES.new(key, AES.MODE_GCM)
  # encrypt:
  ciphertext = cipher.encrypt(hashed_password_to_encrypt)
  # data to be saved in database: (nonce+ciphertext)
  data = cipher.nonce + ciphertext
  # encode bytes to base64 before saving to database:
  encoded = base64.b64encode(data).decode('ascii')
  # same for the salt that was used for generating key:
  encoded_salt = base64.b64encode(salt).decode('ascii')
  # save to database:
  connection = get_connection('database.db')
  query = """INSERT INTO master_password (master_password, salt) VALUES ('%s', '%s')""" % (encoded, encoded_salt)
  cur = connection.cursor()
  cur.execute(query)
  cur.close()
  connection.commit()
  connection.close()

def check_master_password(password):
  connection = get_connection('database.db')
  query = """SELECT * FROM master_password"""
  cur = connection.cursor()
  cur.execute(query)
  fetched = cur.fetchall()
  cur.close()
  connection.commit()
  connection.close()
  # decode fetched pass and salt with base64 decoder:
  decoded_pass = base64.b64decode(fetched[0][0])
  decoded_salt = base64.b64decode(fetched[0][1])
  # generate key for decryption:
  key = PBKDF2(password.strip(), decoded_salt, 32, count=1000, hmac_hash_module=SHA512)
  cipher2 = AES.new(key, AES.MODE_GCM, nonce=decoded_pass[:16])
  plaintext = cipher2.decrypt(decoded_pass[16:])
  return SHA256.new(data=bytes(password, 'utf-8')).digest() == plaintext

def put_password(master_pass, address, password):
  # check if address already exists. (address is SHA summed and saved to database)
  address_sha = SHA256.new(data=bytes(address.strip(), 'utf-8')).digest()
  # check if address already exists in database:
  connection = get_connection('database.db')
  cur = connection.cursor()
  cur.execute("""SELECT * FROM passwords WHERE address = '{a}'""".\
    format(a=base64.b64encode(address_sha).decode('ascii')))
  fetched = cur.fetchall()
  cur.close()
  connection.commit()
  connection.close()
  # else: put new address and password to database:
  salt = get_random_bytes(16)
  key = PBKDF2(master_pass.strip(), salt, 32, count=1000, hmac_hash_module=SHA512)
  cipher = AES.new(key, AES.MODE_GCM)
  to_encrypt = base64.b64encode(address_sha).decode('ascii') + " : " + base64.b64encode(bytes(password, 'utf-8')).decode('ascii')
  ciphertext = cipher.encrypt(bytes(to_encrypt, 'utf-8'))  
  # data to be saved in database: (nonce+ciphertext)
  data = cipher.nonce + ciphertext
  print("size of data before base64:", len(data))
  # encode bytes to base64 before saving to database:
  encoded = base64.b64encode(data).decode('ascii')
  # same for the salt that was used for generating key:
  encoded_salt = base64.b64encode(salt).decode('ascii')
  #print("encoded_salt:", encoded_salt)

  connection = get_connection('database.db')
  cur = connection.cursor()

  if len(fetched) != 0:
    # update password for existing address.
    print("Address already exists. Updating.")
    cur.execute("""UPDATE passwords SET password='{p}', salt='{s}' WHERE address = '{q}';""".\
      format(p=encoded, s=encoded_salt, q=base64.b64encode(address_sha).decode('ascii')))
    cur.close()
    connection.commit()
    connection.close()
    return
  
  cur.execute("INSERT INTO passwords VALUES ('{a}','{p}','{s}')".\
        format(a=base64.b64encode(address_sha).decode('ascii'), p=encoded, s=encoded_salt))
  cur.close()
  connection.commit()
  connection.close()

if sys.argv[1].strip() not in ['get', 'put', 'init']:
  print("Incorrect arguments. Choose between get, put, init.")

elif sys.argv[1].strip() == 'init':
   initialize_database()
   save_master_password(sys.argv[2])
   print("Password manager initialized.")

elif sys.argv[1].strip() == 'put':
  if not check_master_password(sys.argv[2]):
    print("Master password incorrect or integrity check failed.")
  else:
    put_password(sys.argv[2], sys.argv[3], sys.argv[4])
    print("Stored password for", sys.argv[3])

elif sys.argv[1].strip() == 'get':
  if not check_master_password(sys.argv[2]):
    print("Master password incorrect or integrity check failed.")
  else:
    p = get_password_by_address(sys.argv[3].strip(), sys.argv[2].strip())
    print("Password for", sys.argv[3], "is:", p)
