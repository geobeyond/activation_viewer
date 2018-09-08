import React from 'react';
import {GridList} from 'material-ui/GridList';
import CollMapSnippet from './CollectionMapSnippet.jsx';
import 'whatwg-fetch';
import queryString from 'query-string';
import TextField from 'material-ui/TextField';
import AppConfig from '../constants/AppConfig.js';

const styles = {
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
  },
  gridList: {
    width: '100%',
    height: 450,
    overflowY: 'auto',
  },
};

export default class LatestMaps extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      'maps': [],
      'query': {}
    }
  }

  _prepareQueryString(){
    for (let param in this.state.query){
      if(this.state.query[param] == ''){
        delete this.state.query[param];
      }
    }
    return queryString.stringify(this.state.query);
  }

  _doQuery(){
    let self = this;
    let query_string = this._prepareQueryString();
    let url = query_string === '' ? AppConfig.LIST_MAPS_URL
      : AppConfig.LIST_MAPS_URL + '?' + query_string;
    fetch(url,{
      credentials: 'same-origin'
    })
    .then(function(response){
      return response.json();
    })
    .then(function(json){
      self.setState({
        'maps': json.objects
      });
    });
  }

  componentWillMount(){
    this._onSearch = this._onSearch.bind(this);
  }

  componentDidMount(){
    this._doQuery();
  }

  componentDidUpdate(prevProps, prevState){
    // Compare the previous state of the query to detemine whether to issue another request or not
    if(JSON.stringify(prevState.query) != JSON.stringify(this.state.query)){
      this._doQuery();
    }
  }

  _onSearch(event){
    this.setState({
      query: {
        q: event.target.value
      }
    });
  }

  render() {
    let selectInteraction = null;

    return (
      <div id="latest_maps" style={styles.root}>
        <TextField
            hintText="Search"
            floatingLabelText="Search"
            onChange={this._onSearch}
            className={'mapsSearch'}
            floatingLabelFocusStyle={{'color': 'rgba(255, 255, 255, 1)'}}
          />
        <GridList
          cellHeight={180}
          cols={4}
          padding={20}
          style={styles.gridList}
        >
          {this.state.maps.map((collmap) => (
            <CollMapSnippet
              key={collmap.map_id}
              collmap={collmap}
            >
            <img src={collmap.thumbnail_url} />
            </CollMapSnippet>
          ))}
        </GridList>
      </div>
    )
  }
}
