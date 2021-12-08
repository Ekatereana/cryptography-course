import { hash, verify, Options } from 'argon2';
import { checkAndGetEnv } from '../utils/utils';
const xsalsa20 = require('xsalsa20');
import { randomBytes, createHash } from 'crypto';

const argonOptions = {
  memoryCost: 4096,
  timeCost: 4096,
  parallelism: 1,
} as Options & { raw: true };

export const hashPassword = async (password: string): Promise<string> => {
  const sha1Hasher = createHash('sha1');
  sha1Hasher.update(password);
  let pass = sha1Hasher.digest().toString('hex');

  const passwordHash = await hash(pass, argonOptions);

  const cipherKey = checkAndGetEnv('CIPHER_KEY');

  const bufferNonce = randomBytes(32);
  const passwordBuffer = Buffer.from(passwordHash);

  const xor = xsalsa20(bufferNonce, Buffer.from(cipherKey, 'utf-8'));
  let cipher = Buffer.from(xor.update(passwordBuffer)).toString('hex');

  return `${bufferNonce.toString('hex')}$${cipher}`;
};

export const comparePasswords = async (password: string, hash: string): Promise<boolean> => {
  const cipherKey = checkAndGetEnv('CIPHER_KEY');

  const [nonce, cipher] = hash.split('$');
  const cipherBuffer = Buffer.from(cipher, 'hex');
  const bufferNonce = Buffer.from(nonce, 'hex');

  const xor = xsalsa20(bufferNonce, Buffer.from(cipherKey, 'utf-8'));
  const passwordHash = Buffer.from(xor.update(cipherBuffer)).toString('utf-8');

  const sha1Hasher = createHash('sha1');
  sha1Hasher.update(password);
  let pass = sha1Hasher.digest().toString('hex');

  return verify(passwordHash, pass, argonOptions);
};
