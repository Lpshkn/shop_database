import flask


def add_icon_path():
    def add_icon():
        return flask.url_for('static', filename='images/icons/add.svg')
    return dict(add_icon=add_icon)


def sort_icon_path():
    def sort_icon():
        return flask.url_for('static', filename='images/icons/sort-solid.svg')
    return dict(sort_icon=sort_icon)
