import React from "react";
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import  "./styles.scss";
import Footer from "components/Footer";
import Auth from 'components/Auth';

// class App extends Component {
//   render() {
//     return <div className={styles.App}>
//         <Switch>
//             <Route exact path="/" render={() => "hello!"} />
//             <Route path="/login" render={() => "login!"} />
//         </Switch>
//         <Footer />
//       </div>;
//   }
// }

const App = props => [
  // Nav,
  //Routes,
  props.isLoggedIn ? <PrivateRoutes key={2} /> : <PublicRoutes key={2} />, // privateRoute : //Public
  //Footer
  <Footer key={3} />
];

App.propTypes = {
    isLoggedIn: PropTypes.bool.isRequired
};

const PrivateRoutes = props => (
  <Switch>
    <Route key="1" exact path="/" render={() => "feed"} />,
    <Route key="2" exact path="/explore" render={() => "explore"} />
  </Switch>
);

const PublicRoutes = props => (
  <Switch>
    <Route key="1" exact path="/" component={Auth} />,
    <Route key="2" exact path="/forgot" render={() => "password"} />
  </Switch>
);

export default App;