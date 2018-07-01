import ReactDOM from 'react-dom';
import React, {Component, PropTypes} from 'react';
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table';

/*
* Describes the collection metadata table into the map composer.
*/

export default class CollectionInfoSnippet extends Component{
  render(){
    let collection = this.props.collection;
    let event_time = new Date(collection.event_time);
    let collection_time = new Date(collection.collection_time);

    return (
      <Table selectable={false} wrapperStyle={{maxWidth: '500px', float: 'left', marginRight: '8px'}}>
        <TableHeader displaySelectAll={false}>
          <TableRow>
            <TableHeaderColumn colSpan="2" style={{textAlign: 'center'}}>
              {collection.collection_id} - {collection.collection_type.name} in {collection.region.name}
            </TableHeaderColumn>
          </TableRow>
        </TableHeader>
        <TableBody displayRowCheckbox={false}>
          <TableRow>
            <TableRowColumn style={{width: '100px'}}>Event time</TableRowColumn>
            <TableRowColumn>{event_time.toString()}</TableRowColumn>
          </TableRow>
          <TableRow>
            <TableRowColumn style={{width: '100px'}}>Collection time</TableRowColumn>
            <TableRowColumn>{collection_time.toString()}</TableRowColumn>
          </TableRow>
          <TableRow>
            <TableRowColumn style={{width: '100px'}}>Glide number</TableRowColumn>
            <TableRowColumn>{collection.glide_number == '' ? 'Not available' : collection.glide_number}</TableRowColumn>
          </TableRow>
        </TableBody>
      </Table>
    )
  }
}

CollectionInfoSnippet.propTypes = {
  /**
   * Style for the button.
   */
  collection: React.PropTypes.object.isRequired
}
