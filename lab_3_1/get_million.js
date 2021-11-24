const http = require('http');

const a = 1664525;
const c = 1013904223;
const m = 4294967296;

const account_id = 7500;

const generateNext = prev => {
  return (prev * a + c) % m;
};

const createNewAccount = () => {
  return new Promise((resolve, reject) => http.get({
    hostname: '95.217.177.249',
    port: 80,
    path: `/casino/createacc?id=${account_id}`,
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
  let numInt32 = num | 0;
  return new Promise((resolve, reject) => http.get({
    hostname: '95.217.177.249',
    port: 80,
    path: `/casino/play${mode}?id=${id}&bet=${moneyAmount}&number=${numInt32}`,
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
    const account = await createNewAccount();
    console.log(account);

    let res = await bet('Lcg', 1, 32, account.id);
    console.log(res);

    let realNumber = res.realNumber;
    let money = res.account.money;

    while (money < 1000000) {
      const nextNumber = generateNext(+realNumber);
      console.log('gess: ' + nextNumber);
      const tmp = await bet('Lcg', account.money - 1, nextNumber, account.id);
      console.log(tmp);
      realNumber = +tmp.realNumber;
      money = tmp.account.money;
    }
  } catch (err) {
    console.error('Error:');
    console.error(err);
  }
})();

