import React from "react";
import formStyles from "shared/formStyles.scss";
import Proptypes from "prop-types";
import FacebookLogin from 'react-facebook-login';
//import Ionicon from "react-ionicons";

export const LoginForm = (props, context) => <div className={formStyles.formComponent}>
           <form className={formStyles.form} onSubmit={props.handleSubmit}>
             <input type="text" placeholder={context.t("Username")} className={formStyles.textInput} value={props.usernameValue} onChange={props.handleInputChange} name="username" />
             <input type="password" placeholder={context.t("Password")} className={formStyles.textInput} value={props.passwordValue} onChange={props.handleInputChange} name="password" />
             <input type="submit" placeholder={context.t("Log in")} className={formStyles.button} />
           </form>
           <span className={formStyles.divider}>or</span>
           <FacebookLogin appId="541464489550594" autoLoad={true} fields="name,email,picture" callback={props.handleFacebookLogin} cssClass={formStyles.facebookLink} icon="fa-facebook-official">
             {/* <Ionicon icon="logo-facebook" fontSize="20px" color="#385185" />{" "} {context.t("Log in with Facebook")} */}
           </FacebookLogin>
           <span className={formStyles.forgotLink}>
             {context.t("Forgot password?")}
           </span>
         </div>;

LoginForm.prototype = {
  usernameValue: Proptypes.string.isRequired,
  passwordValue: Proptypes.string.isRequired,
  handleInputChange: Proptypes.func.isRequired,
  handleSubmit: Proptypes.func.isRequired,
  handleFacebookLogin: Proptypes.func.isRequired,
}

LoginForm.contextTypes = {
  t: Proptypes.func.isRequired
};

export default LoginForm;