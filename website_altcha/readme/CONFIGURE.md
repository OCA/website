Go to Configuration/Website, check "Enable Altcha" under "Privacy". 
Some extra parameters will appear with all the ALTCHA information. 
This parameters are website dependent.

- `altcha_key`: This key is made to create the challenge and review it later

Also, the system adds the option to use some extra parameters:

- `altcha_secret_key`: Key used to use deterministic mode. 
  Using it will make it faster from a server perspective.
- `altcha_algorithm`: Algorithm used, by default `PBKDF2/SHA-512`, however, we can use:
  - Fast ones only for testing purposes: `SHA-256`, `SHA-384`, `SHA-512`
  - Good by default: `PBKDF2/SHA-256`, `PBKDF2/SHA-384`, `PBKDF2/SHA-512`
  - Memory Hard: `SCRYPT`. To be implemented
  - Memory Hard (it required argon2-cffi): `ARGON2ID`. To be implemented
- `altcha_timeout`: Number of minutes that we will trust the key, by default 5
- `altcha_cost`: Cost of the challenge. By default, 5000

