# Sensitive information storage

### General info

Backend та Frontend ми взяли із минулої лобораторної роботи. У цій лабораторній роботі ми вирішили шифрувати наступні дані:

* username
* full name
* email

(пароль хешується та шифрується за замовчуванням, тому у цьому списку його не вказували)

### How we encrypt the data

Для усіх даних, які ми шифрували, використовується алгоритма `xsalsa20` із заданим ключем та випадковим nonce. nonce генерується за допомогою функції `randomBytes` із стандартного можуля `crypto`. Ця функція є криптографічнобезпечною.
Ключ береться із змінної середовища.

### How we implement it

Враховуючи те, що ми використовуємо код із минулих проектів/лабораторних, то ми хотіли б змінювати чим менше коду, але при цьому додати шифрування для важливих даних. У коді є виклики до бд, діставання конекшина із пула і тд. Наприклад:

```js
const client = await this.connectionPool.connect();
client.query(...);
client.release();
```

Ми написали свій клас, який є обгорткою над `Pool, PoolClient` і має такий самий контракт, як і вони. Тепер ми просто в конструкторі підмінюємо `Pool` & `PoolClient` на свою обгортку. Для чого це? Просто в середині обгортки ми шифруємо дані. В результаті основний код не змінився (тільки конструктор) + ми можемо шифрувати дані.
Тепер потрібно придумати як саме їх шифрувати. Не все, що потрапляє у запит, потрібно шифрувати. В нашій поточній реалізації це виглядає ось так:

```js
await client.query('insert into users values ($1, $2, $3, $4, $5)', [
  user.id,                                     // do not encrypt
  { value: user.username, isEncrypted: true }, // encrypt username
  { value: user.email, isEncrypted: true },
  { value: user.fullName, isEncrypted: true },
  { value: user.password, isEncrypted: false } // do not encrypt. the same as just `user.password`
]);
```
Якщо коротко, то якщо опція `isEncrypted` явно сказана, то тоді шифрується. В усіх інших випадках - ні.

Для розшифровування ми теж повинні вказати, які колонки мають бути розшифровані. Приклад:

```js
const decryptedUser = decryptRow(user, { fullName: true, username: true, email: true });
```

Першим параметром передаємо об'єкт, поля якого треба розшифрувати. Другим параметром схему - тобто які поля реально потрібно розшифрувати.

