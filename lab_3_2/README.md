# Lab 3.2

### Algorithm

Ми знаємо, що під час створення акаунта, генератор за сід бере поточний час у секундах. Тому ми теж сідуємо наший локальний генератор поточним часом у секундах. Можливий випадок, коли наший сід буде на пару секунд підрізнятися від того, що на сервері. Тому в коді є цикл, для синхронізації.

Після того, як генератори синхронізовані, то я просто в циклі роблю ставки, допоки не буде потрібна сума.

### Conclusion

Використовувати в якості сіда не видпадкові дані погано.
