import React, { FC } from 'react';
import { Route, Switch } from 'react-router-dom';
import PrivateRoute from '../PrivateRoute';
import PublicRoute from '../PublicRoute';
import LoginPage from '../../components/LoginPage';
import RegisterPage from '../../components/RegisterPage';

const Routing: FC = () => {
  return (
    <>
      <Switch>
        <PublicRoute exact path="/login" component={LoginPage} />
        <PublicRoute exact path="/register" component={RegisterPage} />
        <PrivateRoute exact path="/" component={() => <span>Landing page</span>} />
        <PrivateRoute exact path="/dashboard" component={() => <span>Dashboard</span>} />
        <Route path="/*" component={() => <span>Error</span>} />
      </Switch>
    </>
  );
}

export default Routing;