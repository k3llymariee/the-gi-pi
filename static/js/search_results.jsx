class SearchResult extends React.component {
    render() {
    return (
        <div className="food">
            <p>Name: {this.props.brand_name_item_name}</p>
            <img src={this.props.imgURL} />
            <p>Brand: {this.props.brand_name}</p>
        </div>
    );
    }
}