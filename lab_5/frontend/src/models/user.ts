
export interface IUser extends IUserShort {
  username: string;
  email: string;
}

export interface IUserShort {
  id: string;
  fullName: string;
  roles: string[];
}

export interface IMember {
  id: string;
  fullName: string;
  username: string;
  email: string;
}
