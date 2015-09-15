'use strict';

(function(){
  angular.module('composer', [])
    .controller('ActList', function($scope, composer){
      $scope.composer = composer;
      $scope.layers_params = '';
  
      $scope.newMap = function(){
        var items = composer.getCart().items;
        var params = '';
        for(var i=0; i<items.length; i++){
          params += 'layer=' + items[i].typename +'&';
        }
        window.location = '/maps/new?' + params;
      }
    })

    .controller('ActSnippetCtrl', function($scope){
      
    })

    .directive('composerCart', [function(){
      return {
        restrict: 'E',
        controller: 'ActList',
        scope: {},
        templateUrl: "/static/js/app/templates/_composerCart.html"
      };
    }])

    .directive('snippetModal', [function(){
      return {
        restrict: 'E',
        controller: 'ActSnippetCtrl',
        templateUrl: "/static/js/app/templates/_snippet_modal.html"
      };
    }])

    .service('composer', function(){
      
      this.init = function(){
        this.$cart = {
          items: []
        };
      };

      this.getCart = function(){
        return this.$cart;
      }

      this.addItem = function(item){
        if(this.getItemById(item.id) === null){
          this.getCart().items.push(item);
        }
      }

      this.removeItem = function(id){
        if(this.getItemById(id) !== null){
          var cart = this.getCart();
          angular.forEach(cart.items, function(item, index){
            if(item.id === id){
              cart.items.splice(index, 1);
            }
          });
        }
      }

      this.getItemById = function (itemId) {
        var items = this.getCart().items;
        var the_item = null;
        angular.forEach(items, function(item){
          if(item.id === itemId){
            the_item = item;
          }
        });
        return the_item;
      };
    })

    .run(['composer', function(composer){
      composer.init();
    }])
})();