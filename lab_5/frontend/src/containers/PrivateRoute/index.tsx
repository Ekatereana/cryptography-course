import React, {FC, useEffect} from 'react';
import Header from '../../components/Header';
import { Route} from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import { IAppState } from '../../models/appState';
import { loadUserRoutine } from '../../sagas/auth/routines';
import { connect, ConnectedProps } from 'react-redux';

export interface IPrivateRouteProps {
  component: any;
  exact: boolean;
  path: string;
}

const PrivateRoute: FC<IPrivateRouteProps & PrivateRouteStateProps> = ({
  component: Component,
  user,
  loadUserData,
  ...rest
}) => {
  const history = useHistory();

  useEffect(() => {
    if (!user) {
      loadUserData(history);
    }
  }, [user, loadUserData]);

  return (
    <Route
      {...rest}
      render={(props) => (
            <>
              <Header />
              <Component/>
            </>
      )}
    />
  );
};

const mapStateToProps = (appState: IAppState) => ({
  user: appState.auth.user
});

const mapDispatchToProps = {
  loadUserData: loadUserRoutine,
};

const connector = connect(mapStateToProps, mapDispatchToProps);
type PrivateRouteStateProps = ConnectedProps<typeof connector>;
export default connector(PrivateRoute);
