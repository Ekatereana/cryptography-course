import React, { useState } from 'react';
import { connect } from 'react-redux';
import { registerRoutine } from '../../sagas/auth/routines';
import { IAppState} from '../../models/appState';
import styles from '../LoginPage/styles.module.sass';
import inputs from '../styles/inputs.module.sass';
import { Link } from 'react-router-dom';
import Loader from '../Loader';

const emailRegex = /^\S+@\S+\.\S+$/;
const usernameRegex = /^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$/;
const fullNameRegex = /^[a-zA-Z]{2,}(?: [a-zA-Z]+){0,2}$/;

const handleChange = (value: string,
                      regex: RegExp,
                      errorMessage: string,
                      set: (value: string) => void,
                      setError: (value: string) => void) => {
  if (regex.test(value)) {
    set(value);
    setError('');
  } else {
    set('');
    setError(errorMessage);
  }
};

const validatePassword = (password: string): boolean[] => {
  let lower = false;
  let upper = false;
  let num = false;
  let special = false;

  for (let i = 0; i < password.length; i++) {
    const c = password.charCodeAt(i);
    console.log(c);
    if (c >= 65 && c <= 90) {
      upper = true;
    }
    if (c >= 97 && c <= 122) {
      lower = true;
    }
    if (c >= 48 && c <= 57) {
      num = true;
    }
    if ((c >= 33 && c <= 47) || (c >= 58 && c <= 64) || (c >= 91 && c <= 96) || (c >= 123 && c <= 126)) {
      special = true;
    }
  }

  return [lower, upper, num, special, password.length >= 10];
};

const validatePasswords = (pass1: string,
                           pass2: string,
                           set: (value: string) => void,
                           setRepeatError: (value: string) => void,
                           setPasswordError: (value: boolean[]) => void
) => {
  setPasswordError(validatePassword(pass1));
  if (pass1 === '' || pass2 === '') {
    set(pass1);
    return;
  }
  if (pass1 !== pass2) {
    set(pass1);
    setRepeatError('passwords do not match');
    return;
  }
  set(pass1);
  setRepeatError('');
};

export interface IRegisterProps {
  isLoading: boolean;
  register(registerData: any): void;
}

const RegisterPage: React.FC<IRegisterProps> = ({ isLoading, register }) => {
  const [name, setName] = useState<string>('');
  const [nameError, setNameError] = useState<string>('');

  const [username, setUsername] = useState<string>('');
  const [usernameError, setUsernameError] = useState<string>('');

  const [email, setEmail] = useState<string>('');
  const [emailError, setEmailError] = useState<string>('');

  const [password, setPassword] = useState<string>('');
  const [passwordValidations, setPasswordValidations] = useState<boolean[]>([false, false, false, false, false]);
  const [passwordRepeat, setPasswordRepeat] = useState<string>('');
  const [passwordRepeatError, setPasswordRepeatError] = useState<string>('');

  const handleSubmit = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    e.preventDefault();
    console.log({ email, password, name, username });
    register({ email, password, fullName: name, username });
  };

  return (
    <div className={styles.login_page_wrapper}>
      <div className={`${styles.login_page} ${styles.register_page}`}>
        <div className={`${styles.column} ${styles.additional_info}`}>
          <span className={styles.title}>Welcome!</span>
          <span className={styles.text}>
            To keep connected with us please register
          </span>
          <span>
            Have a problem with registration? Then <Link to="/register" className={styles.link}>follow the link</Link>
          </span>
          <span>Already have an account? <Link to="/login" className={styles.link}>Login...</Link></span>
        </div>
        <form className={`${styles.column} ${styles.login_column}`}>
          <span>Register</span>
          <label>Username {usernameError && <span className={styles.error}>{usernameError}</span>}</label>
          <input className={inputs.input_standard} placeholder="e. g. cap.map" onChange={event =>
            handleChange(event.target.value, usernameRegex, ' not valid', setUsername, setUsernameError)
          }/>
          <label>Full Name {nameError && <span className={styles.error}>{nameError}</span>}</label>
          <input className={inputs.input_standard} placeholder="Max Pugachov" onChange={event =>
            handleChange(event.target.value, fullNameRegex, ' not valid', setName, setNameError)
          }/>
          <label>Email {emailError && <span className={styles.error}>{emailError}</span>}</label>
          <input className={inputs.input_standard} placeholder="exmaple@email.com" onChange={event =>
            handleChange(event.target.value, emailRegex, ' not valid', setEmail, setEmailError)
          }/>
          <label>Password</label>
          <label className={passwordValidations[0] ? styles.success : styles.error}>{passwordValidations[0] ? '\u2713' : '\u2717'} Lowercase letter</label>
          <label className={passwordValidations[1] ? styles.success : styles.error}>{passwordValidations[1] ? '\u2713' : '\u2717'} Uppercase letter</label>
          <label className={passwordValidations[2] ? styles.success : styles.error}>{passwordValidations[2] ? '\u2713' : '\u2717'} Number</label>
          <label className={passwordValidations[3] ? styles.success : styles.error}>{passwordValidations[3] ? '\u2713' : '\u2717'} Special character</label>
          <label className={passwordValidations[4] ? styles.success : styles.error}>{passwordValidations[4] ? '\u2713' : '\u2717'} Have minimum 10 symbols</label>
          <input className={inputs.input_standard} type="password" onChange={event =>
            validatePasswords(event.target.value, passwordRepeat, setPassword, setPasswordRepeatError, setPasswordValidations)
          }/>
          <label>Repeat password</label>
          <input className={inputs.input_standard} type="password"
                 onChange={event =>
                   validatePasswords(password, event.target.value, setPasswordRepeat, setPasswordRepeatError, setPasswordValidations)
                 }
          />
          {passwordRepeatError &&
            <label className={styles.error} style={{marginTop: "0.25em"}}>{passwordRepeatError}</label>
          }
          {isLoading
            ? <Loader />
            : <button onClick={handleSubmit}>Register</button>
          }
        </form>
      </div>
    </div>
  );
};

const mapStateToProps = (appState: IAppState) => ({
  isLoading: appState.auth?.isLoading
});

const mapDispatchToProps = {
  register: registerRoutine
};

export default connect(mapStateToProps, mapDispatchToProps)(RegisterPage);