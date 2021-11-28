import * as bcrypt from 'bcrypt';
import { sha512 } from 'sha.js';

// schema: bcrypt(salt + sha512(password))
export const hashPassword = async (password: string): Promise<string> => {
  const hash = await bcrypt.hash(new sha512().update(password).digest('hex'), 16);
  return hash.substr(7);
};

export const comparePasswords = (password: string, hash: string): Promise<boolean> => {
  const middlePassword = new sha512().update(password).digest('hex');
  const middleHash = '$2b$16$' + hash;
  return bcrypt.compare(middlePassword, middleHash);
};
