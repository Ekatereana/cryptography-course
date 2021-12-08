export interface UserBase {
  id: string;
  email: string;
  fullName: string;
  username: string;
}

export interface User extends UserBase {
  password?: string;
}

export interface UserSignUp {
  username: string;
  email: string;
  fullName: string;
  password: string;
}

export interface Credentials {
  username: string;
  password: string;
}

export interface AfterLogin {
  id: string;
  fullName: string;
  email: string;
  username: string;
  sessionId?: string;
}
