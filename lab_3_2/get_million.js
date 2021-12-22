const MersenneTwister = require('mersenne-twister');
const http = require('http');

const createNewAccount = id => {
  return new Promise((resolve, reject) => http.get({
    hostname: '95.217.177.249',
    port: 80,
    path: `/casino/createacc?id=${id}`,
    agent: false
  }, res => {
    res.setEncoding('utf8');
      const buffer = [];
      res.on('data', chunk => {
        buffer.push(chunk);
      });
      res.on('end', () => {
        const data = buffer.join().toString();
        const resCode = res.statusCode;
        if (resCode  > 300) {
          reject({ err: `expected 200 or 201 status code. got: ${resCode}. body: ${data}` });
        } else {
          resolve(JSON.parse(data));
        }
      });
  }));
};

const bet = (mode, moneyAmount, num, id) => {
  // let numInt32 = Number(num) | 0;
  return new Promise((resolve, reject) => http.get({
    hostname: '95.217.177.249',
    port: 80,
    path: `/casino/play${mode}?id=${id}&bet=${moneyAmount}&number=${Number(num)}`,
    agent: false
  }, res => {
    res.setEncoding('utf8');
      const buffer = [];
      res.on('data', chunk => {
        buffer.push(chunk);
      });
      res.on('end', () => {
        const data = buffer.join().toString();
        const resCode = res.statusCode;
        if (resCode  > 300) {
          reject({ err: `expected 200 or 201 status code. got: ${resCode}. body: ${data}` });
        } else {
          resolve(JSON.parse(data));
        }
      });
  }));
};

(async () => {
  try {
    const now = Math.round(+(new Date()) / 1000) - 1;

    console.log(now);

    const account = await createNewAccount("fhfhsknxnxawww");
    console.log(account);

    const res = await bet('Mt', 1, 32, account.id);
    console.log(res);
    const realNumber = res.realNumber;
    let money = res.account.money;

    let generator = new MersenneTwister(now);
    for (let i = 1; i > 0; i++) {
      if (generator.random_int() === realNumber) {
        break;
      }
      generator = new MersenneTwister(now + i);
    }

    const generate = () => generator.random_int();

    while (money < 1000000) {
      const nextNumber = generate();
      console.log('gess: ' + nextNumber);
      const res = await bet('Mt', money - 1, nextNumber, account.id);
      console.log(res);
      money = res.account.money;
    }

  } catch (err) {
    console.error('Error:');
    console.error(err);
  }
})();
