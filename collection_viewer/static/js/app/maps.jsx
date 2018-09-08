import React from 'react';
import ReactDOM from 'react-dom';
import {IntlProvider} from 'react-intl';
import injectTapEventPlugin from 'react-tap-event-plugin';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {List} from 'material-ui/List';
import ViewerAppBar from './components/ViewerAppBar.jsx';
import CustomTheme from './theme';
import LatestMaps from './components/MapsGrid.jsx';

injectTapEventPlugin();


class App extends React.Component {
  getChildContext() {
    return {
      muiTheme: getMuiTheme(CustomTheme)
    };
  }
  getMapItem() {

  }
  render() {
    return (
      <div id='content'>
        <ViewerAppBar page={'maps'} />
        <LatestMaps />
      </div>
    );
  }
}

App.childContextTypes = {
  muiTheme: React.PropTypes.object
};

ReactDOM.render(
  <IntlProvider locale="en"><App /></IntlProvider>,
  document.getElementById('main')
);
