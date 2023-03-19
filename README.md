# Zaštita lozinki simetričnom enkripcijom

Ovaj program pisan je u programskom jeziku **python** te je za implementaciju kriptografskih funkcija korišten python paket **pycryptodome** i moduli koje sadrži: ```Crypto.Hash```, ```Crypto.Random```, ```Crypto.Cipher```, ```Crypto.Protocol```

## Mogućnosti programa:
- inicijalizacija
- pohrana para adresa/zaporka
- dohvat zaporke za određenu adresu
- update zaporke za određenu adresu

## Inicijalizacija password managera

Komanda za inicijalizaciju password managera je sljedeća: ```./secretary init {masterPassword}```
Password manager sve podatke zapisuje u bazu podataka. Pri svakom dohvatu/spremanju podataka prvo se provjerava uneseni masterPassword. Zato je ovaj korak inicijalizacije jako bitan. Kao prvo, masterPassword potrebno je negdje spremiti da bismo kod kasnijih njegovih provjera nekako mogli do njega doći. MasterPassword spremljen je u zasebnu tablicu u bazi podataka uz sljedeće korake:
- generiranje ključa za simetričnu enkripciju komandom
- PBKDF2(sys.argv[2].strip(), salt, 32, count=1000, hmac_hash_module=SHA512)

## Pohrana para adresa/zaporka

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Dohvat lozinke za određenu adresu

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Update lozinke za određenu adresu

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.
