import React from 'react';
import styles from './styles.scss';
import { LoginForm, SignupForm } from 'components/AuthForms';

const Auth = (props, context) => (
  <main className={styles.auth}>
    <div className={styles.column}>
      <img src={require("images/phone.png")} alt="Checkout our app" />
    </div>
    <div className={styles.column}>
      <div className={`${styles.whiteBox} ${styles.formBox}`}>
        <img src={require("images/logo.png")} alt="logo" />
        {props.action === "login" && <LoginForm />}
        {props.action === "signup" && <SignupForm />}
      </div>
      <div className={styles.whiteBox}>
        {props.action === "login" && (
          <p className={styles.text}>
            Don't have and account?{" "}
            <span onClick={props.changeAction} className={styles.changeLink}>
              Sign up
            </span>
          </p>
        )}

        {props.action === "signup" && (
          <p className={styles.text}>
            Have an account?{" "}
            <span onClick={props.changeAction} className={styles.changeLink}>
              Log in
            </span>
          </p>
        )}
      </div>
      <div className={styles.appBox}>
        <span>Get the app</span>
        <div className={styles.appStores}>
          <img
            src={require("images/app-ios.png")}
            alt="Download it on the Apple Appstore"
          />
          <img
            src={require("images/app-android.png")}
            alt="Download it on the Androidstore"
          />
        </div>
      </div>
    </div>
  </main>
);

export default Auth;