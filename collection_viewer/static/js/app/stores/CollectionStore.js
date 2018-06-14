import AppDispatcher from 'boundless-sdk/dispatchers/AppDispatcher';
import {EventEmitter} from 'events';
import LayerConstants from 'boundless-sdk/constants/LayerConstants';


class CollectionStore extends EventEmitter {
  constructor(){
    super();
    this.collections = [];
  }

  addCollection(collection){
    this.collections.push(collection);
    this.emitChange();
  }

  removeCollection(collection_id){
    let self = this;
    self.collections.forEach(function(collection, index){
      if (collection.collection_id === collection_id){
        self.collections.splice(index, 1);
      }
    });
    self.emitChange();
  }

  getCollections(){
    return this.collections;
  }

  emitChange() {
    this.emit('CHANGE');
  }

  addChangeListener(cb) {
    this.on('CHANGE', cb);
  }

  removeChangeListener(cb) {
    this.removeListener('CHANGE', cb);
  }
} 

var _collectionStore = new CollectionStore();

export default _collectionStore;

AppDispatcher.register(function(payload){
  let action = payload.action;
  switch (action.type) {
    case 'add-collection':
      _collectionStore.addCollection(action.collection);
      break;
    case LayerConstants.REMOVE_LAYER:
      let layer = action.layer;
      if (layer.get('coll_id')){
        _collectionStore.removeCollection(layer.get('coll_id'));
      }
      break;
    default:
      break;
  }
});
