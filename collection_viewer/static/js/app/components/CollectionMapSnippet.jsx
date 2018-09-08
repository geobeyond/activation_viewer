import React, { Component, PropTypes } from 'react';
import AppConfig from '../constants/AppConfig.js';


function getStyles(props, context) {
  const {baseTheme, gridTile} = context.muiTheme;

  const actionPos = props.actionIcon && props.actionPosition;

  const styles = {
    root: {
      position: 'relative',
      display: 'block',
      height: '200px',
      width: '300px',
      overflow: 'hidden'
    },
    titleBar: {
      position: 'absolute',
      left: 0,
      right: 0,
      [props.titlePosition]: 0,
      height: props.subtitle
        ? 68
        : 48,
      background: props.titleBackground,
      display: 'flex',
      alignItems: 'center'
    },
    titleWrap: {
      flexGrow: 1,
      marginLeft: actionPos !== 'left'
        ? baseTheme.spacing.desktopGutterLess
        : 0,
      marginRight: actionPos === 'left'
        ? baseTheme.spacing.desktopGutterLess
        : 0,
      color: gridTile.textColor,
      overflow: 'hidden'
    },
    title: {
      fontSize: '16px',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap'
    },
    subtitle: {
      fontSize: '12px',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap'
    },
    actionIcon: {
      order: actionPos === 'left'
        ? -1
        : 1
    },
    childImg: {
      height: '100%',
      transform: 'translateX(-50%)',
      position: 'relative',
      left: '50%'
    }
  };
  return styles;
}

/*
* A single snippet for the home page maps grid. Each snippet renders it's own thumbnail
* and click on the html component.
*/

class CollMapSnippet extends Component {

  constructor(props) {
    super();
    this.onSnippetclick = this.onSnippetclick.bind(this);
    this.state = {
      selectClass: ''
    };
  }

  onSnippetclick() {
    window.location = AppConfig.COMPOSER_URL + '#' + this.props.collmap.map_id;
  }

  render() {
    const {
      title, subtitle, titlePosition, // eslint-disable-line no-unused-vars
      titleBackground, // eslint-disable-line no-unused-vars
      actionIcon, // eslint-disable-line no-unused-vars
      actionPosition, // eslint-disable-line no-unused-vars
      style,
      children,
      containerElement,
      collmap,
      ...other
    } = this.props;

    const { prepareStyles } = this.context.muiTheme;
    const styles = getStyles(this.props, this.context);
    const mergedRootStyles = Object.assign(styles.root, style);

    let titleBar = (
      <div key="titlebar" className={'snippetTitle'} style={prepareStyles(styles.titleBar)} onClick={function () { window.location = AppConfig.COMPOSER_URL + '#' + collmap.map_id }}>
        <div style={prepareStyles(styles.titleWrap)}>
          <div style={prepareStyles(styles.title)}>{this.props.collmap.map_id}</div>
          {/* <div style={prepareStyles(styles.subtitle)}>
          {this.props.collection.collection_type.name} in {this.props.collection.region.name}
        </div> */}
        </div>
        {actionIcon ? (<div style={prepareStyles(styles.actionIcon)}>{actionIcon}</div>) : null}
      </div>
    );

    let newChildren = children;

    // if there is a single image passed as children
    // clone it and add our styles
    if (React.Children.count(children) === 1) {
      newChildren = React.Children.map(children, (child) => {
        if (child.type === 'img') {
          return React.cloneElement(child, {
            key: 'img',
            ref: 'img',
            style: prepareStyles(Object.assign({}, styles.childImg, child.props.style)),
          });
        } else {
          return child;
        }
      });
    }
    const containerProps = {
      style: prepareStyles(mergedRootStyles),
      onMouseEnter: this.onMouseEnterHandler,
      onMouseLeave: this.onMouseLeaveHandler,
      onClick: this.onSnippetclick,
      className: this.state.selectClass,
      ...other,
    };

    return React.isValidElement(containerElement) ?
      React.cloneElement(containerElement, containerProps, [newChildren, titleBar]) :
      React.createElement(containerElement, containerProps, [newChildren, titleBar]);
  }

}

CollMapSnippet.propTypes = {
  /**
   * An IconButton element to be used as secondary action target
   * (primary action target is the tile itself).
   */
  actionIcon: PropTypes.element,
  /**
   * Position of secondary action IconButton.
   */
  actionPosition: PropTypes.oneOf(['left', 'right']),
  /**
   * Theoretically you can pass any node as children, but the main use case is to pass an img,
   * in whichcase ActSnippet takes care of making the image "cover" available space
   * (similar to background-size: cover or to object-fit:cover).
   */
  children: PropTypes.node,
  /**
   * Width of the tile in number of grid cells.
   */
  cols: PropTypes.number,
  /**
   * Either a string used as tag name for the tile root element, or a ReactElement.
   * This is useful when you have, for example, a custom implementation of
   * a navigation link (that knows about your routes) and you want to use it as the primary tile action.
   * In case you pass a ReactElement, please ensure that it passes all props,
   * accepts styles overrides and render it's children.
   */
  containerElement: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
  /**
   * Height of the tile in number of grid cells.
   */
  rows: PropTypes.number,
  /**
   * Override the inline-styles of the root element.
   */
  style: PropTypes.object,
  /**
   * String or element serving as subtitle (support text).
   */
  subtitle: PropTypes.node,
  /**
   * Title to be displayed on tile.
   */
  title: PropTypes.node,
  /**
   * Style used for title bar background.
   * Useful for setting custom gradients for example
   */
  titleBackground: PropTypes.string,
  /**
   * Position of the title bar (container of title, subtitle and action icon).
   */
  titlePosition: PropTypes.oneOf(['top', 'bottom']),

  collmap: PropTypes.object,

};

CollMapSnippet.defaultProps = {
  titlePosition: 'bottom',
  titleBackground: 'rgba(0, 0, 0, 0.4)',
  actionPosition: 'right',
  cols: 1,
  rows: 1,
  containerElement: 'div'
};

CollMapSnippet.contextTypes = {
  muiTheme: PropTypes.object.isRequired
};

export default CollMapSnippet;