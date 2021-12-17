# Password generator

### CLI tool

Ми написали невелику cli tool, щоб генерувати паролі, хеші, та зберігати їх у файл. Тут коротка інструкція яу нею користуватися:

```bash
lab_4 1.0
Pavlo Myroniuk <pspos.developqkation@gmail.com>, Ekatereana Gricaenko <ekatereanagricaenko@gmail.com>
can generate new passwords and their hashes

USAGE:
    lab_4 [FLAGS] [OPTIONS] --pass-amount=pass-amount 

FLAGS:
    -h, --help         Prints help information
        --not-print    do not print the generated data to stdout
    -v, --version      Prints version information

OPTIONS:
        --hash=hash...                specify hashing algorithms [values: argon2 bcrypt md5 sha256]
        --out=out                     specify a filepath to save generated data
        --out-format=out-format       specify a file format for output file [values: csv]
        --pass-amount=pass-amount     specify amount of passwords to generate
```

Приклад використання:

```bash
./lab_4 --pass-amount 100000 --hash sha256 --hash md5 --not-print --out passwords_without_salt.csv
./lab_4 --pass-amount 100000 --hash argon2 --hash bcrypt --not-print --out passwords_with_salt.csv
```

Процеси генерації паролів, хешування запускаються у різних потоках, якщо кількість, яку потрібно згенерувати >= 500. Тому якщо увесь процес завантажений, то це нормально.

### Як генеруються паролі:

* common paswords: знайшли 10 000 паролів. Всі вони у файлі `top_passwords.txt`. Наший генератор видає випадкові паролі із цього списку в 60% випадків
* random passwords: в нас є визначений алфавіт допустимих символів для пароля. `const ALPHABET: [char; 84] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '/', '|', '?', '<', '>', ':', ';'];` Теретично це не всі допустимі символи, що можна ввести на клавіатурі, але цих теж достатньо. Випадковим чином вибирається довжина пароля у проміжку від 12 до 18. Потім випадковим чином вибираються символи із заданого алфавіту для пароля. Випадкові паролі генеруються в 10% випадків
* human like passwords: для початку знайшли словник допустимих слів. Думали взяти просто слова із словника, але зробили цікавіше: взяли датасет із іменами, прізвищами та назвами вулиць. Всі ці дані у файлі `dictionary.txt`. Із цього файлу випадковим чином вибираються слова допоки їх сумарна довжина не буде як мінімум 12. Потім робиться заміна символів на цифри, пробіла на будь який спеціальний символ. `e -> 3, o -> 0, ch -> 4 etc...`. Приклад таких згенерований паролів:

```bash
Christins~Nic0la&St3fan0
Ang3l0%Al3ssia
Silv3nt3$Shahilla
```

Такі паролі досить схожі на ті, які люди пишуть, коли їх попросити придумати "складний" пароль. Вони генеруються в 30% випадків.

### Хешування

Ми реалізували:

* md5
* sha256
* bcrypt with salt
* argon2 with salt

csv файли із хешами можна знайти в чаті.

В якості генератора випадкових чисел вибрали `ChaCha`.

