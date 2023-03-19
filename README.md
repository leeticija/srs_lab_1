# Zaštita lozinki simetričnom enkripcijom

Ovaj program pisan je u programskom jeziku ```python``` te je za implementaciju kriptografskih funkcija korišten python paket ```pycryptodome``` https://pycryptodome.readthedocs.io/en/latest/src/introduction.html i moduli: ```Crypto.Hash```, ```Crypto.Random```, ```Crypto.Cipher```, ```Crypto.Protocol```. Pokreće se iz komandne linije uz ključne riječi i dodatne proizvoljne argumente.

## Mogućnosti programa:
- inicijalizacija ```init```
- pohrana para adresa/zaporka ```put```
- dohvat zaporke za određenu adresu ```get```
- update zaporke za određenu adresu ```put```

## Inicijalizacija password managera

Komanda za inicijalizaciju password managera je sljedeća: ```./secretary init {masterPassword}```

Password manager sve podatke zapisuje u bazu podataka. Pri svakom dohvatu/spremanju podataka prvo se provjerava uneseni masterPassword. Zato je ovaj korak inicijalizacije jako bitan. Kao prvo, masterPassword potrebno je negdje spremiti da bismo kod kasnijih njegovih provjera nekako mogli do njega doći. MasterPassword spremljen je u zasebnu tablicu u bazi podataka uz sljedeće korake:

- generiranje ```salt``` vrijednosti te ključa za simetričnu enkripciju komandama:

```salt = get_random_bytes(16)```

```PBKDF2(masterPassword, salt, 32, count=1000, hmac_hash_module=SHA512)```

- računanje hash sume raw vrijednosti danog master passworda:

```master_sha = SHA256.new(data=bytes(sys.argv[2], 'utf-8')).digest()```

- enkripcija dobivene hash vrijednost:

```AES.encrypt(master_sha)```

- budući da prilikom enkripcije funkcija ```encrypt()``` samostalno generira ```nonce``` (najčešće informacija od 16 bajtova) koja služi kao dodatna metoda zaštite i jednokratno se koristi. ```nonce``` je potreban i za dekripciju pa ga je potrebno sačuvati. Stoga se prefiksira na šifrat lozinke te se zatim enkodira ```base64``` enkoderom i sprema u bazu. Prilikom dešifriranja masterPassworda ```nonce``` lako se ponovno ekstrahira (prvih 16 bajtova).


Baza podataka ima sljedeće tablice i podatke:

```TABLE passwords(address VARCHAR, password VARCHAR, salt VARCHAR)```

```TABLE master_password(master_password VARCHAR, salt VARCHAR)```

## Pohrana para adresa/zaporka

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Dohvat lozinke za određenu adresu

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Update lozinke za određenu adresu

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.
