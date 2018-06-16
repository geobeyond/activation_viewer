import ReactDOM from 'react-dom';
import ReactTransitionGroup from 'react-addons-transition-group';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import React, {Component, PropTypes} from 'react';
import classNames from 'classnames';
import FlatButton from 'material-ui/FlatButton';
import CustomTheme from '../theme';
import CollectionStore from '../stores/CollectionStore'
import CollectionInfoSnippet from './CollectionInfoSnippet.jsx'

class CollInfo extends Component {

  constructor(){
    super();
    this.state = {
      collections: []
    }
  }

  componentWillUnmount(){
    CollectionStore.removeChangeListener(this._onChangeCb);
  }

  componentWillMount(){
    this._onChangeCb = this._onChange.bind(this);
    CollectionStore.addChangeListener(this._onChangeCb);
    this._onChange();
  }

  _onChange() {
    this.setState({collections: CollectionStore.getCollections()});
  }

  render(){
    return (
      <div id={'infoPanelContent'}>
        {this.state.collections.map((collection) => (
          <CollectionInfoSnippet key={collection.collection_id} collection={collection} />
        ))}
      </div>
    )
  }
}


export default class CollInfoPanel extends Component {

  constructor(props){
    super(props);
    this.state = {
      show: false
    }
  }

  _togglePanel(){
    this.setState({show: !this.state.show});
  }

  render(){
    return (
      <div id={'collInfoPanel'}>
        <FlatButton
          id={'openInfoPanel'}
          primary={true} 
          label={'Toggle Info'}
          onTouchTap={this._togglePanel.bind(this)} 
          labelStyle={{color: CustomTheme.palette.textColor}}
          style={{
            borderTop: '1px solid #BDBDBD',
            borderLeft: '1px solid #BDBDBD',
            borderRight: '1px solid #BDBDBD',
            borderRadius: '3px 3px 0 0',
          }}
          rippleColor={'#faa73f'}
        />
        <ReactCSSTransitionGroup
          transitionName="infoPanelContent"
          transitionEnterTimeout={500}
          transitionLeaveTimeout={300}>
          {this.state.show ? <CollInfo /> : null}
        </ReactCSSTransitionGroup>
      </div>
    )
  }
}
