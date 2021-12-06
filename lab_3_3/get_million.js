const http = require('http');

class FixedArray {
  constructor(maxlen) {
    this.maxlen = maxlen;
    this.data = [];
  }

  static fromArray(arr) {
    const fixedArray = new FixedArray(arr.length);
    fixedArray.data = arr;
    return fixedArray;
  }

  push(value) {
    this.data.push(value);
    const diff = this.data.length - this.maxlen;
    if (diff > 0) {
      this.data.splice(0, diff);
    }
  }

  get(index) {
    let i = Number(index);
    if (i < 0) {
      i = this.data.length - Math.abs(i);
    }
    return this.data[i];
  }
}

const generatorParams = {
  w: 32n,              // word size
  n: 624n,             // degree of recursion
  m: 397n,             // middle term
  r: 31n,              // separation point of one word
  a: BigInt(0x9908b0df),      // bottom row of matrix A
  u: 11n,              // tempering shift
  s: 7n,               // tempering shift
  t: 15n,              // tempering shift
  l: 18n,              // tempering shift
  b: BigInt(0x9d2c5680),      // tempering mask
  c: BigInt(0xefc60000),      // tempering mask
};

const undoXorRShift = (x, shift) => {
  let res = x;
  for (let shiftAmount = shift; shiftAmount < generatorParams.w; shiftAmount += shift) {
    res ^= (x >> shiftAmount);
  }
  return res;
};

const undoXorLShiftMask = (x, shift, mask) => {
  let window = (1n << shift) - 1n;
  for (let i = 0; i < generatorParams.w / shift; i++) {
    x ^= (((window & x) << shift) & mask);
    window <<= shift;
  }
  return x;
};

const temper = x => {
  x ^= (x >> generatorParams.u);
  x ^= ((x << generatorParams.s) & generatorParams.b);
  x ^= ((x << generatorParams.t) & generatorParams.c);
  x ^= (x >> generatorParams.l);
  return x;
};

const untemper = x => {
  x = undoXorRShift(x, generatorParams.l);
  x = undoXorLShiftMask(x, generatorParams.t, generatorParams.c);
  x = undoXorLShiftMask(x, generatorParams.s, generatorParams.b);
  x = undoXorRShift(x, generatorParams.u);
  return x;
};

const upper = x => {
  return x & ((1n << generatorParams.w) - (1n << generatorParams.r));
}

const lower = x => x & ((1n << generatorParams.r) - 1n);

const timesA = x => {
  if (x & 1n) {
    return (x >> 1n) ^ generatorParams.a;
  } else {
    return (x >> 1n);
  }
};

const readPrevValuesFromFile = filepath => require('fs').readFileSync(filepath, 'utf-8').trim().split('\n').map(e => BigInt(+e));

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

const getGenerator = seen => () => {
  const nextVal = seen.get(-generatorParams.n + generatorParams.m) ^ timesA(
      upper(seen.get(-generatorParams.n)) | lower(seen.get(-generatorParams.n + 1n))
  );
  seen.push(nextVal);
  return temper(nextVal);
};

const testPrediction = (seen, test) => {
  for (const val of test) {
    const nextVal = seen.get(-generatorParams.n + generatorParams.m) ^ timesA(
        upper(seen.get(-generatorParams.n)) | lower(seen.get(-generatorParams.n + 1n))
    );
    seen.push(nextVal);
    const predicted = temper(nextVal);
    console.log(`actual: ${val}; predicted: ${predicted}; ${val === predicted}`);
  }
};

const values = readPrevValuesFromFile('./seq.txt');
const seen = FixedArray.fromArray(values.slice(0, Number(generatorParams.n)).map(e => untemper(e)));

// const test = values.slice(Number(generatorParams.n));
// testPrediction(seen, test);

(async () => {
  try {
    const account = await createNewAccount(939);
    console.log(account);

    const numbers = [];
    let money = 0;
    for (let i = 0; i < generatorParams.n; i++) {
      const res = await bet('Mt', 1, 32, account.id);
      numbers.push((res.realNumber));
      money = res.account.money;
    }

    const seen = FixedArray.fromArray(numbers.map(e => untemper(BigInt(+e))));
    const generate = getGenerator(seen);

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
